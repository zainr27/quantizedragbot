import os
from dotenv import load_dotenv
import groq

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables. Please set it in your .env file.")

client = groq.Groq(api_key=groq_api_key)

def generate_response(prompt):
    completion = client.chat.completions.create(
        model="moonshotai/kimi-k2-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=100000,
    )
    return completion.choices[0].message.content

prompt_template = (
    "Context information is below. \n"
    "-------------------------------- \n"
    "CONTEXT: {context} \n"
    "-------------------------------- \n"
    "Given the context information above think step by step "
    "to answer the user's query in a crisp and concise manner. "
    "In case you don't know the answer say 'I don't know'. \n "
    "QUERY: {query} \n"
    "ANSWER: "
   
)

