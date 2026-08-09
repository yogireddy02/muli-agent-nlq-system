from app.database.connection import get_connection

def execute_query(query):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(query)

        results = cursor.fetchall()

        return results

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":

    query = """
    SELECT
        p.product_name,
        SUM(oi.quantity * oi.unit_price) AS revenue
    FROM products p
    JOIN order_items oi
        ON p.product_id = oi.product_id
    JOIN orders o
        ON oi.order_id = o.order_id
    WHERE o.status = 'completed'
    GROUP BY p.product_name
    ORDER BY revenue DESC
    LIMIT 3;
    """

    results = execute_query(query)

    for product_name, revenue in results:
        print(f"{product_name}: ₹{revenue}")