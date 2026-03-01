-- ============================================
-- INVENTORY MANAGEMENT SYSTEM - SQL QUERIES
-- Project: Python Driven UI for SQL Operations
-- Author: Pratham mewara
-- ============================================

USE inventory_management;

select * from products;
select * from reorders;
select * from shipments;
select * from stock_entries;
select* from suppliers;

-- 1)Total Suppliers -:
SELECT 
    COUNT(*) AS total_suppliers
FROM
    suppliers;
 
 
-- 2)Total Products -:
SELECT 
    COUNT(*) AS total_products
FROM
    products;


-- 3)Total categories dealing -:
SELECT 
    COUNT(DISTINCT (category)) AS total_categories
FROM
    products;
    

-- 4)Total sales value made in last 3 month -:

 
