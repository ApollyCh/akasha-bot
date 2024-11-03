import google.generativeai as genai
import os
from dotenv import load_dotenv
from transformers import pipeline

load_dotenv()

API_KEY_AI = os.getenv("API_KEY_GENAI")
genai.configure(api_key=API_KEY_AI)


def gemini_ask_questions(question: str, context) -> str:
    ask = "Answer the question related with Genshin Impact using the information I provide you"

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(ask + "\n" + question + "\n" + context)

    return response.text


def robert_ask_questions(question: str, context) -> str:
    question_answerer = pipeline("question-answering", model='distilbert-base-cased-distilled-squad')

    result = question_answerer(question=question, context=context)

    return result["answer"]


if __name__ == "__main__":
    question = "Who is the character with the highest base HP?"
    context = " ".join(
        ["Zhongli has the highest base HP of all characters in the game, with 1311 at level 1 and 1640 at level 90.",
         "Zhongli is a 5-star Geo character in Genshin Impact.",
         "He is a polearm user and has a shield ability that can protect him and his teammates from damage."])

    response = robert_ask_questions(question, context)

    print(response)
