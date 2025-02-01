import streamlit as st
import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv
import plotly.express as px

# Load environment variables
load_dotenv()

# Fetch Database Credentials
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def load_data_from_postgresql():
    """
    Load data from PostgreSQL database into a Pandas DataFrame.
    """
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        query = "SELECT * FROM purchase;"
        purchase_data = pd.read_sql_query(query, conn)
        conn.close()

        # Calculate total price for each row
        purchase_data['total_price'] = purchase_data['quantity'] * purchase_data['price_per_unit']
        return purchase_data

    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Streamlit app
st.title("Purchase Data Dashboard")

# Load data
data = load_data_from_postgresql()

if data is not None:
    # Display data
    st.subheader("Raw Purchase Data")
    st.dataframe(data)

    # Total revenue
    total_revenue = data['total_price'].sum()
    st.subheader("Total Revenue")
    st.metric(label="Revenue", value=f"${total_revenue:,.2f}")

    # Top products by revenue
    top_products = (
        data.groupby('product_name')['total_price']
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )
    st.subheader("Top Products by Revenue")
    st.bar_chart(top_products)

    # Top customers by purchase frequency
    top_customers = (
        data.groupby('customer_name')['id']
        .count()
        .sort_values(ascending=False)
        .head(5)
    )
    st.subheader("Top Customers by Purchase Frequency")
    st.bar_chart(top_customers)

    # Sales over time
    sales_over_time = (
        data.groupby('purchase_date')['total_price']
        .sum()
        .reset_index()
    )
    st.subheader("Sales Over Time")
    fig = px.line(sales_over_time, x='purchase_date', y='total_price', title='Sales Over Time')
    st.plotly_chart(fig)

else:
    st.warning("No data to display. Please check your database connection.")
