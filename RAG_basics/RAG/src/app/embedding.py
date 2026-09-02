from langchain_openai import OpenAIEmbeddings
from pathlib import Path
from config import (embedding_model_name, persist_directory, collection_name)
import os
from dotenv import load_dotenv
load_dotenv()
class ChromaVectorStore:
    def __init__(self, embedding_model_name: str = embedding_model_name, persist_directory: str | Path = persist_directory, collection_name: str = collection_name):
        try:

            from langchain_chroma import Chroma
        except ImportError:
            raise ImportError("Please install langchain_core to use ChromaVectorStore.")   
        
        
        self.embedding_model_name = OpenAIEmbeddings(model=embedding_model_name,api_key=os.getenv("Embedding_API_Key"))  
        self.persist_directory = Path(persist_directory)
        self.collection_name = collection_name
        self.vectorstore = Chroma(
            embedding_function=self.embedding_model_name,   
            persist_directory=str(self.persist_directory),
            collection_name=self.collection_name
        )
    
    def add_documents(self, chunks):
    
        return self.vectorstore.add_documents(chunks)
    
