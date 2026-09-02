from langchain_community.document_loaders import (PyPDFLoader, WebBaseLoader,NotionDirectoryLoader)
from abc import ABC, abstractmethod

class DocumentLoader(ABC):

    @abstractmethod
    def load(self,source):
        pass

class PDFLoader(DocumentLoader):
    source_type = "pdf"
    
    def load(self, file_path):
        loader = PyPDFLoader(file_path)
        return loader.load()

class WebLoader(DocumentLoader):
    source_type = "web"


    def load(self, url):
        loader = WebBaseLoader(url)
        return loader.load()


class NotionLoader(DocumentLoader):
    source_type = "notion"
    
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
        normalized_source = source.lower()

        if normalized_source.endswith(".pdf"):
            return PDFLoader()
        elif normalized_source.startswith("http"):
            return WebLoader()
        elif normalized_source.endswith(".notion"):
            return NotionLoader()
        else:
            raise ValueError("Unsupported source type. Please provide a valid PDF, URL, or Notion file path.")



