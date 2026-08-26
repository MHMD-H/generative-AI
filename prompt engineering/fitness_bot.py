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
        temperature=temperature,
        tools=[calculate_bmr_tdee]
        
    )
    return response.choices[0].message.content


def calculate_bmr_tdee(age:int, weight:float, height:float, activity_level:str) -> dict:
    """
    Calculate BMR and TDEE based on the provided parameters.

    Parameters:
    - age (int): Age in years.
    - weight (float): Weight in kilograms.
    - height (float): Height in centimeters.
    - activity_level (str): Activity level (sedentary, lightly active, moderately active, very active, or extra active).

    Returns:
    - dict: A dictionary containing BMR and TDEE values.
    """
    # Calculate BMR using the Mifflin-St Jeor Equation
    bmr = 10 * weight + 6.25 * height - 5 * age + 5

    # Define activity level multipliers
    activity_multipliers = {
        "sedentary": 1.2,
        "lightly active": 1.375,
        "moderately active": 1.55,
        "very active": 1.725,
        "extra active": 1.9
    }
    # Get the multiplier for the provided activity level
    multiplier = activity_multipliers.get(activity_level.lower(), 1.2)  # Default to sedentary if not found

    # Calculate TDEE
    tdee = bmr * multiplier

    return {"BMR": bmr, "TDEE": tdee}
calculate_bmr_tdee_description= calculate_bmr_tdee.__doc__

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
    and then calculate BMR 
    and then calculate TDEE 
    you are access to a tool that can calculate BMR and TDEE based on the provided parameters : ```calculate_bmr_tdee_description```.
    Use this tool to perform the calculations and then give him plan based on his goal (lose weight or gain weight) and his TDEE
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




