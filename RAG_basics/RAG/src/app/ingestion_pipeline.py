
import sys
from embedding import ChromaVectorStore
from chunks import ChunkerFactory
from metadata import MetadataEnrichment
from loaders import LoaderFactory
from prompt_loading import (  OpenAIResponse , OpenAIResponseAdapter)
from token_limiting import TokenBudget
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
vector_db=vector_chroma.vectorstore
vector_db.add_documents(chunks)

def semantic_search_(k,query,title = None)  :
    if title is None:
        return vector_db.similarity_search(k=k,query=query)
    return vector_db.similarity_search(k=k,query=query,filter={"title":title})

relative_docs = semantic_search_(3,query)

client = OpenAIResponse()
llm_response = OpenAIResponseAdapter(client)
output = llm_response.invoke(query,relative_docs)
token_calculation = client.calculate_usage()

token_consuming = TokenBudget()
token_consuming.limiting(token_calculation["Total_tokens"])
token_consuming.calculate_tokens(token_calculation["Input_tokens"], token_calculation["Output_tokens"])

tokens_status = token_consuming.get_status()
print(output)
print(tokens_status)
    
