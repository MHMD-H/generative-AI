import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def get_response(messages, model="openai/gpt-oss-120b", temperature=0):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature
    )
    return response.choices[0].message.content


# نفس الـ context بتاعك
if "context" not in st.session_state:
    st.session_state.context = [
        {
            "role": "system",
            "content": """You are Ai fitness coach
    help users to in thier problems about fitness and gym but follow the next instructions:
    1- you should not give any medical advice or diagnosis.
    2-be serious with trainees and don't dedicate thek with jokes
    3-encourage trainees if they told you anything about thier progress
    4-if some one ask you about how to lose weight or gain weight ask him for his:
    -age
    -current weight
    -intended weight
    -height
    -activity level
    -has he suffered from any disease or not
    then calculate BMR and TDEE
    5-give him the final answer"""
        }
    ]


def call_messages():
    prompt = st.chat_input("Can I help you?")

    if prompt:
        st.session_state.context.append(
            {"role": "user", "content": prompt}
        )

        response = get_response(st.session_state.context)

        st.session_state.context.append(
            {"role": "assistant", "content": response}
        )


st.title("🏋️ AI Fitness Coach")

call_messages()

# عرض المحادثة
for message in st.session_state.context:
    if message["role"] == "system":
        continue

    with st.chat_message(message["role"]):
        st.write(message["content"])