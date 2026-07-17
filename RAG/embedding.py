from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddingss
from load_data import load_document
from langchain_chroma import Chroma
from splitting import Split_text

def embedding_store():
    chunks = Split_text()
    embeddings  = OpenAIEmbeddingss(model="text-embedding-3-large")

    vectordb = Chroma.from_documents(documents=chunks,embedding=embeddings,persist_directory="chroma/")
    
    return vectordb
