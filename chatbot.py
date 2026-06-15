import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-1.5-flash"
)

print("\n🤖 VITAssist AI Started")
print("Type 'exit' to quit\n")

chat = model.start_chat(history=[])

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    try:
        response = chat.send_message(user_input)

        print("\nBot:")
        print(response.text)
        print()

    except Exception as e:
        print("Error:", e)
