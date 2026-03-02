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


-- 7)Suppliers and their contact details
SELECT 
    supplier_name, contact_name, email, phone
FROM
    suppliers;
    
    
-- 8)Product with their suppliers and current stock
SELECT 
    p.product_name,
    s.supplier_name,
    p.stock_quantity,
    p.reorder_level
FROM
    products AS p
        JOIN
    suppliers AS s ON p.supplier_id = s.supplier_id
ORDER BY p.product_name ASC;


-- 9)Product needing reorder
SELECT 
    product_id, product_name, stock_quantity, reorder_level
FROM
    products
WHERE
    stock_quantity < reorder_level;



-- 10)Add an new product to the databse
DELIMITER $$

CREATE PROCEDURE AddNewProductManualID
(
    IN p_name VARCHAR(255),
    IN p_category VARCHAR(100),
    IN p_price DECIMAL(10,2),
    IN p_stock INT,
    IN p_reorder INT,
    IN p_supplier INT
)
BEGIN

    DECLARE new_prod_id INT;
    DECLARE new_shipment_id INT;
    DECLARE new_entry_id INT;

    -- Generate product_id
    SELECT IFNULL(MAX(product_id),0) + 1 INTO new_prod_id FROM products;

    INSERT INTO products
    (product_id, product_name, category, price,
     stock_quantity, reorder_level, supplier_id)
    VALUES
    (new_prod_id, p_name, p_category, p_price,
     p_stock, p_reorder, p_supplier);

    -- Generate shipment_id
    SELECT IFNULL(MAX(shipment_id),0) + 1 INTO new_shipment_id FROM shipments;

    INSERT INTO shipments
    (shipment_id, product_id, supplier_id,
     quantity_received, shipment_date)
    VALUES
    (new_shipment_id, new_prod_id, p_supplier,
     p_stock, CURDATE());

    -- Generate entry_id
    SELECT IFNULL(MAX(entry_id),0) + 1 INTO new_entry_id FROM stock_entries;

    INSERT INTO stock_entries
    (entry_id, product_id, change_quantity,
     change_type, entry_date)
    VALUES
    (new_entry_id, new_prod_id, p_stock,
     'Restock', CURDATE());

END $$

DELIMITER ;


-- 11)Product history ,[finding shipment , sales ,purchase]
CREATE OR REPLACE VIEW product_inventory_history AS
    SELECT 
        pih.product_id,
        pih.record_type,
        pih.record_date,
        pih.quantity,
        pih.change_type,
        pr.supplier_id
    FROM
        (SELECT 
                 product_id,
                'Shipment' AS record_type,
                shipment_date AS record_date,
                quantity_received AS Quantity,
                NULL change_type
        FROM
            shipments UNION ALL 
            SELECT 
                 product_id,
                'Shipment' AS record_type,
                entry_date AS record_date,
                change_quantity AS Quantity,
                change_type
        FROM
            stock_entries) pih
            JOIN
        products pr ON pr.product_id = pih.product_id;


-- 12)Place an reorder
INSERT INTO reorders
(reorder_id, product_id, reorder_quantity, reorder_date, status)
SELECT 
    IFNULL(MAX(reorder_id),0) + 1,
    101,
    200,
    CURDATE(),
    'Ordered'
FROM reorders;


-- 13)Receive reorder
delimiter $$ 
create procedure MarkReorderASReceived( in in_reorder_id int)
begin 
declare prod_id int ,
declare qty int ,
declare sup_id int ,
declare new_shipment_id int ,
declare new_entry_id int ;

start Transaction;
# get producgt_id ,quantity from reorders 
Select product_Id , reorder_quantity 
into product_id ,qty
from reorders
where reorder_id = in_reorder_id ;

#Get supplier_id from products
select supplier_id 
into sup_id
from products 
where product_Id = prod_id;

#update reorder table -- received 
update reorders 
set status = "Received"
where reorder_id = in_reorder_id;

#update quantity in product table 
update products 
set stock_quantity = stock_quantity+qty 
where product_id = prod_Id;

#insert record into shipment table 
select max(shipment_id)+1 into new_shipment_id from shipments ;
insert into shipments(shipment_id , product_id ,suppplier_id , quantity_received , shipment_date)
values (new_shipment_id ,prod_id ,sup_id ,qty ,curdate());

#insert record into restock 
select max(entry_id) +1 into new_shipment_id from stock_entries;
insert into stock_entries(entry_id , product_id , change_quantity , change_type , entry_date)
values (new_entry_id ,prod_id ,qty ,"Restok",curdate());

commit;
end $$ 

DELIMITER ;





