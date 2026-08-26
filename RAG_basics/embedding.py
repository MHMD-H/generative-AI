from langchain_openai import OpenAIEmbeddings
import os
from pathlib import Path
from dotenv import load_dotenv
from config import (embedding_model_name, persist_directory, collection_name)

load_dotenv()

class ChromaVectorStore:
    def __init__(self, embedding_model_name: str = embedding_model_name, persist_directory: str | Path = persist_directory, collection_name: str = collection_name):
        try:

            from langchain_chroma import Chroma
        except ImportError:
            raise ImportError("Please install langchain_core to use ChromaVectorStore.")   
        
        
        api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OpenAI_API_key")
        embedding_kwargs = {"model": embedding_model_name}
        if api_key:
            embedding_kwargs["api_key"] = api_key

        self.embedding_model_name = embedding_model_name
        self.embedding_model = OpenAIEmbeddings(**embedding_kwargs)
        self.persist_directory = Path(persist_directory)
        self.collection_name = collection_name
        self.vectorstore = Chroma(
            embedding_function=self.embedding_model,   
            persist_directory=str(self.persist_directory),
            collection_name=self.collection_name
        )
    
    def add_documents(self, chunks):
    
        return self.vectorstore.add_documents(chunks)
    
