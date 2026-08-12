import re


FORBIDDEN_KEYWORDS = [
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "TRUNCATE",
    "CREATE",
    "GRANT",
    "REVOKE",
    "MERGE",
    "CALL",
    "EXEC",
    "EXECUTE",
]


def validate_sql(sql: str) -> tuple[bool, str]:

    # --------------------------------------------------
    # 1. Empty SQL
    # --------------------------------------------------

    if not sql or not sql.strip():
        return False, "SQL query is empty."

    sql = sql.strip()


    # --------------------------------------------------
    # 2. Remove trailing semicolon
    # --------------------------------------------------

    normalized_sql = sql.rstrip(";").strip()


    # --------------------------------------------------
    # 3. Block multiple SQL statements
    # --------------------------------------------------

    if ";" in normalized_sql:
        return False, "Multiple SQL statements are not allowed."


    # --------------------------------------------------
    # 4. Only SELECT is allowed
    # --------------------------------------------------

    if not re.match(
        r"^SELECT\b",
        normalized_sql,
        re.IGNORECASE
    ):
        return False, "Only SELECT queries are allowed."


    # --------------------------------------------------
    # 5. Check forbidden keywords
    # --------------------------------------------------

    for keyword in FORBIDDEN_KEYWORDS:

        pattern = rf"\b{keyword}\b"

        if re.search(
            pattern,
            normalized_sql,
            re.IGNORECASE
        ):
            return False, (
                f"Forbidden SQL keyword detected: {keyword}"
            )


    # --------------------------------------------------
    # 6. Block SQL comments
    # --------------------------------------------------

    if "--" in normalized_sql:
        return False, "SQL comments are not allowed."

    if "/*" in normalized_sql or "*/" in normalized_sql:
        return False, "SQL block comments are not allowed."


    # --------------------------------------------------
    # 7. Block dangerous PostgreSQL functions
    # --------------------------------------------------

    dangerous_functions = [
        "pg_sleep",
        "pg_terminate_backend",
        "pg_cancel_backend",
        "dblink_connect",
        "dblink_exec",
    ]

    for function in dangerous_functions:

        pattern = rf"\b{re.escape(function)}\s*\("

        if re.search(
            pattern,
            normalized_sql,
            re.IGNORECASE
        ):
            return False, (
                f"Dangerous SQL function detected: {function}"
            )


    # --------------------------------------------------
    # 8. Final validation
    # --------------------------------------------------

    return True, "SQL query is valid."


# ======================================================
# TESTING
# ======================================================

if __name__ == "__main__":

    test_queries = [

        # Safe
        "SELECT * FROM products",

        "SELECT product_name, price FROM products",

        """
        SELECT p.product_name,
               SUM(oi.quantity * oi.unit_price) AS revenue
        FROM order_items oi
        JOIN products p
            ON oi.product_id = p.product_id
        GROUP BY p.product_name
        ORDER BY revenue DESC
        LIMIT 3
        """,

        # Dangerous
        "UPDATE products SET price = 0",

        "DELETE FROM products",

        "DROP TABLE products",

        "TRUNCATE products",

        "CREATE TABLE test(id INT)",

        # Multiple statements
        "SELECT * FROM products; DELETE FROM products",

        # Comments
        "SELECT * FROM products -- delete everything",

        "SELECT * FROM products /* dangerous */",

        # Dangerous functions
        "SELECT pg_sleep(10)",

        "SELECT pg_terminate_backend(123)",
    ]


    for query in test_queries:

        print("\n" + "=" * 60)

        print("SQL:")
        print(query)

        valid, message = validate_sql(query)

        print("Valid:", valid)
        print("Message:", message)