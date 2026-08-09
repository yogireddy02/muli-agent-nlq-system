DATABASE_SCHEMA = """
Database: nlq_knowledge_db

Tables:

customers
- customer_id
- name
- city
- email

categories
- category_id
- category_name

products
- product_id
- product_name
- category_id
- price

orders
- order_id
- customer_id
- order_date
- status

order_items
- order_item_id
- order_id
- product_id
- quantity
- unit_price

Relationships:

products.category_id → categories.category_id

orders.customer_id → customers.customer_id

order_items.order_id → orders.order_id

order_items.product_id → products.product_id

Business rule:

Revenue = quantity × unit_price

Only orders with status = 'completed'
should be included when calculating revenue.
"""