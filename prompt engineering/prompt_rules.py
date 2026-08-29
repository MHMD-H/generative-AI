import openai
import os


client = openai.OpenAI(api_key = os.getenv("API_KEY"))
def generate_completeness(prompt,model="gpt-5-mini"):
    messages = [{"role":"user","content" : prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=1)
    
    return response.choices[0].message.content

text = """
Artificial Intelligence is transforming many industries.
It helps automate repetitive tasks, improve decision-making,
and create new applications in healthcare, finance, and education.
However, AI also raises concerns about privacy, bias,
and job displacement.
"""

#summarize the text in one line 
prompt = f"""Summarize the following text that are delimited by triple backticks in one line:\
    ```{text}```"""
summary = generate_completeness(prompt)
print("Summary:", summary)


#return in json format
prompt =f"""summarize the following text :\
    ```{text}```
    and return output in json format that contain the following keys :
    summary,topic,sentiment"""

