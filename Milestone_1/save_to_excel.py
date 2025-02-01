import requests
import json
import os
import pandas as pd

# Your NASDAQ Data Link API key and endpoint
API_KEY = "Your API Key "
URL = "https://data.nasdaq.com/api/v3/datatables/QUOTEMEDIA/PRICES.json?api_key=8yUvt6m1xCBamwWoQsUb"

# Directory for local storage
excel_dir = "excel_storage"
os.makedirs(excel_dir, exist_ok=True)

try:
    # Fetch data from the API
    response = requests.get(URL)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse JSON response
        data = response.json()

        # Check if the required fields exist
        if "datatable" in data and "data" in data["datatable"] and "columns" in data["datatable"]:
            rows = data["datatable"]["data"]
            columns = [col["name"] for col in data["datatable"]["columns"]]

            # Create a Pandas DataFrame
            df = pd.DataFrame(rows, columns=columns)

            # Save DataFrame to an Excel file
            excel_file_path = os.path.join(excel_dir, "nasdaq_data.xlsx")
            df.to_excel(excel_file_path, index=False)
            print(f"Data saved successfully to {excel_file_path}")
        else:
            print("Invalid data structure in the JSON response.")
    else:
        print(f"Failed to fetch data. HTTP Status Code: {response.status_code}")
        print("Response:", response.text)

except Exception as e:
    print("An error occurred:", e)
