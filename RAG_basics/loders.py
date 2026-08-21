from langchain_community.document_loaders import (PyPDFLoader, WebBaseLoader,NotionDirectoryLoader)
from abc import ABC, abstractmethod

class DocumentLoader(ABC):

    @abstractmethod
    def load(self,source):
        pass

class PDFLoader(DocumentLoader):
    
    def load(self, file_path):
        loader = PyPDFLoader(file_path)
        return loader.load()

class WebLoader(DocumentLoader):


    def load(self, url):
        loader = WebBaseLoader(url)
        return loader.load()


class NotionLoader(DocumentLoader):
    
    def load(self, file_path):
        loader = NotionDirectoryLoader(file_path)
        return loader.load()


#temparory context loader for testing 
class ContextLoader:
    def __init__ (self,loader : DocumentLoader):
        self.loader = loader

    def set_loader(self, loader: DocumentLoader):
        self.loader = loader

    def perform_loader (self,file_path ) :
        return self.loader.load(file_path)



class LoaderFactory():
    def define_type (self,source):

        if source.endswith(".pdf"):
            return PDFLoader()
        elif source.startswith("http"):
            return WebLoader()
        elif source.endswith(".notion"):
            return NotionLoader()
        else:
            raise ValueError("Unsupported source type. Please provide a valid PDF, URL, or Notion file path.")

def main():
    source = r"RAG_Search_Retrieval_Guide_AR.pdf"  # Replace with your PDF file path
    loader_factory = LoaderFactory()

    loader = loader_factory.define_type(source)
    documents = loader.load(source)
    print(f"Loaded {len(documents)} documents from {source}")

if __name__ == "__main__":
    main()