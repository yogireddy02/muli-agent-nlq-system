from langgraph.graph import StateGraph, START, END

from app.graph.state import AgentState
from app.agents.planner import create_plan
from app.agents.sql_writer import generate_sql
from app.database.validator import validate_sql
from app.agents.answer import generate_answer

def planner_node(state: AgentState):

    print("\n--- PLANNER ---")

    question = state["user_question"]

    plan = create_plan(question)

    print("\nGenerated Plan:")
    print(plan)

    return {
        "plan": plan
    }

def sql_writer_node(state: AgentState):

    print("\n--- SQL WRITER ---")

    question = state["user_question"]
    plan = state["plan"]

    previous_sql = state.get("sql_query", "")
    validation_message = state.get(
        "validation_message",
        ""
    )

    sql = generate_sql(
        question=question,
        plan=plan,
        previous_sql=previous_sql,
        validation_message=validation_message
    )

    print("\nGenerated SQL:")
    print(sql)

    return {
        "sql_query": sql,
        "retry_count": state.get("retry_count", 0) + 1
    }

def validator_node(state: AgentState):

    print("\n--- VALIDATOR ---")

    sql = state["sql_query"]

    print("\nSQL being validated:")
    print(sql)

    is_valid, message = validate_sql(sql)

    print("\nValidation result:", is_valid)
    print("Validation message:", message)

    return {
        "validation_result": is_valid,
        "validation_message": message
    }

def validation_router(state: AgentState):

    if state["validation_result"]:
        return "executor"

    retry_count = state.get("retry_count", 0)

    if retry_count >= 2:
        return "answer"

    return "sql_writer"

def executor_node(state: AgentState):

    print("\n--- EXECUTOR ---")

    sql = state["sql_query"]

    print("\nExecuting SQL:")
    print(sql)

    from app.database.queries import execute_query

    try:
        result = execute_query(sql)

        print("\nQuery Result:")
        print(result)

        return {
            "query_result": str(result),
            "error": ""
        }

    except Exception as e:

        print("\nExecution Error:")
        print(e)

        return {
            "query_result": "",
            "error": str(e)
        }


def answer_node(state: AgentState):

    print("\n--- ANSWER ---")

    question = state["user_question"]
    result = state.get("query_result", "")

    final_answer = generate_answer(
        question=question,
        result=result
    )

    print("\nFinal Answer:")
    print(final_answer)

    return {
        "final_answer": final_answer
    }

# --------------------------------------------------
# Build graph
# --------------------------------------------------

builder = StateGraph(AgentState)

builder.add_node("planner", planner_node)
builder.add_node("sql_writer", sql_writer_node)
builder.add_node("validator", validator_node)
builder.add_node("executor", executor_node)
builder.add_node("answer", answer_node)


builder.add_edge(START, "planner")
builder.add_edge("planner", "sql_writer")
builder.add_edge("sql_writer", "validator")
builder.add_conditional_edges(
    "validator",
    validation_router,
    {
        "executor": "executor",
        "sql_writer": "sql_writer",
        "answer": "answer"
    }
)
builder.add_edge("executor", "answer")
builder.add_edge("answer", END)


graph = builder.compile()


# --------------------------------------------------
# Test
# --------------------------------------------------

if __name__ == "__main__":

    result = graph.invoke(
        {
            "user_question": "What are the top 3 products by revenue?"
        }
    )

    print("\n==============================")
    print("FINAL RESULT")
    print("==============================")

    print(result)