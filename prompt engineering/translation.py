from openai import OpenAI

import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key = os.getenv("GROQ_API_KEY"),
                base_url="https://api.groq.com/openai/v1")


def get_response(prompt,model="openai/gpt-oss-120b",temperature=0) :
    messages = [
        {"role":"system","content":"You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature
    )
    return response.choices[0].message.content

prompt = """generate text in clear language that tailking about family"""





text = """Family is more than just a word; it’s a network of love, care, and shared experiences. Whether your family is big or small, close or spread across the world, \
the connections you nurture today will shape a happier, healthier tomorrow."""


prompt = f"""Translate the following text that are delimited by triple backticks from English to French:\
```{text}```"""



example = """The dashboard is too slow after the latest update.
It's affecting our team's work.
Please fix it as soon as possible."""

prompt = f"""write an official e_mail to the costumer including the next topics:
-thank the costumer for his feedback
-apologize for this problem 
-emphasize that the technical support team will solve the provlem as soon as possible
-ask him to provide us with anyaddtional information that help us to solve the problem

and make sure the the number of words less than 150 
in addition, make sure the e_mail is clear and professional and polite and friendly and empathetic and concise and grammatically correct
and the complaint is : 
```{example}```"""
print(get_response(prompt,model="openai/gpt-oss-120b",temperature=0.7))


