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

    enriched_transactions = []

    # Process each transaction line
    for line in transactions:
        # Split transaction fields
        fields = line.split("|")

        # Create base transaction dictionary
        transaction = {
            "TransactionID": fields[0],
            "Date": fields[1],
            "ProductID": fields[2],
            "ProductName": fields[3],
            "Quantity": fields[4],
            "UnitPrice": fields[5],
            "CustomerID": fields[6],
            "Region": fields[7]
        }

        # Extract numeric product ID (P101 -> 101)
        try:
            numeric_id = int("".join(filter(str.isdigit, transaction["ProductID"])))
        except ValueError:
            numeric_id = None

        # Check if product exists in API mapping
        api_product = product_mapping.get(numeric_id)

        if api_product:
            transaction["API_Category"] = api_product.get("category")
            transaction["API_Brand"] = api_product.get("brand")
            transaction["API_Rating"] = api_product.get("rating")
            transaction["API_Match"] = True
        else:
            transaction["API_Category"] = None
            transaction["API_Brand"] = None
            transaction["API_Rating"] = None
            transaction["API_Match"] = False

        enriched_transactions.append(transaction)

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
