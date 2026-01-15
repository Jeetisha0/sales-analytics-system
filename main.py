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

 
 


if __name__ == "__main__":
    main()

