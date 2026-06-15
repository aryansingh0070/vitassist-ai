import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

print("Key loaded:", bool(api_key))
print("Key length:", len(api_key))

genai.configure(api_key=api_key)

try:
    models = genai.list_models()

    print("CONNECTED!")
    for model in models:
        print(model.name)

except Exception as e:
    print("ERROR:")
    print(repr(e))