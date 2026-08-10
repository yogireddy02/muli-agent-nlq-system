import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)


PLANNER_PROMPT = """
You are a database query planning agent.

Your job is to create a clear step-by-step plan for answering
a user's natural language question using PostgreSQL.

IMPORTANT:
You MUST use ONLY the following database schema.

TABLES:

categories:
- category_id
- category_name

customers:
- customer_id
- customer_name
- email

products:
- product_id
- product_name
- category_id
- price

orders:
- order_id
- customer_id
- order_date
- status

order_items:
- order_item_id
- order_id
- product_id
- quantity
- unit_price

RELATIONSHIPS:

categories.category_id
    -> products.category_id

customers.customer_id
    -> orders.customer_id

orders.order_id
    -> order_items.order_id

products.product_id
    -> order_items.product_id

IMPORTANT RULES:

1. Never invent tables.
2. Never invent columns.
3. Never assume a table exists unless it is listed above.
4. Revenue should normally be calculated using:
   quantity * unit_price
   from order_items.
5. If the question asks about products, use products.
6. If the question asks about customers, use customers.
7. If the question asks about orders, use orders.
8. If relationships between tables are required, use the relationships
   provided above.
9. The final plan should explain which tables and columns are needed.
10. When calculating revenue from orders, include only orders where
   orders.status = 'completed', unless the user explicitly asks
   for another order status or all orders.
11. Do not write SQL. Only provide the execution plan.

USER QUESTION:
{question}
"""


def create_plan(question: str) -> str:

    prompt = PLANNER_PROMPT.format(
        question=question
    )

    response = llm.invoke(prompt)

    return response.content