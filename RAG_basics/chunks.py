from langchain_text_splitters import CharacterTextSplitter,RecursiveCharacterTextSplitter,MarkdownHeaderTextSplitter
from abc import ABC , abstractmethod

class Chunker(ABC):
    @abstractmethod
    def split_document(self, documents):
        pass
class RecursiveCharacterChunker(Chunker):
    def __init__(self,chunk_size : int ,chunk_overlap : int , separator : list[str] = None) :
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separator = separator
    def split_document(self,documents):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap, separators=self.separator)
        return text_splitter.split_documents(documents)

class CharacterChunker(Chunker):
    def __init__(self,chunk_size : int ,chunk_overlap : int) :
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_document(self,documents):
        text_splitter = CharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        return text_splitter.split_documents(documents)

    
class MarkdownChunker(Chunker):
    def __init__(self,headers_to_split_on : list[tuple[str, str]]):
        self.headers_to_split_on = headers_to_split_on

    def split_document(self,documents):
        text_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=self.headers_to_split_on)
        chunks = []
        for document in documents:
            for chunk in text_splitter.split_text(document.page_content):
                chunk.metadata = {**document.metadata, **chunk.metadata}
                chunks.append(chunk)
        return chunks

class ChunkerFactory:
    def create(self, metadata):
        source_type = metadata.get("source_type")

        if source_type == "pdf":
            return RecursiveCharacterChunker(
                chunk_size=800,
                chunk_overlap=50,
            )

        if source_type == "web":
            return RecursiveCharacterChunker(
                chunk_size=1000,
                chunk_overlap=100,
            )

        if source_type == "markdown":
            return MarkdownChunker(
                headers_to_split_on=[
                    ("#", "Header 1"),
                    ("##", "Header 2"),
                    ("###", "Header 3"),
                ]
            )

        raise ValueError(f"Unsupported source type: {source_type}")
