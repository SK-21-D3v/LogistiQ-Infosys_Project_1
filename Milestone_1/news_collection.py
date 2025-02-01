import requests
import psycopg2
from psycopg2 import sql
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# NewsAPI Configuration
NEWS_API_KEY = os.getenv("NEWS_API_KEY")  # Fetch from .env file
NEWS_API_URL = "https://newsapi.org/v2/everything"
SEARCH_QUERY = "electronics risk factors"

# PostgreSQL Configuration
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),      # Fetch from .env file
    "user": os.getenv("DB_USER"),        # Fetch from .env file
    "password": os.getenv("DB_PASSWORD"),# Fetch from .env file
    "host": os.getenv("DB_HOST", "localhost"),  # Default to localhost if not set
    "port": os.getenv("DB_PORT", 5432)   # Default to 5432 if not set
}

def fetch_supply_chain_news():
    """Fetch supply chain news from NewsAPI."""
    params = {
        "q": SEARCH_QUERY,
        "apiKey": NEWS_API_KEY,
        "pageSize": 20,  # Adjust the number of results as needed
        "language": "en"
    }
    response = requests.get(NEWS_API_URL, params=params)
    if response.status_code == 200:
        return response.json().get("articles", [])
    else:
        raise Exception(f"Error fetching news: {response.status_code}, {response.text}")

def store_news_in_db(articles):
    """Store news articles in PostgreSQL."""
    try:
        # Connect to PostgreSQL
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # Check if the table exists; if not, create it
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS electronics_news (
                id SERIAL PRIMARY KEY,
                title TEXT,
                description TEXT,
                url TEXT,
                published_at TIMESTAMP
            );
        """)
        connection.commit()

        # Insert articles into the database
        insert_query = sql.SQL("""
            INSERT INTO electronics_news (title, description, url, published_at)
            VALUES (%s, %s, %s, %s)
        """)
        for article in articles:
            title = article.get("title", "No Title")
            description = article.get("description", "No Description")
            url = article.get("url", "No URL")
            published_at = article.get("publishedAt")
            if published_at:
                published_at = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ")

            cursor.execute(insert_query, (title, description, url, published_at))

        # Commit changes
        connection.commit()
        print(f"{cursor.rowcount} articles inserted successfully.")

    except psycopg2.Error as e:
        print(f"Database error: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    try:
        print("Fetching supply chain news...")
        articles = fetch_supply_chain_news()
        if articles:
            print(f"Fetched {len(articles)} articles.")
            print("Storing news in the database...")
            store_news_in_db(articles)
        else:
            print("No articles found.")
    except Exception as e:
        print(f"Error: {e}")
