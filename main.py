# main.py
# Entry point for Sales Analytics System

from utils.file_handler import read_sales_file

# Task 1 & 2
from utils.data_processor import (
    parse_transactions,
    validate_and_filter,
    generate_sales_report
)

# Task 3
from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data,
    save_enriched_data
)

def main():
   
    # Task 1: Read, parse, validate
  
    raw_lines = read_sales_file("data/sales_data.txt")
    parsed_transactions = parse_transactions(raw_lines)
    valid_transactions = validate_and_filter(parsed_transactions)

    
    # Task 3: API Integration
    
    products = fetch_all_products()
    product_mapping = create_product_mapping(products)

    enriched_data = enrich_sales_data(valid_transactions, product_mapping)

    
    # FORMAT DATA FOR TASK 3.2 OUTPUT 
  
    formatted_enriched_data = []

    for tx in enriched_data:
     formatted_enriched_data.append({
        "TransactionID": tx["transaction_id"],
        "Date": tx["date"],
        "ProductID": tx["product_id"],
        "ProductName": tx["product_name"],
        "Quantity": tx["quantity"],
        "UnitPrice": tx["price"],  
        "CustomerID": tx["customer_id"],
        "Region": tx["region"],
        "API_Category": tx.get("API_Category"),
        "API_Brand": tx.get("API_Brand"),
        "API_Rating": tx.get("API_Rating"),
        "API_Match": tx.get("API_Match")
    })


    save_enriched_data(formatted_enriched_data)

  
    # Task 4: Report Generation
    
    generate_sales_report(valid_transactions, enriched_data)

    print("All tasks completed successfully.")

if __name__ == "__main__":
    main()

 

