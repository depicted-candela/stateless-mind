/* Schema for statelessCommerce */
CREATE TABLE customers (
    customerId SERIAL PRIMARY KEY,
    firstName VARCHAR(50),
    lastName VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    registrationDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE products (
    productId SERIAL PRIMARY KEY,
    productName VARCHAR(100),
    category VARCHAR(50),
    price NUMERIC(10, 2)
);

CREATE TABLE orders (
    orderId SERIAL PRIMARY KEY,
    customerId INT REFERENCES customers(customerId),
    orderDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    totalAmount NUMERIC(10, 2)
);

CREATE TABLE orderItems (
    orderItemId SERIAL PRIMARY KEY,
    orderId INT REFERENCES orders(orderId),
    productId INT REFERENCES products(productId),
    quantity INT,
    pricePerUnit NUMERIC(10, 2)
);