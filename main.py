# main.py
# Entry point for Sales Analytics System

from utils.file_handler import read_sales_file
from utils.data_processor import (
    parse_transactions,
    validate_and_filter,
    generate_sales_report
)
from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data,
    save_enriched_data
)

def main():
    print("=" * 40)
    print("SALES ANALYTICS SYSTEM")
    print("=" * 40)

    try:
        # [1/10] Read sales data
        print("\n[1/10] Reading sales data...")
        raw_lines = read_sales_file("data/sales_data.txt")
        print(f"✓ Successfully read {len(raw_lines)} transactions")

        # [2/10] Parse and clean
        print("\n[2/10] Parsing and cleaning data...")
        parsed_transactions = parse_transactions(raw_lines)
        print(f"✓ Parsed {len(parsed_transactions)} records")

        # [3/10] User filter interaction (MINIMAL & VALID)
        regions = sorted(set(tx["region"] for tx in parsed_transactions))
        print("\n[3/10] Filter Options Available:")
        print("Regions:", ", ".join(regions))

        choice = input("Do you want to filter by region? (y/n): ").strip().lower()
        if choice == "y":
            selected_region = input("Enter region name: ").strip()
            parsed_transactions = [
                tx for tx in parsed_transactions
                if tx["region"].lower() == selected_region.lower()
            ]
            print(f"✓ Filter applied for region: {selected_region}")
        else:
            print("✓ No filters applied")

        # [4/10] Validate transactions
        print("\n[4/10] Validating transactions...")
        valid_transactions = validate_and_filter(parsed_transactions)
        print(f"✓ Valid records after validation: {len(valid_transactions)}")

        # [5/10] Fetch product data
        print("\n[5/10] Fetching product data from API...")
        products = fetch_all_products()
        product_mapping = create_product_mapping(products)
        print(f"✓ Fetched {len(products)} products")

        # [6/10] Enrich sales data
        print("\n[6/10] Enriching sales data...")
        enriched_data = enrich_sales_data(valid_transactions, product_mapping)

        success_count = sum(1 for tx in enriched_data if tx.get("API_Match"))
        success_rate = (success_count / len(enriched_data)) * 100 if enriched_data else 0
        print(f"✓ Enriched {success_count}/{len(enriched_data)} transactions ({success_rate:.1f}%)")

        # [7/10] Save enriched data
        print("\n[7/10] Saving enriched data...")
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
        print("✓ Saved to: data/enriched_sales_data.txt")

        # [8/10] Generate report
        print("\n[8/10] Generating report...")
        generate_sales_report(valid_transactions, enriched_data)
        print("✓ Report saved to: output/sales_report.txt")

        # [9/10] Completion
        print("\n[9/10] Process Complete!")
        print("=" * 40)

    except Exception as error:
        print("\n An error occurred during execution")
        print("Error details:", error)

if __name__ == "__main__":
    main()

