import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def generate_quiz(text: str):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise Exception("GEMINI_API_KEY not found in .env")

    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",
        google_api_key=api_key,
        temperature=0.3
    )

    prompt = PromptTemplate(
        input_variables=["content"],
        template="""
You are an expert quiz generator.

Based ONLY on the following Wikipedia content, generate 5 MCQs.
Each MCQ must include:
- question
- 4 options
- correct answer
- difficulty (easy, medium, hard)
- short explanation

Content:
{content}

Return JSON array only.
"""
    )

    chain = LLMChain(llm=llm, prompt=prompt)
    result = chain.run(content=text[:4000])

    related_topics = [
        "Computer Science",
        "Cryptography",
        "Artificial Intelligence"
    ]

    return eval(result), related_topics
