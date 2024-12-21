import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv

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
        print(purchase_data.head())
        print("Data loaded successfully.")
        purchase_data['total_price'] = purchase_data['quantity'] * purchase_data['price_per_unit']
        total_revenue = purchase_data['total_price'].sum()
        print(f"Total Revenue: ${total_revenue}")
        top_products = (
            purchase_data.groupby('product_name')['total_price']
            .sum()
            .sort_values(ascending=False)
            .head(5)
            )
        print("Top Products by Revenue:")
        print(top_products)
        customer_purchases = (
            purchase_data.groupby('customer_name')['id']
            .count()
            .sort_values(ascending=False)
            .head(5)
            )
        print("Top Customers by Purchase Frequency:")
        print(customer_purchases)
        sales_over_time = (
            purchase_data.groupby('purchase_date')['total_price']
            .sum()
            .reset_index()
            )
        print(sales_over_time)


    except Exception as e:
        print(f"Error loading data: {e}")
        return None
