# 📦 Inventory Management & Supply Chain Dashboard

A full-stack **database-driven inventory management system** built using **MySQL + Python + Streamlit**, designed to simulate real-world inventory lifecycle operations and business analytics.

---

## 🚀 Project Overview

This project demonstrates how relational database design, SQL business logic, and a Python-based UI can work together to manage and analyze inventory operations.

The system supports:

- Product creation
- Reorder placement
- Reorder receiving
- Inventory lifecycle tracking
- Business KPI dashboard
- Transaction-safe operations using stored procedures

The goal of this project is to showcase practical backend + database + analytics integration skills for data and backend roles.

---

## 🏗️ System Architecture

User (Streamlit UI)  
        ↓  
Python Backend (db_utils.py)  
        ↓  
MySQL Database  
        ↓  
Stored Procedures + Views + Business Queries  

---

## 📂 Project Structure
```
SQL-Database-Operations-UI/
│
├── app/
│   ├── app.py              # Streamlit UI
│   ├── db_utils.py         # Database connection & business logic
│
├── database/
│   ├── schema.sql          # Database schema definition
│   ├── queries.sql         # Business queries & stored procedures
│   └── inventory_management_dump.sql
│
├── screenshots/            # Dashboard screenshots
├── .env                    # Environment variables (ignored in git)
├── .gitignore
├── requirements.txt
└── README.md
```


---

## 🗄️ Database Design

### Core Tables

- **products** – product master data
- **suppliers** – supplier information
- **reorders** – reorder tracking
- **shipments** – shipment records
- **stock_entries** – inventory movement history

### Relationships

- products.supplier_id → suppliers.supplier_id  
- reorders.product_id → products.product_id  
- shipments.product_id → products.product_id  
- stock_entries.product_id → products.product_id  

Foreign keys ensure referential integrity.

---

## 🔄 Inventory Lifecycle Workflow

### 1️⃣ Add Product
- Inserts into `products`
- Inserts shipment record
- Inserts stock entry record

### 2️⃣ Place Reorder
- Inserts new reorder with status `Ordered`
- Uses AUTO_INCREMENT primary key

### 3️⃣ Receive Reorder
- Stored Procedure: `MarkReorderASReceived`
- Updates reorder status to `Received`
- Increases product stock
- Inserts shipment record
- Inserts stock entry record
- Wrapped in a transaction for data consistency

### 4️⃣ Product History
- View: `product_inventory_history`
- Combines shipment + stock movement into unified timeline

---

## 📊 Business KPIs Implemented

Dashboard displays:

- Total Suppliers
- Total Products
- Total Categories
- Total Sales Value (Last 3 Months)
- Total Restock Value (Last 3 Months)
- Below Reorder & No Pending Reorders
- Pending Reorders

All KPI queries:
- Handle NULL safely using `IFNULL`
- Use `CURDATE()` for accurate rolling time windows

---

## 🧠 Advanced SQL Concepts Used

- JOINs
- Subqueries
- Aggregations (SUM, COUNT, DISTINCT)
- IFNULL handling
- DATE_SUB with CURDATE
- Stored Procedures
- Transactions (START TRANSACTION / COMMIT)
- Views
- Foreign Keys
- AUTO_INCREMENT refactoring

---

## 🛠️ Tech Stack

- **Database:** MySQL 8
- **Backend:** Python 3
- **UI Framework:** Streamlit
- **Connector:** mysql-connector-python
- **Environment Management:** python-dotenv
- **Version Control:** Git & GitHub

---

## 🔐 Security & Best Practices

- Database credentials stored in `.env`
- `.env` excluded via `.gitignore`
- Removed manual ID generation logic
- Converted reorder_id to AUTO_INCREMENT
- Transaction handling with rollback protection

---

## ▶️ How to Run
```
### 1️⃣ Install Dependencies
pip install -r requirements.txt

### 2️⃣ Create `.env` file
DB_HOST=localhost

DB_USER=root

DB_PASSWORD=your_password

DB_NAME=inventory_management

### 3️⃣ Run Streamlit
streamlit run app/app.py

```
---

## 📸 Screenshots

(Add dashboard screenshots here)

---

## 🎯 Key Skills Demonstrated

- Relational database design
- End-to-end backend + database integration
- SQL-based business metric development
- Transaction-safe inventory operations
- Full inventory lifecycle modeling
- Streamlit dashboard development
- Clean Git commit history & feature-based versioning

---

## 📈 Future Enhancements

- Record Sale workflow
- Low-stock alert automation
- Role-based authentication
- Deployment to cloud
- Inventory forecasting model

---

## 👨‍💻 Author

**Pratham Mewara**  
Data Analyst | SQL | Python | Power BI