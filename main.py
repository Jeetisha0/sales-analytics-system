# main.py
# Entry point for Sales Analytics System

from utils.file_handler import read_sales_file
from utils.data_processor import process_sales_data

def main():
    file_path = "data/sales_data.txt"

    # Step 1: Read file
    raw_lines = read_sales_file(file_path)

    # Step 2: Clean and validate data
    cleaned_data = process_sales_data(raw_lines)

    # Just confirmation message
    print("Data cleaning and validation completed.")

if __name__ == "__main__":
    main()

from utils.file_handler import read_sales_file
from utils.data_processor import parse_transactions, validate_and_filter

raw = read_sales_file("data/sales_data.txt")
parsed = parse_transactions(raw)

valid, invalid_count, summary = validate_and_filter(parsed)

print(summary)

