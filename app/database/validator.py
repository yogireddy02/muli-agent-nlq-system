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

    test_sql = """
        UPDATE products
        SET price = 0;
        """

    valid, message = validate_sql(test_sql)

    print("Valid:", valid)
    print("Message:", message)

