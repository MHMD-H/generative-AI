from langchain_community.retrievers import BM25Retriever , TFIDFRetriever

from langchain_community.document_loaders import PyPDFLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter
#load docs
pdf = r""
loader = PyPDFLoader(pdf)
docs = loader.load()

#splitiing docs --> chunks
splitter = RecursiveCharacterTextSplitter(chunk_size = 100)

chunks = splitter.split_documents(docs)


vectordb = BM25Retriever(chunks)
vectordb.k = 5


