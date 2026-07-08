import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key =os.getenv("GROQ_API_KEY"),
                base_url="https://api.groq.com/openai/v1")

def get_response(prompt,model ="openai/gpt-oss-120b") : 
    response = client.chat.completions.create (
        model =model ,
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
        
    )
    return response.choices[0].message.content



example = """Hello,

My name is Ahmed Hassan. I recently graduated with a degree in Computer Science from Cairo University.

I have experience with Python, SQL, TensorFlow, and machine learning. During my graduation project, I built a model to predict customer churn with an accuracy of 91%.

I also completed internships in data analysis and AI engineering.

I am applying for the Junior AI Engineer position.

Please find my resume attached.

Thank you for your time.

Best regards,
Ahmed Hassan"""


#start with simple prompt
prompt = f"""extract personal information from the following text :\

```{example}```"""


#modify prompt to suit the task and repeat this process until you get the desired output
prompt = f"""extract personal information from the following text :\
```{example}```\
ans return the rsult in json format with the following keys : name, education, skills, experience, position_applied_for"""


job_description = """
Company: Future Vision AI Solutions

Position: Machine Learning Engineer

We are looking for a skilled Machine Learning Engineer to join our AI team.

Requirements:
- Bachelor's degree in Computer Science, Artificial Intelligence, Data Science, or a related field.
- At least 2 years of experience in Machine Learning or Artificial Intelligence.
- Strong SQL skills.
- Excellent Problem Solving skills.
- Good understanding of Large Language Models (LLMs) concepts.
- Basic knowledge of Cloud platforms such as AWS, Azure, or Google Cloud.
- Good Data Analysis skills.
- Strong Python programming skills.

Projects:
- The candidate must have completed at least 3 Machine Learning or AI projects.
- Each project should achieve an accuracy or performance of at least 90%.

Responsibilities:
- Develop and deploy Machine Learning models.
- Analyze datasets and build predictive models.
- Work with AI and Data Science teams.
- Optimize model performance.
- Implement LLM-based solutions when needed.

Preferred Skills:
- Experience with TensorFlow, PyTorch, or Scikit-learn.
- Good communication and teamwork skills.
"""



prompt = f"""extract the required skills and qualifications from the following job description :\
```{job_description}```\
    """

#give prompt time to think and answer in a structured format
prompt = f"""compare the skills and qualifications extracted from the job description with the skills and qualifications extracted from the resume:\
    the skills and qualifications extracted from the job description are :\
```{job_description}```\
    the skills and qualifications extracted from the resume are :\
```{example}```\
step1 : extract skills from both of them 
step2:compare the skills between them 
step3:if the skills in example are covered with 90% percent or more then go to step 4 otherwise return the missing skills
step4: extract qualifications from both of them 
step5:compare the qualifications between them   
step6 : decide if the candidate in suitable for the job  or not
    """


#And again modify the prompt to get the desired output

prompt = f"""compare the skills and qualifications extracted from the job description with the skills and qualifications extracted from the resume:\
    the skills and qualifications extracted from the job description are :\
```{job_description}```\
    the skills and qualifications extracted from the resume are :\
```{example}```\
step1 : extract skills from both of them 
step2:compare the skills between them 
step3:if the skills in example are covered with 90% percent or more then go to step 4 otherwise return the missing skills
step4: extract qualifications from both of them 
step5:compare the qualifications between them   
step6 : decide if the candidate in suitable for the job  or not

make the comprision in a table and replace <*> with <()>
    """

