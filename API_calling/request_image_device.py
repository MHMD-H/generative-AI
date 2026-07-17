from openai import OpenAI
import os
from dotenv import load_dotenv
import streamlit as st
import base64

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

#upload image from your device
image_path = r"C:\Users\moham_f78sqay\Pictures\Screenshots\Screenshot 2026-07-07 110317.png"

#open the image in binary mode:
with open(image_path, "rb") as file:
    #convert image --> base64-->string (that make model can read string)
    image_bs64 = base64.b64encode(file.read()).decode("utf-8")


#------------------------------------------------------------
#upload_image from user (using streamlit)

image = st.file_uploader("upload media here", type=["jpg", "png", "jpeg"])


#generate response
def generate_response(messages, model="openai/gpt-oss-120b"):
    response = client.responses.create(
        model=model,
        input=messages
    )
    return response.output_text


context = [
    {
        "role": "system",
        "content": """You are an image analyzer ,analyze any image but take care this condition :
    don't analyze any image doesnot math ethical sanderds and roles"""
    }
]


def collect_messages(prompt, image=None):
    content = []

    content.append({
        "type": "input_text",
        "text": prompt
    })

    if image:
        #convert image-->base64--->string
        image_base64 = base64.b64encode(image.read()).decode("utf-8")

        content.append({
            "type": "input_image",
            "image_url": f"data:image/jpeg;base64,{image_base64}"
        })

    context.append({
        "role": "user",
        "content": content
    })

    response = generate_response(context)

    context.append({
        "role": "assistant",
        "content": response
    })

    return response