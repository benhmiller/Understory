from dotenv import load_dotenv
from openai import OpenAI
import os

# Load the environment variables from the .env file
load_dotenv()

# Set API Key and model
MODEL = "gpt-4o-mini"
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def send_text_to_gpt(text):
    response = client.chat.completions.create(model="gpt-4",
    messages=[
        {"role": "system", "content": "You are an AI that extracts key fields from insurance loss runs."},
        {"role": "user", "content": text}
    ])
    return response.choices[0].message.content

if __name__ == "__main__":
     send_text_to_gpt("TEST")