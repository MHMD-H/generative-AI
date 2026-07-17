import os

from pathlib import Path

from typing import Iterable

 

from dotenv import load_dotenv

from langchain_chroma import Chroma

from langchain_community.document_loaders import PyPDFLoader

from langchain_core.documents import Document

from langchain_core.prompts import ChatPromptTemplate

from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from langchain_text_splitters import RecursiveCharacterTextSplitter

 

load_dotenv()

 

PDF_PATH = Path("data/company_policy.pdf")

DB_DIR = "./chroma_db"

COLLECTION_NAME = "company_policy"

 

 

def format_context(documents: Iterable[Document]) -> str:

    """Format retrieved chunks with source information for the prompt."""

    blocks: list[str] = []

    for index, doc in enumerate(documents, start=1):

        source = doc.metadata.get("source", "unknown")

        page = doc.metadata.get("page", "?")

        blocks.append(

            f"[Chunk {index} | source={source} | page={page}]\n"

            f"{doc.page_content}"

        )

    return "\n\n".join(blocks)

 

 

def build_vector_store(pdf_path: Path) -> Chroma:

    if not pdf_path.exists():

        raise FileNotFoundError(f"PDF not found: {pdf_path}")

 

    # 1) Load

    documents = PyPDFLoader(str(pdf_path)).load()

 

    # 2) Optional cleaning / metadata enrichment

    for doc in documents:

        doc.page_content = " ".join(doc.page_content.split())

        doc.metadata["file_name"] = pdf_path.name

 

    # 3) Split

    splitter = RecursiveCharacterTextSplitter(

        chunk_size=900,

        chunk_overlap=150,

        separators=["\n\n", "\n", ". ", "؟ ", "! ", "، ", " ", ""],

    )

    chunks = splitter.split_documents(documents)

 

    # 4) Embeddings + 5) Index

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    vector_store = Chroma.from_documents(

        documents=chunks,

        embedding=embeddings,

        collection_name=COLLECTION_NAME,

        persist_directory=DB_DIR,

    )

    print(f"Indexed {len(chunks)} chunks from {len(documents)} pages.")

    return vector_store

 

 

def open_vector_store() -> Chroma:

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    return Chroma(

        collection_name=COLLECTION_NAME,

        persist_directory=DB_DIR,

        embedding_function=embeddings,

    )

 

 

def rewrite_follow_up(

    llm: ChatOpenAI,

    question: str,

    chat_history: list[tuple[str, str]],

) -> str:

    """Turn a follow-up question into a standalone search query."""

    if not chat_history:

        return question

 

    history_text = "\n".join(

        f"User: {user}\nAssistant: {assistant}"

        for user, assistant in chat_history[-4:]

    )

 

    rewrite_prompt = ChatPromptTemplate.from_messages([

        (

            "system",

            "أعد صياغة سؤال المستخدم ليصبح سؤالًا مستقلًا يصلح للبحث. "

            "استخدم تاريخ المحادثة فقط لفهم الضمائر والإشارات. "

            "لا تجب عن السؤال. أعد السؤال فقط.",

        ),

        (

            "human",

            "تاريخ المحادثة:\n{history}\n\nالسؤال الجديد:\n{question}",

        ),

    ])

    response = (rewrite_prompt | llm).invoke(

        {"history": history_text, "question": question}

    )

    return response.content.strip()

 

 

def answer_question(

    vector_store: Chroma,

    llm: ChatOpenAI,

    question: str,

    chat_history: list[tuple[str, str]],

) -> tuple[str, list[Document], str]:

    # 6) Query processing

    standalone_question = rewrite_follow_up(llm, question, chat_history)

 

    # 7) Retrieval: MMR gives relevant but less repetitive chunks

    retriever = vector_store.as_retriever(

        search_type="mmr",

        search_kwargs={"k": 4, "fetch_k": 12},

    )

    documents = retriever.invoke(standalone_question)

 

    # 8) Prompt construction

    context = format_context(documents)

    answer_prompt = ChatPromptTemplate.from_messages([

        (

            "system",

            "أنت مساعد يجيب من السياق المرفق فقط. "

            "إذا لم توجد معلومات كافية، قل بوضوح: "

            "لا توجد معلومات كافية في الملفات للإجابة. "

            "لا تخترع حقائق أو مصادر.\n\nالسياق:\n{context}",

        ),

        ("human", "السؤال: {question}"),

    ])

 

    # 9) Generation

    response = (answer_prompt | llm).invoke(

        {"context": context, "question": question}

    )

    return response.content.strip(), documents, standalone_question

 

 

def print_sources(documents: list[Document]) -> None:

    print("\nSources:")

    seen: set[tuple[str, object]] = set()

    for doc in documents:

        source = doc.metadata.get("source", "unknown")

        page = doc.metadata.get("page", "?")

        key = (source, page)

        if key not in seen:

            seen.add(key)

            print(f"- {source}, page {page}")

 

 

def main() -> None:

    if not os.getenv("OPENAI_API_KEY"):

        raise RuntimeError("OPENAI_API_KEY is missing from .env")

 

    # Build once; after that use open_vector_store() to avoid duplicate indexing.

    if not Path(DB_DIR).exists():

        vector_store = build_vector_store(PDF_PATH)

    else:

        vector_store = open_vector_store()

 

    llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)

    chat_history: list[tuple[str, str]] = []

 

    print("RAG chatbot is ready. Type 'exit' to stop.")

    while True:

        question = input("\nYou: ").strip()

        if question.lower() in {"exit", "quit"}:

            break

        if not question:

            continue

 

        try:

            answer, docs, standalone = answer_question(

                vector_store, llm, question, chat_history

            )

            print(f"\nSearch query: {standalone}")

            print(f"\nAssistant: {answer}")

            print_sources(docs)

            chat_history.append((question, answer))

        except Exception as exc:

            print(f"Error: {exc}")

 

 

if __name__ == "__main_