# main.py
# Entry point for Sales Analytics System

from utils.file_handler import read_sales_file
from utils.data_processor import (
    parse_transactions,
    validate_and_filter,
    calculate_total_revenue,
    region_wise_sales, top_selling_products,
    customer_analysis, daily_sales_trend,
    peak_sales_day, low_performing_products
)

def main():
    # Task 1.1: Read raw sales data
    raw_lines = read_sales_file("data/sales_data.txt")

    # Task 1.2: Parse and clean transactions
    parsed_transactions = parse_transactions(raw_lines)

    # Task 1.3: Validate transactions
    valid_transactions = validate_and_filter(parsed_transactions)

    # Task 2.1 (a): Total revenue
    total_revenue = calculate_total_revenue(valid_transactions)


    # Task 2.1 (b): Region-wise sales analysis
    region_stats = region_wise_sales(valid_transactions)
    
    
    # Task 2.1 (c): Top selling products
    top_products = top_selling_products(valid_transactions)
    
    
    # Task 2.1 (d): Customer purchase analysis
    customer_stats = customer_analysis(valid_transactions)
   

   # Task 2.2 (a): Daily sales trend
    daily_trend = daily_sales_trend(valid_transactions)
    

    # Task 2.2 (b): Peak sales day
    peak_day = peak_sales_day(valid_transactions)
    
    # Task 2.3: Low performing products
    low_products = low_performing_products(valid_transactions)
    print(low_products)


    #Task 3.1: Fetch product details
    
    from utils.api_handler import fetch_all_products, create_product_mapping, enrich_sales_data 

    def main():
    # (a): Fetch products
     products = fetch_all_products()

    # (b): Create mapping
     product_mapping = create_product_mapping(products)

# Task 3.2: Enrich Sales Data
     # Step 1: Read sales data from file
     transactions = read_sales_file("data/sales_data.txt")

     # Step 2: Fetch products from API
     products = fetch_all_products()

     # Step 3: Create product mapping
     product_mapping = create_product_mapping(products)

     # Step 4: Enrich sales data
     enriched_data = enrich_sales_data(transactions, product_mapping)

 
# TASK 3

from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data,
    save_enriched_data
)

def main():
    
    # Task 3.1: Fetch Product Details
    # (a) Fetch products from API
    products = fetch_all_products()

    # (b) Create product mapping
    product_mapping = create_product_mapping(products)

    # Task 3.2: Enrich Sales Data
    # Read sales data from file
    transactions = read_sales_file("data/sales_data.txt")

    # Enrich sales data using API mapping
    enriched_data = enrich_sales_data(transactions, product_mapping)

    # Save enriched data to file
    save_enriched_data(enriched_data)

# Task 4.1: Generates a comprehensive text report
    from utils.data_processor import generate_sales_report
    generate_sales_report(transactions, enriched_data)


if __name__ == "__main__":
    main()
    



 

