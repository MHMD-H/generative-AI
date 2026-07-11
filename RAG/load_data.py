import os
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
from langchain.documnt_loader import 


#load api key from .env
load_dotenv()
client = OpenAI(api_key=os.getenv("GROQ_API_KEY"),base_url="https://api.groq.com/openai/v1")

def define_format(url) :
    url = input("enter the URL : ")

    if url.startswith(("http://","https://"))  :
        if "youtube" in url : return "youtube"
        else : return "web"
    format = Path(url).suffix.lstrip(".")
    if format == "pdf" :
        return "pdf"
    elif format in ["png","jpeg","jpeg"] :
        return "image"
    if "notion" in url :
        return "notion"
    return url


def load_document(url) :
    #load PDF document
    format,url = define_format()
    if format == "pdf" :



