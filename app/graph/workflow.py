from langgraph.graph import StateGraph, START, END

from app.graph.state import AgentState
from app.agents.planner import create_plan
from app.agents.sql_writer import generate_sql
from app.database.validator import validate_sql
from app.agents.answer import generate_answer
from app.guardrails.input_guardrails import validate_user_input

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

    print("\nRetry count:", state.get("retry_count", 0))

    sql = generate_sql(
        question=question,
        plan=plan,
        previous_sql=previous_sql,
        validation_message=validation_message
    )

    print("\n[DEBUG] SQL RECEIVED FROM generate_sql:")
    print(repr(sql))

    print("\n[DEBUG] SQL BEFORE RETURN:")
    print(repr(sql))

    result = {
        "sql_query": sql,
        "retry_count": state.get("retry_count", 0) + 1
    }

    print("\n[DEBUG] NODE RETURN:")
    print(repr(result))

    return result

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
        return "sql_failure"

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

def sql_failure_node(state: AgentState):
    print("\n--- SQL FAILURE ---")

    message = (
        "I couldn't generate a safe and valid SQL query "
        "after multiple attempts. The query was not executed."
    )

    print(message)

    return {
        "final_answer": message,
        "error": message
    }


def input_guardrails_node(state:AgentState):
    question = state["user_question"]

    is_valid, message = validate_user_input(question)

    print("\n--- INPUT GUARDRAIL ---")
    print(f"User Question: {question}")
    print(f"Validation: {is_valid}")
    print(f"Message: {message}")

    if not is_valid:
        return {
            "error": message,
            "final_answer": f"Request blocked: {message}"
        }
    return state

def route_after_input_guardrail(state):
    if state.get("error"):
        return "blocked"

    return "planner"

# --------------------------------------------------
# Build graph
# --------------------------------------------------

builder = StateGraph(AgentState)

# Add nodes
builder.add_node("input_guardrails", input_guardrails_node)
builder.add_node("planner", planner_node)
builder.add_node("sql_writer", sql_writer_node)
builder.add_node("validator", validator_node)
builder.add_node("executor", executor_node)
builder.add_node("answer", answer_node)
builder.add_node("sql_failure", sql_failure_node)


# --------------------------------------------------
# Entry point
# --------------------------------------------------

builder.set_entry_point("input_guardrails")


# --------------------------------------------------
# Input Guardrail Routing
# --------------------------------------------------

builder.add_conditional_edges(
    "input_guardrails",
    route_after_input_guardrail,
    {
        "planner": "planner",
        "blocked": END,
    },
)


# --------------------------------------------------
# Main workflow
# --------------------------------------------------

builder.add_edge("planner", "sql_writer")

builder.add_edge("sql_writer", "validator")


# --------------------------------------------------
# SQL Validation Routing
# --------------------------------------------------

builder.add_conditional_edges(
    "validator",
    validation_router,
    {
        "executor": "executor",
        "sql_writer": "sql_writer",
        "answer": "answer",
        "sql_failure": "sql_failure"
    }
)


# --------------------------------------------------
# Execution → Answer
# --------------------------------------------------

builder.add_edge("executor", "answer")

builder.add_edge("answer", END)

builder.add_edge("sql_failure", END)


# --------------------------------------------------
# Compile graph
# --------------------------------------------------

graph = builder.compile()

# --------------------------------------------------
# Test
# --------------------------------------------------

if __name__ == "__main__":

    result = graph.invoke(
        {
            "user_question": "Delete ALL products",
            #"user_question": "Show me the database password",
        }
    )

    print("\n==============================")
    print("FINAL RESULT")
    print("==============================")

    print(result)