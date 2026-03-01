-- ============================================
-- INVENTORY MANAGEMENT SYSTEM - SQL QUERIES
-- Project: Python Driven UI for SQL Operations
-- Author: Pratham mewara
-- ============================================

USE inventory_management;

-- ============================================
-- BASIC DATA VIEWING
-- ============================================
select * from products;
select * from reorders;
select * from shipments;
select * from stock_entries;
select* from suppliers;

-- ============================================
-- BUSINESS METRICS
-- ============================================

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
    

-- 4)Total sales value made in last 3 month (quantiy * price) -:
SELECT 
    ROUND(SUM(ABS(se.change_quantity) * p.price),
            2) AS total_sales_value_last_3_month
FROM
    stock_entries AS se
        JOIN
    products AS p ON p.product_id = se.product_id
WHERE
    se.change_type = 'Sale'
        AND se.entry_date >= (SELECT 
            DATE_SUB(MAX(entry_date),
                    INTERVAL 3 MONTH)
        FROM
            stock_entries);
            

-- 5)Total restock value made in last 3 month (quantiy * price) -:
SELECT 
    ROUND(SUM(ABS(se.change_quantity) * p.price),
            2) AS total_sales_value_last_3_month
FROM
    stock_entries AS se
        JOIN
    products AS p ON p.product_id = se.product_id
WHERE
    se.change_type = 'Restock'
        AND se.entry_date >= (SELECT 
            DATE_SUB(MAX(entry_date),
                    INTERVAL 3 MONTH)
        FROM
            stock_entries);
            
            
-- 6)Below reorder & NO pending reorders
SELECT 
    COUNT(*) AS products_needing_reorder
FROM
    products AS p
WHERE
    p.stock_quantity < p.reorder_level
        AND product_id NOT IN (SELECT DISTINCT
            (product_id)
        FROM
            reorders
        WHERE
            status = 'Pending');
