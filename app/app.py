import streamlit as st
import pandas as pd
from click import option
from numpy.ma.core import product
from pandas.core.methods.describe import reorder_columns
from streamlit.elements.widgets.radio import T

from db_function import (
connect_to_db,
get_basic_info,
get_additional_tables,
add_new_manual_id ,
get_categories ,
get_suppliers,
get_product_history,
get_all_products,
place_reorder,
get_pending_reorders,
mark_reorder_as_received
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


    if selected_task == "Product History":
        st.header("Product Inventory History")

        #get Product list
        products =get_all_products(cursor)
        product_names=[p['product_name'] for p in products]
        product_ids =[p['product_id'] for p in products]

        selected_product_name  = st.selectbox("Select Product",options=product_names)

        if selected_product_name:
            selected_product_id = product_ids[product_names.index(selected_product_name)]
            history_data = get_product_history(cursor, selected_product_id)

            if history_data:
                df = pd.DataFrame(history_data)
                st.dataframe(df, use_container_width=True)

            else:
                st.info("Product History Not Found")


    if selected_task == "Place Reorder":
        st.header("Place an Reorder")

        # get Product list
        products = get_all_products(cursor)
        product_names = [p['product_name'] for p in products]
        product_ids = [p['product_id'] for p in products]

        selected_product_name = st.selectbox("Select Product", options=product_names)

        reorder_qty = st.number_input("Reorder Qty", min_value=1, step=1)

        if st.button("Place Reorder"):
            if not selected_product_name:
                st.error("Product Name is required")

            elif reorder_qty<=0:
                st.error("Reorder Qty is required")

            else:
                selected_product_id = product_ids[product_names.index(selected_product_name)]
                try:
                    place_reorder(cursor, db , selected_product_id , reorder_qty)
                    st.success(f"Product {selected_product_name} with quantity {reorder_qty} Placed Successfully")

                except Exception as e:
                    st.error(f"Error: {e}")

    elif selected_task == "Receive Reorder":
        st.header("Receive Reorder")
        #fetch orders in orders stage
        pending_reorders = get_pending_reorders(cursor)
        if not pending_reorders:
            st.info("NO Pendng orders to receive")

        else:
            reorder_ids = [r['reorder_id'] for r in pending_reorders]
            reorder_labels =[f"ID {r['reorder_id']} -{r['product_name']}" for r in pending_reorders]

            selected_label = st.selectbox("Select Reorder",options=reorder_labels)
            if selected_label:
                selected_reorder_id = reorder_ids[reorder_labels.index(selected_label)]


                if st.button("Mark as Received"):
                    try:
                        mark_reorder_as_received(cursor, db , selected_reorder_id )
                        st.success(f"Reorder Received Successfully")

                    except Exception as e:
                        st.error(f"Error: {e}")










