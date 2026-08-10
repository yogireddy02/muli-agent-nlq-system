from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)


ANSWER_PROMPT = """
You are an answer generation agent.

Answer the user's question using ONLY the database result provided.

Rules:
1. Do not invent information.
2. Do not perform additional database queries.
3. Be concise and clear.
4. If the result contains product IDs and product names, prefer names.
5. Include relevant numbers such as revenue, counts, or totals.
6. Do not mention SQL, agents, prompts, or internal processing.

User question:
{question}

Database result:
{result}
"""


def generate_answer(question: str, result: str) -> str:

    prompt = ANSWER_PROMPT.format(
        question=question,
        result=result
    )

    response = llm.invoke(prompt)

    return response.content.strip()