from typing import TypedDict

class AgentState(TypedDict, total=False):
    user_question: str
    plan: str
    sql_query: str
    validation_result: bool
    validation_message: str
    query_result: bool
    final_answer: str
    error: str
    retry_count: int