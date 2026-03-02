import streamlit as st
import pandas as pd
from click import option
from numpy.ma.core import product
from streamlit.elements.widgets.radio import T

from db_function import (
connect_to_db,
get_basic_info,
get_additional_tables,
add_new_manual_id ,
get_categories ,
get_suppliers
)

st.set_page_config(page_title="Inventory Dashboard", layout="wide")

#sidebar
st.sidebar.title("Inventory Management Dashboard")
option = st.sidebar.radio("Select Option:",["Basic Information" , "Operational Tasks"])  #button click kar tha hai


#main space
st.title("Inventory and Supply chain Dashboard")
db = connect_to_db()
cursor = db.cursor(dictionary=True)



# -----------------------------------------------BASIC INFORMATION PAGE------------------------------------------------
if option == "Basic Information":
    st.header("Basic Metrics")

    #get basic information from data base
    basic_info = get_basic_info(cursor)

    cols = st.columns(3)
    keys = list(basic_info.keys())

    for i in range (3):
        cols[i].metric(label=keys[i],value=basic_info[keys[i]])


    cols = st.columns(3)
    for i in range (3,6):
        cols[i-3].metric(label=keys[i],value=basic_info[keys[i]])


    st.divider()

    #fetch and display detailed tables
    tables = get_additional_tables(cursor)
    for labels , data in tables.items():
        st.header(labels)
        df = pd.DataFrame(data)
        st.dataframe(df)
        st.divider()

# -----------------------------------------------OPERATIONAL TASKS PAGE------------------------------------------------
elif option == "Operational Tasks":
    st.header("Operational Tasks")
    selected_task = st.selectbox("Choose an Task" , ["Add New Product" ,"Product History" ,"Place Reorder" , "Receive Reorder"])
    if selected_task == "Add New Product":
        st.header("Add New Product")
        categories = get_categories(cursor)
        suppliers = get_suppliers(cursor)

        with st.form("Add_Product_Form"):
            product_name = st.text_input("Product Name")
            product_category = st.selectbox("Select Category",categories)
            product_price = st.number_input("Product Price" ,min_value=0.00)
            product_stock = st.number_input("Product Stock" ,min_value=0 , step=1)
            product_level = st.number_input("Reorder level", min_value=0, step=1)

            supplier_ids = [s["supplier_id"] for s in suppliers]
            supplier_names = [s["supplier_name"] for s in suppliers]

            supplier_id = st.selectbox(
                "Supplier",
                options=supplier_ids,
                format_func=lambda x: supplier_names[supplier_ids.index(x)]

            )

            submitted = st.form_submit_button("Add New Product")
            if submitted:
                if not product_name:
                    st.error("Product Name is required")

                else:
                    try:
                        add_new_manual_id(cursor, db , product_name , product_category , product_price , product_stock , product_level , supplier_id )
                        st.success(f"Product {product_name} Added Successfully")

                    except Exception as e:
                        st.error(f"Error: {e}")



