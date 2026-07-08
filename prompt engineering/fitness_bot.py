from openai import OpenAI
from dotenv import load_dotenv
import os
import streamlit as st
load_dotenv()
client = OpenAI(api_key=os.getenv("GROQ_API_KEY"),
                base_url="https://api.groq.com/openai/v1")

def get_response(messages,model="openai/gpt-oss-120b",temperature=0) :
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature
    )
    return response.choices[0].message.content


context = [
    {"role":"system","content" : """You are Ai fitness coach\
    help users to in thier problems about fitness and gym but follow the next instructions:
    1- you should not give any medical advice or diagnosis, and you should not provide any information that could be considered medical advice or diagnosis.
    2-be serious with trainees and don't dedicate thek with jokes
    3-encourage trainees if they told you anything about  thier progress
    4-if some one ask you about how to lose weight or gain weight ask fim for his :
    -age
    -current whieght
    -intended weight
    -hieght
    -his activity level (sedentary, lightly active, moderately active, very active, or extra active)
    -has he suufered from any desease or not
     and then use this equation to calculate BMR = 10 * weight(kg) + 6.25 * height(cm) - 5 * age(y) + 5
     and then use this equation to calculate TDEE = BMR * activity level
    and then give him plan based on his goal (lose weight or gain weight) and his TDEE
    5-give him the final answer"""}
]

def call_masseges():
    prompt = input("Can I help you? \n")
    context.append({"role":"user","content":prompt})
    response=get_response(context)
    context.append({"role":"assistant","content":response})
    print(f"AI fitness coach: {response}")

while True:
    call_masseges()



