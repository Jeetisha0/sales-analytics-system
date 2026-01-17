# Task 3.1 (a): Fetch All Products
import requests

def fetch_all_products():
    
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
    
    

# Task 3.1 (b): Create Product Mapping

def create_product_mapping(api_products):

    # Initialize empty dictionary for mapping
    product_mapping = {}

    # Iterate through each product in the API data
    for product in api_products:
        product_id = product.get("id")

        # Only add product if ID is present
        if product_id is not None:
            product_mapping[product_id] = {
                "title": product.get("title"),
                "category": product.get("category"),
                "brand": product.get("brand"),
                "rating": product.get("rating")
            }

    return product_mapping


# Task 3.2: Enrich Sales Data

def enrich_sales_data(transactions, product_mapping):
    """
    Task 3.2
    Enriches cleaned transaction dictionaries with API product information.
    """

    enriched_transactions = []

    for txn in transactions:
        # Copy original transaction
        enriched_txn = txn.copy()

        # Extract numeric product ID (P101 -> 101)
        try:
            numeric_id = int("".join(filter(str.isdigit, txn["product_id"])))
        except ValueError:
            numeric_id = None

        api_product = product_mapping.get(numeric_id)

        if api_product:
            enriched_txn["API_Category"] = api_product.get("category")
            enriched_txn["API_Brand"] = api_product.get("brand")
            enriched_txn["API_Rating"] = api_product.get("rating")
            enriched_txn["API_Match"] = True
        else:
            enriched_txn["API_Category"] = None
            enriched_txn["API_Brand"] = None
            enriched_txn["API_Rating"] = None
            enriched_txn["API_Match"] = False

        enriched_transactions.append(enriched_txn)

    return enriched_transactions

# Task 3.2: Part-2
import os

def save_enriched_data(enriched_transactions, filename="data/enriched_sales_data.txt"):

    # Ensure output directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Define file header with all fields
    header = (
        "TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|"
        "CustomerID|Region|API_Category|API_Brand|API_Rating|API_Match\n"
    )

    # Open file in write mode
    with open(filename, "w", encoding="utf-8") as file:
        # Write header
        file.write(header)

        # Write each enriched transaction
        for tx in enriched_transactions:
            line = (
                f"{tx['TransactionID']}|{tx['Date']}|{tx['ProductID']}|"
                f"{tx['ProductName']}|{tx['Quantity']}|{tx['UnitPrice']}|"
                f"{tx['CustomerID']}|{tx['Region']}|"
                f"{tx['API_Category']}|{tx['API_Brand']}|"
                f"{tx['API_Rating']}|{tx['API_Match']}\n"
            )
            file.write(line)
