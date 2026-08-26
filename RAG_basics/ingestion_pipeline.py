
import sys
from embedding import ChromaVectorStore
from chunks import ChunkerFactory
from metadata import MetadataEnrichment
from loders import LoaderFactory
from prompt_loading import Response
from token_limiting import tokenbudget
sys.stdout.reconfigure(encoding="utf-8")

source = r"Docs\RAG_Search_Retrieval_Guide_AR.pdf"  # Replace with your PDF file path
loader_factory = LoaderFactory()

loader = loader_factory.define_type(source)
documents = loader.load(source)

# Enrich metadata for each document
metadata_enricher = MetadataEnrichment(visibility="public", title="RAG Search Retrieval Guide", source_type=loader.source_type)
chunker_factory = ChunkerFactory()
chunks = []
for document in documents:
    document.metadata = metadata_enricher.enrich_metadata(document.metadata)
    chunker = chunker_factory.create(document.metadata)
    chunk = chunker.split_document([document])
    chunks.extend(chunk)
    print(f"Document content: {document.page_content[:500]} , metadata: {document.metadata}")  # Print first 500 characters of each document

query = input("How can i help you ?")
vector_chroma = ChromaVectorStore()
vectror_db=vector_chroma.vectorstore
vectror_db.add_documents(chunks)

def semantic_search_(k,query,title = None)  :
    if title is None:
        return vectror_db.similarity_search(k=k,query=query)
    return vectror_db.similarity_search(k=k,query=query,filter={"title":title})

relative_docs = semantic_search_(3,query)

llm_response = Response()
output = llm_response.get_response(query,relative_docs)
token_calculation = llm_response.calculate_usage()

token_consuming = tokenbudget()
token_consuming.limiting(token_calculation["Total_tokens"])
token_consuming.calculate_tokens(token_calculation["Input_tokens"], token_calculation["Output_tokens"])

tokens_status = token_consuming.get_status()
print(output)
print(tokens_status)
    
