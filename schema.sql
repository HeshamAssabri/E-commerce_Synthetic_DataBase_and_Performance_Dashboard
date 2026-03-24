-- Create database
CREATE DATABASE IF NOT EXISTS assabri_shop;
USE assabri_shop;

-- Employees table (self-referencing for manager hierarchy)
CREATE TABLE employees (
    employee_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    hire_date DATE NOT NULL,
    job_title VARCHAR(100) NOT NULL,
    salary DECIMAL(10,2) NOT NULL,
    manager_id INT NULL,
    department VARCHAR(50),
    FOREIGN KEY (manager_id) REFERENCES employees(employee_id)
);

-- Customers table
CREATE TABLE customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(50),
    postal_code VARCHAR(20),
    country VARCHAR(50) DEFAULT 'USA',
    registration_date DATE NOT NULL,
    date_of_birth DATE,
    gender ENUM('Male','Female','Other'),
    is_active BOOLEAN DEFAULT TRUE
);

-- Products table (with product_description)
CREATE TABLE products (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    product_name VARCHAR(200) NOT NULL,
    product_description TEXT,
    category VARCHAR(50) NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    cost DECIMAL(10,2) NOT NULL,
    supplier VARCHAR(100),
    stock_quantity INT NOT NULL,
    reorder_level INT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATE NOT NULL
);

-- Orders table
CREATE TABLE orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    employee_id INT,
    order_date DATETIME NOT NULL,
    required_date DATE,
    shipped_date DATE,
    ship_via VARCHAR(50),
    freight DECIMAL(10,2),
    ship_name VARCHAR(100),
    ship_address VARCHAR(255),
    ship_city VARCHAR(100),
    ship_state VARCHAR(50),
    ship_postal_code VARCHAR(20),
    ship_country VARCHAR(50),
    status ENUM('Pending','Processing','Shipped','Delivered','Cancelled') DEFAULT 'Pending',
    total_amount DECIMAL(10,2),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);

-- Order items table
CREATE TABLE order_items (
    order_item_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    discount DECIMAL(4,2) DEFAULT 0.00,
    total_price DECIMAL(10,2) GENERATED ALWAYS AS (quantity * unit_price * (1 - discount)) STORED,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Reviews table
CREATE TABLE reviews (
    review_id INT PRIMARY KEY AUTO_INCREMENT,
    product_id INT NOT NULL,
    customer_id INT NOT NULL,
    rating TINYINT CHECK (rating BETWEEN 1 AND 5),
    review_text TEXT,
    review_date DATETIME NOT NULL,
    is_verified_purchase BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
