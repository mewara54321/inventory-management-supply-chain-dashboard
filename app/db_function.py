import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            passwd=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        return connection
    except mysql.connector.Error as err:
        print("Database connection failed:", err)
        return None


db = connect_to_db()

if db and db.is_connected():
    print("Database connected successfully")

cursor = db.cursor(dictionary=True)

print(cursor) #agent name

def get_basic_info(cursor):
    queries = {
        "Total Suppliers": "SELECT COUNT(*) AS count FROM suppliers",

        "Total Products": "SELECT COUNT(*) AS count FROM products",

        "Total Categories Dealing": "SELECT COUNT(DISTINCT category) AS count FROM products",

        "Total Sale Value (Last 3 Months)": """
        SELECT ROUND(SUM(ABS(se.change_quantity) * p.price), 2) AS total_sale
        FROM stock_entries se
        JOIN products p ON se.product_id = p.product_id
        WHERE se.change_type = 'Sale'
        AND se.entry_date >= (
        SELECT DATE_SUB(MAX(entry_date), INTERVAL 3 MONTH) FROM stock_entries)
        """,

        "Total Restock Value (Last 3 Months)": """
        SELECT ROUND(SUM(se.change_quantity * p.price), 2) AS total_restock
        FROM stock_entries se
        JOIN products p ON se.product_id = p.product_id
        WHERE se.change_type = 'Restock'
        AND se.entry_date >= (
        SELECT DATE_SUB(MAX(entry_date), INTERVAL 3 MONTH) FROM stock_entries)
        """,

        "Below Reorder & No Pending Reorders": """
        SELECT COUNT(*) AS below_reorder
        FROM products p
        WHERE p.stock_quantity < p.reorder_level
        AND p.product_id NOT IN (
        SELECT DISTINCT product_id FROM reorders WHERE status = 'Pending')
        """
    }

    result = {}
    for label, query in queries.items():
        cursor.execute(query)
        row = cursor.fetchone()
        result[label] = list(row.values())[0]

    return result



def get_additional_tables(cursor):
    queries = {
        "Suppliers Contact Details": "SELECT supplier_name, contact_name, email, phone FROM suppliers;",

        "Products with Supplier and Stock": """
            SELECT 
                p.product_name,
                s.supplier_name,
                p.stock_quantity,
                p.reorder_level
            FROM products p
            JOIN suppliers s ON p.supplier_id = s.supplier_id
            ORDER BY p.product_name ASC;
        """,

        "Products Needing Reorder": """
            SELECT product_name, stock_quantity, reorder_level
            FROM products
            WHERE stock_quantity <= reorder_level;
        """
    }

    tables = {}
    for label, query in queries.items():
        cursor.execute(query)
        tables[label] = cursor.fetchall()

    return tables





def add_new_manual_id(cursor,db,p_name ,p_category ,p_price ,p_stock ,p_reorder , p_supplier):    #db isle ya bhej rha hun kyu ki database mai changes karna rha hun
    proc_call = "call ADDNewProductManualID(%s ,%s ,%s ,%s ,%s ,%s )"
    params = (p_name ,p_category ,p_price ,p_stock ,p_reorder , p_supplier)
    cursor.execute(proc_call, params)
    db.commit()

def get_categories(cursor):
    cursor.execute("SELECT DISTINCT category FROM products  order by category asc ")
    rows = cursor.fetchall()
    return [row["category"] for row in rows]


def get_suppliers(cursor):
    cursor.execute("select supplier_id ,supplier_name from suppliers  order by supplier_id asc ")
    rows = cursor.fetchall()
    return  rows



