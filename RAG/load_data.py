import os
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

# PDF / Web / Notion Loaders
from langchain_community.document_loaders import (
    PyPDFLoader,
    WebBaseLoader,
    NotionDirectoryLoader,
)


# YouTube
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.blob_loaders import FileSystemBlobLoader
from langchain_community.document_loaders.parsers import OpenAIWhisperParser
from langchain_community.document_loaders.blob_loaders.youtube_audio import (
    YoutubeAudioLoader,
)

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

#load api key from .env
load_dotenv()
client = OpenAI(api_key=os.getenv("GROQ_API_KEY"),base_url="https://api.groq.com/openai/v1")

def define_format(url) :
    url=url
    source = None
    if url.startswith(("http://","https://"))  :
        if "youtube" in url or "youtu.be" in url : return url , "youtube"
        else : return url,"web"
    format = Path(url).suffix.lstrip(".")
    if format == "pdf" :
        return url,"pdf"
    elif format in ["png","jpeg","jpg"] :
        return url,"image"
    elif "notion" in url :
        return url,"notion"


def load_document() :
    #load PDF document
    url,format = define_format()
    if format == "pdf" :
        loader = PyPDFLoader(url)
    elif format == "web" :
        loader = WebBaseLoader(url)
    elif format == "notion" :
        loader = NotionDirectoryLoader(url)
    elif format == "youtube" :
        save_dir = "downloads/"
        YoutubeAudioLoader([url],save_dir).load()

        loader = GenericLoader(
            FileSystemBlobLoader(save_dir,glob = "*.mp3"),
            OpenAIWhisperParser()
        )
    docs = loader.load()

    return docs




