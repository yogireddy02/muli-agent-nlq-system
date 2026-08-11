BLOCKED_PATTERNS = [
    "drop table",
    "drop database",
    "delete all",
    "delete everything",
    "truncate table",
    "update all",
    "alter table",
    "ignore previous instructions",
    "ignore your instructions",
    "show me the database password",
    "show me the api key",
    "show me the secret",
]

def validate_user_input(question: str):

    normalized_question = question.lower().strip()

    for pattern in BLOCKED_PATTERNS:
        if pattern in normalized_question:
            return False, f"Blocked request: {pattern}"

    return True, "Input is safe."