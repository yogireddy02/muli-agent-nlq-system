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
    "REVOKE"
]


def validate_sql(sql: str) -> tuple[bool, str]:

    sql = sql.strip()

    if not sql:
        return False, "SQL query is empty."

    # Remove trailing semicolon
    normalized_sql = sql.rstrip(";").strip()

    # Only allow SELECT statements
    if not re.match(r"^SELECT\b", normalized_sql, re.IGNORECASE):
        return False, "Only SELECT queries are allowed."

    # Check forbidden SQL keywords
    for keyword in FORBIDDEN_KEYWORDS:

        pattern = rf"\b{keyword}\b"

        if re.search(pattern, normalized_sql, re.IGNORECASE):
            return False, f"Forbidden SQL keyword detected: {keyword}"

    return True, "SQL query is valid."

if __name__ == "__main__":

    test_queries = [

        """
        SELECT *
        FROM products;
        """,

        """
        DELETE FROM customers;
        """,

        """
        DROP TABLE products;
        """,

        """
        UPDATE products
        SET price = 0;
        """

    ]

    for query in test_queries:

        valid, message = validate_sql(query)

        print("=" * 50)
        print("Query:")
        print(query.strip())

        print("Valid:", valid)
        print("Message:", message)