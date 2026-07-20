import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


def get_response(prompt):
    client = OpenAI(
        api_key=os.getenv("GROQ_API_KEY"),
        base_url="https://api.groq.com/openai/v1",
    )

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "user", "content": prompt},
        ],
    )

    return response.choices[0].message.content
