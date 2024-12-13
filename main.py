import requests
import json
import os

# Your NASDAQ Data Link API key and endpoint
API_KEY = "hkcDRsMpULNu7-9NPPdV"
URL = "https://data.nasdaq.com/api/v3/datatables/QUOTEMEDIA/PRICES.json?api_key=8yUvt6m1xCBamwWoQsUb"

# Directory for local JSON storage
local_dir = "data_storage"
os.makedirs(local_dir, exist_ok=True)

try:
    # Fetch data from the API
    response = requests.get(URL)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse JSON response
        data = response.json()

        # Save JSON to local storage
        json_file_path = os.path.join(local_dir, "nasdaq_data.json")
        with open(json_file_path, "w") as file:
            json.dump(data, file, indent=4)
        print(f"Data saved successfully to {json_file_path}")
    else:
        print(f"Failed to fetch data. HTTP Status Code: {response.status_code}")
        print("Response:", response.text)

except Exception as e:
    print("An error occurred:", e)