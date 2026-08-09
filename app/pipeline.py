from app.database.queries import execute_query
from app.database.validator import validate_sql
from app.llm.gemini_client import generate_sql

def run_nlq(question: str):

    print("\nUser Question:")
    print(question)

    # Step-1: Generate SQL
    sql = generate_sql(question)

    print("\nGenerated SQL:")
    print(sql)

    #step-2: Validate SQL
    is_valid, message = validate_sql(sql)

    print("\nValidation:")
    print(message)

    if not is_valid:
        print("\n❌ Query rejected.")
        return

    #step-3: Execute SQL
    try:

        results = execute_query(sql)

    except Exception as error:

        print("\n❌ Database error.")
        print(error)
        return

    #step-4: Display Results
    print("\nResults:")

    for row in results:
        print(row)

if __name__ == "__main__":

    question = "Delete all customers from the database."

    run_nlq(question)