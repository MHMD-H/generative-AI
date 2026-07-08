from openai import OpenAI
from dotenv import load_dotenv
import os 
from base64 import b64encode


load_dotenv()
client = OpenAI(api_key=os.getenv("GROQ_API_KEY"),base_url="https://api.groq.com/openai/v1")

def get_response(messages,model="openai/gpt-oss-120b"):
    response = client.chat.completions.create(
        model =model ,
        messages=  messages
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


def call_messages(prompt,image=None) :
    content = []
    content.append({
        "type":"text",
        "text":prompt
        })

    if image:
        mime_type = image.type
        image.seek(0)
        image_base64 = b64encode(image.read()).decode("utf-8")
        content.append(
            {
                "type":"image_url",
                "image_url" : {
        "url":f"data:{mime_type};base64,{image_base64}"
    }
            }
        )
    context.append({
            "role":"user",
            "content":content
        })
    
    response = get_response(context)
    context.append({
            "role":"assistant",
            "content":response
        })
    return response

