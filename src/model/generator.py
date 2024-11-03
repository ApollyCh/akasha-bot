import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY_AI = os.getenv("API_KEY_GENAI")
genai.configure(api_key=API_KEY_AI)


class AnswerGenerator:
    model = genai.GenerativeModel("gemini-1.5-flash")

    def generate(self, question, context):
        ask = "Answer the question related with Genshin Impact using the information I provide you"

        response = self.model.generate_content(ask + "\n" + question + "\n" + context)

        return response.text
