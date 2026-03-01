-- Database initialization 
CREATE DATABASE IF NOT EXISTS inventory_management_test; 
USE inventory_management;

CREATE TABLE suppliers (
    supplier_id INT AUTO_INCREMENT PRIMARY KEY,
    supplier_name VARCHAR(150) NOT NULL,
    contact_name VARCHAR(150),
    email VARCHAR(150),
    phone VARCHAR(20),
    address VARCHAR(255)
) ENGINE=InnoDB;

CREATE TABLE products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(150) NOT NULL,
    category VARCHAR(100),
    price DECIMAL(10,2),
    stock_quantity INT DEFAULT 0,
    reorder_level INT DEFAULT 0,
    supplier_id INT,
    FOREIGN KEY (supplier_id)
        REFERENCES suppliers(supplier_id)
) ENGINE=InnoDB;

CREATE TABLE reorders (
    reorder_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    reorder_quantity INT,
    reorder_date DATE,
    status VARCHAR(50),
    FOREIGN KEY (product_id)
        REFERENCES products(product_id)
) ENGINE=InnoDB;

CREATE TABLE shipments (
    shipment_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    supplier_id INT,
    quantity_received INT,
    shipment_date DATE,
    FOREIGN KEY (product_id)
        REFERENCES products(product_id),
    FOREIGN KEY (supplier_id)
        REFERENCES suppliers(supplier_id)
) ENGINE=InnoDB;

CREATE TABLE stock_entries (
    entry_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    change_quantity INT,
    change_type VARCHAR(50),
    entry_date DATE,
    FOREIGN KEY (product_id)
        REFERENCES products(product_id)
) ENGINE=InnoDB;