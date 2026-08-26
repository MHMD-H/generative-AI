import os
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()

def get_client():
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OpenAI_API_key")
    return OpenAI(api_key=api_key)
    
class Response :
    def __init__(self,model="gpt-5-mini",tempreture = .3) :
        
        self.model=model
        self.temperature=tempreture
        self.response = None
        


    

    
    def get_response(self,query,source):
        
        context =[{"role" : "system" , "content" : """
    Answer the question using only the context below.
    If the answer is not in the context, say: I don't know.

    Context:
    {source}

    Question:
    {query}

    Answer:
    """
        }]
        content = {"role":"user","content":f"""Context:
    {source}

    Question:
    {query}
    """}
        context.append(content )
        self.response = get_client().chat.completions.create(
            model=self.model,
            messages=context,
            temperature=self.temperature,
        )
        return self.response.choices[0].message.content
        
    def calculate_usage(self):
            
            return {
                "Input_tokens" : self.response.usage.prompt_tokens,
                "Output_tokens":self.response.usage.completion_tokens,
                "Total_tokens" : self.response.usage.total_tokens
    
            }
    

