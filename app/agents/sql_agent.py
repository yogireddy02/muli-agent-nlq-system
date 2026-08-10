import os

from dotenv import load_dotenv

from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import(
    SQLDatabaseToolkit,
    create_sql_agent
)
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq


load_dotenv()


# ============================================================
# 1. DATABASE CONFIGURATION
# ============================================================

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


database_uri = (
    f"postgresql+psycopg2://"
    f"{DB_USER}:{DB_PASSWORD}@"
    f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


# ============================================================
# 2. CONNECT LANGCHAIN TO POSTGRESQL
# ============================================================

db = SQLDatabase.from_uri(database_uri)


# ============================================================
# 3. CREATE GEMINI MODEL
# ============================================================

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)


# ============================================================
# 4. CREATE SQL TOOLKIT
# ============================================================

toolkit = SQLDatabaseToolkit(
    db=db,
    llm=llm
)


tools = toolkit.get_tools()

agent = create_sql_agent(
    llm=llm,
    db=db,
    agent_type="tool-calling",
    verbose=True
)


# ============================================================
# 5. TEST EVERYTHING
# ============================================================

if __name__ == "__main__":

    print("LangChain SQL Agent is ready!")

    question = "Which customer has placed the most orders?"

    print("\nUser Question:")
    print(question)

    response = agent.invoke(
        {
            "input": question
        }
    )

    print("\nFinal Answer:")
    print(response["output"])