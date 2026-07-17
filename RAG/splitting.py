from langchain_text_splitters import RecursiveCharacterTextSplitter
from load_data import load_document

def Split_text(chunk_size,chunk_overlap):
    docs = load_document()
    split = RecursiveCharacterTextSplitter(
        separators=["\n\n","\n","."," ",""],
        chunk_size=chunk_size,
        chunk_overlap = chunk_overlap
    )
    chunks = split.split_documents(docs)
    return chunks
    
