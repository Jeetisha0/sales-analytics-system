# main.py
# Entry point for Sales Analytics System

from utils.file_handler import read_sales_file
from utils.data_processor import (
    parse_transactions,
    validate_and_filter,
    calculate_total_revenue
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

    # Output for validation
    print(total_revenue)

if __name__ == "__main__":
    main()
