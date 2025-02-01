import os
import requests
import pandas as pd
import psycopg2
import json
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Fetch API Key and Database Credentials
API_KEY = os.getenv("API_KEY")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# API URL
BASE_URL = "https://data.nasdaq.com/api/v3/datatables/QUOTEMEDIA/PRICES.json"


def fetch_data():
    """
    Fetch data from the Nasdaq API.
    """
    try:
        # Construct the URL with API key
        url = f"{BASE_URL}?api_key={API_KEY}"
        response = requests.get(url)
        response.raise_for_status()

        # Parse JSON response
        data = response.json()
        if "datatable" in data and "data" in data["datatable"] and "columns" in data["datatable"]:
            rows = data["datatable"]["data"]
            columns = [col["name"] for col in data["datatable"]["columns"]]

            # Create and return a Pandas DataFrame
            df = pd.DataFrame(rows, columns=columns)
            print("Data fetched successfully.")
            return df
        else:
            print("Invalid data structure in the JSON response.")
            return None
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None


def save_to_json(df, file_path="data/nasdaq_data.json"):
    """
    Save the DataFrame to a JSON file.
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        df.to_json(file_path, orient="records", indent=4)
        print(f"Data saved to JSON file at '{file_path}'.")
        return file_path
    except Exception as e:
        print(f"Error saving data to JSON: {e}")
        return None


def save_to_postgresql(json_file_path):
    """
    Save data from the JSON file to PostgreSQL.
    """
    try:
        # Load data from JSON
        with open(json_file_path, "r") as file:
            data = json.load(file)

        # Connect to PostgreSQL
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()

        # Create table query
        table_name = "nasdaq_data"
        if data:
            columns = ", ".join([f"{key} TEXT" for key in data[0].keys()])  # Adjust data types as needed
            create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns});"
            cursor.execute(create_table_query)
            print(f"Table '{table_name}' created or already exists.")

            # Insert data query
            for row in data:
                placeholders = ", ".join(["%s"] * len(row))
                insert_query = f"INSERT INTO {table_name} VALUES ({placeholders})"
                cursor.execute(insert_query, tuple(row.values()))

        # Commit and close connection
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Data saved to PostgreSQL table '{table_name}'.")
    except Exception as e:
        print(f"Error saving data to PostgreSQL: {e}")


def main():
    """
    Main function to fetch data, save to JSON, and store in PostgreSQL.
    """
    # Fetch data from API
    df = fetch_data()
    if df is not None:
        # Save data to JSON file
        json_file_path = save_to_json(df)
        if json_file_path:
            # Save data to PostgreSQL
            save_to_postgresql(json_file_path)


if __name__ == "__main__":
    main()
