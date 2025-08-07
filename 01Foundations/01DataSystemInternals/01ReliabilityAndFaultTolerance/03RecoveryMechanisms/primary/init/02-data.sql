/* Initial data for statelessCommerce */
INSERT INTO customers (firstName, lastName, email) VALUES
('Alice', 'Smith', 'alice.smith@example.com'),
('Bob', 'Johnson', 'bob.johnson@example.com');

INSERT INTO products (productName, category, price) VALUES
('Laptop Pro', 'Electronics', 1200.00),
('Wireless Mouse', 'Electronics', 25.50),
('Mechanical Keyboard', 'Electronics', 75.00),
('Data Engineering Essentials', 'Books', 49.99);

INSERT INTO orders (customerId, totalAmount) VALUES
(1, 1225.50),
(2, 124.99);

INSERT INTO orderItems (orderId, productId, quantity, pricePerUnit) VALUES
(1, 1, 1, 1200.00),
(1, 2, 1, 25.50),
(2, 4, 1, 49.99),
(2, 3, 1, 75.00);