import os

from dotenv import load_dotenv
from google import genai

from app.llm.prompts import DATABASE_SCHEMA

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def generate_sql(question):

    prompt = f"""
You are an expert PostgreSQL SQL developer. 

Your task is to convert the user's natural language question into a PostgreSQL SQL query.

Database schema: {DATABASE_SCHEMA}

Rules:

1. Generate only SQL.
2. Do not use markdown code fences.
3. Only generate SELECT queries.
4. Never generate INSERT, UPDATE, DELETE, DROP,
   ALTER, or TRUNCATE.
5. Use only tables and columns from the schema.
6. Follow the business rules provided.

User questions:

{question}
"""
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )

    return response.text.strip()



if __name__ == "__main__":

    question = "What are the top 3 prouducts by revenue?"

    sql = generate_sql(question)

    print("\nGenerated SQL:\n")
    print(sql)