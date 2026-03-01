import streamlit as st
import pandas as pd
from click import option
from streamlit.elements.widgets.radio import T

from db_function import (
connect_to_db,
get_basic_info
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