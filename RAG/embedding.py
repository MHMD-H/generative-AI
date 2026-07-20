from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from load_data import load_document
from langchain_chroma import Chroma
from splitting import Split_text

def embedding_store():
    chunks = Split_text()
    embeddings  = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-small")

    vectordb = Chroma.from_documents(documents=chunks,embedding=embeddings,persist_directory="chroma/")
    
    return vectordb
