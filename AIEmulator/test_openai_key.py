from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv("secure.env", override=True)

api_key = os.getenv("OPENAI_API_KEY")

print("Key found:", api_key is not None)
print("Key starts:", api_key[:12])
print("Key ends:", api_key[-4:])

client = OpenAI(api_key=api_key)

response = client.responses.create(
    model="gpt-4o-mini",
    input="Say hello."
)

print(response.output_text)