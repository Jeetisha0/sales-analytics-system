# Responsible for safely reading sales data file

import os

def read_sales_file(file_path):
    """
    Reads the sales data file safely handling encoding issues.
    Returns a list of raw data lines .
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    lines = []

    # Try utf-8 first, then fallback to latin-1
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
    except UnicodeDecodeError:
        with open(file_path, "r", encoding="latin-1") as file:
            lines = file.readlines()

    # Remove header and empty lines
    cleaned_lines = []
    for line in lines[1:]:  # skip header
        line = line.strip()
        if line:
            cleaned_lines.append(line)

    return cleaned_lines


# Task 3.1 (a): Fetch All Products
import requests

def fetch_all_products():
    """
    Fetches all products from DummyJSON API.

    Returns:
        A list of dictionaries containing selected product fields.
        Returns an empty list if the API call fails.
    """

    # API endpoint with limit set to 100
    url = "https://dummyjson.com/products?limit=100"

    try:
        # Send GET request to the API
        response = requests.get(url, timeout=10)

        # Raise error if status code is not 200
        response.raise_for_status()

        # Convert response to JSON
        data = response.json()

        # Extract products list
        products = data.get("products", [])

        # List to store cleaned product data
        cleaned_products = []

        for product in products:
            cleaned_products.append({
                "id": product.get("id"),
                "title": product.get("title"),
                "category": product.get("category"),
                "brand": product.get("brand"),
                "price": product.get("price"),
                "rating": product.get("rating")
            })

        print("API products fetched successfully")
        return cleaned_products

    except Exception as error:
        print("Error while fetching products:", error)
        return []
