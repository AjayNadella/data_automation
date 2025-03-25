import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=groq_api_key)

def extract_fields(email_text,prompt_template):

    response = client.chat.completions.create(
        model="llama3-8b-8192",  
        messages=[
            {
                "role": "system",
                "content": "You are an intelligent assistant that extracts structured data from emails/pdfs/docs/csv."
            },
            {
                "role": "user",
                "content": prompt_template
            }
        ]
    )
    return response.choices[0].message.content

