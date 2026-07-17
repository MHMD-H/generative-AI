from langchain_text_splitters import CharacterTextSplitter,RecursiveCharacterTextSplitter,TokenTextSplitter,MarkdownHeaderTextSplitter
from langchain_community.document_loaders import PyPDFLoader
#define chunk size and overlap
chunk_size =100 
chunk_overlap = 4

#split text by charcters 
text_R_split = RecursiveCharacterTextSplitter(
    separators=["\n\n" , "\n"," ",""],
    chunk_size = chunk_size,
    chunk_overlap = chunk_overlap
)

text_C_split = CharacterTextSplitter(
    
    chunk_size = chunk_size,
    chunk_overlap = chunk_overlap
)

#text
text ="""A report says that people keep more unused electronics. Four years ago, one family usually has 20 things. Now, it is about 30. Most people keep remote controls, old phones, and hairdryers.
People want to recycle these things. But it is not so easy. There are too many things. Companies are not able to recycle them all.
It is not good. These things have important materials in them. We can use these materials again. It saves natural resources.
Another problem is that companies do not make good products. Some products do not last long. Also, it is not possible to repair them. People throw them away and buy new things. It is good for companies but not for the natural world."""
text_R_chunk = text_R_split.split_text(text)
text_C_chunk = text_C_split.split_text(text)


print(text_R_chunk)
print(text_C_chunk)



#document split
#1.load document 
loader = PyPDFLoader("data/_Ch3_Lect. 5-47-76.pdf")

#2.create docs
docs = loader.load()
print(len(docs))#30

#3. split 
documnt_split =  RecursiveCharacterTextSplitter(
    separators=["\n\n" , "\n"," ",""],
    chunk_size = 1000,
    chunk_overlap = 0
)
docs_chunks = documnt_split.split_documents(docs)
print(len(docs_chunks))#32


