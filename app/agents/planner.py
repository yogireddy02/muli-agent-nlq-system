import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)


PLANNER_PROMPT = """
You are a planning agent for a Natural Language Query system.

Your job is to analyze the user's question and create a concise
step-by-step plan for answering it using a PostgreSQL database.

Do NOT write SQL.

Focus on:
1. What information is required?
2. Which database entities/tables are likely relevant?
3. What calculations or filtering are required?
4. What should the final result contain?

User question:
{question}
"""


def create_plan(question: str) -> str:

    prompt = PLANNER_PROMPT.format(
        question=question
    )

    response = llm.invoke(prompt)

    return response.content