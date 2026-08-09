INSERT INTO categories (category_name)
VALUES
('Electronics'),
('Accessories'),
('Home Appliances');

INSERT INTO customers (name, city, email)
VALUES
('Rahul Sharma', 'Bengaluru', 'rahul@example.com'),
('Priya Reddy', 'Hyderabad', 'priya@example.com'),
('Arjun Kumar', 'Chennai', 'arjun@example.com'),
('Sneha Rao', 'Bengaluru', 'sneha@example.com');

INSERT INTO products (product_name, category_id, price)
VALUES
('Laptop', 1, 75000),
('Smartphone', 1, 45000),
('Headphones', 2, 5000),
('Keyboard', 2, 2500),
('Air Conditioner', 3, 55000),
('Washing Machine', 3, 40000);

INSERT INTO orders (customer_id, order_date, status)
VALUES
(1, '2026-01-10', 'completed'),
(2, '2026-01-15', 'completed'),
(3, '2026-02-05', 'completed'),
(4, '2026-02-10', 'completed'),
(1, '2026-03-01', 'completed'),
(2, '2026-03-12', 'cancelled');

INSERT INTO order_items (order_id, product_id, quantity, unit_price)
VALUES
(1, 1, 1, 75000),
(1, 3, 2, 5000),

(2, 2, 1, 45000),
(2, 4, 1, 2500),

(3, 5, 1, 55000),
(3, 3, 1, 5000),

(4, 6, 1, 40000),
(4, 4, 2, 2500),

(5, 2, 2, 45000),
(5, 3, 1, 5000),

(6, 1, 1, 75000);