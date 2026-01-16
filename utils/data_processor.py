# Cleans and validates sales data

def process_sales_data(raw_lines):
    total_records = len(raw_lines)
    invalid_records = 0
    valid_records = []

    for line in raw_lines:
        parts = line.split("|")

        # If row does not have 8 fields, skip
        if len(parts) != 8:
            invalid_records += 1
            continue

        transaction_id = parts[0]
        date = parts[1]
        product_id = parts[2]
        product_name = parts[3]
        quantity = parts[4]
        unit_price = parts[5]
        customer_id = parts[6]
        region = parts[7]

        # Validation rules
        if not transaction_id.startswith("T"):
            invalid_records += 1
            continue

        if customer_id.strip() == "" or region.strip() == "":
            invalid_records += 1
            continue

        # Cleaning
        product_name = product_name.replace(",", "")
        quantity = quantity.replace(",", "")
        unit_price = unit_price.replace(",", "")

        try:
            quantity = int(quantity)
            unit_price = float(unit_price)
        except:
            invalid_records += 1
            continue

        if quantity <= 0 or unit_price <= 0:
            invalid_records += 1
            continue

        # Valid record
        valid_records.append({
            "transaction_id": transaction_id,
            "date": date,
            "product_id": product_id,
            "product_name": product_name,
            "quantity": quantity,
            "unit_price": unit_price,
            "customer_id": customer_id,
            "region": region
        })

    # Mandatory output
    print(f"Total records parsed: {total_records}")
    print(f"Invalid records removed: {invalid_records}")
    print(f"Valid records after cleaning: {len(valid_records)}")

    return valid_records

# Task 1.2: Parse and clean transactions

def parse_transactions(raw_lines):
    cleaned_transactions = []

    for line in raw_lines:
        parts = line.split("|")

        # Skip rows with incorrect number of fields
        if len(parts) != 8:
            continue

        transaction_id = parts[0]
        date = parts[1]
        product_id = parts[2]
        product_name = parts[3].replace(",", "").strip()
        quantity = parts[4].replace(",", "")
        unit_price = parts[5].replace(",", "")
        customer_id = parts[6]
        region = parts[7]

        try:
            quantity = int(quantity)
            unit_price = float(unit_price)
        except:
            continue

        cleaned_transactions.append({
    "transaction_id": transaction_id,
    "date": date,
    "product_id": product_id,
    "product_name": product_name,
    "quantity": quantity,
    "price": unit_price,
    "customer_id": customer_id,
    "region": region
})

    return cleaned_transactions

# Task 1.3: Validate and filter transactions
def validate_and_filter(transactions):
    valid_transactions = []

    for txn in transactions:
        if (
            txn["quantity"] > 0
            and txn["price"] > 0
            and txn["region"].strip() != ""
        ):
            valid_transactions.append(txn)

    return valid_transactions


# Task 2.1: Sales Summary Calculator
# (a): Calculate total revenue
def calculate_total_revenue(transactions):
    total_revenue = 0

    for txn in transactions:
        total_revenue += txn["quantity"] * txn["price"]

    return total_revenue

# (b): Region-wise sales analysis
def region_wise_sales(transactions):
    """
    Analyzes sales by region
    """

    region_data = {}
    overall_sales = 0

    # Calculate total sales and transaction count per region
    for txn in transactions:
        region = txn["region"]
        sale_amount = txn["quantity"] * txn["price"]

        overall_sales += sale_amount

        if region not in region_data:
            region_data[region] = {
                "total_sales": 0,
                "transaction_count": 0
            }

        region_data[region]["total_sales"] += sale_amount
        region_data[region]["transaction_count"] += 1

    # Calculate percentage contribution
    for region in region_data:
        region_data[region]["percentage"] = round(
            (region_data[region]["total_sales"] / overall_sales) * 100, 2
        )

    # Sort by total_sales (descending)
    sorted_region_data = dict(
        sorted(
            region_data.items(),
            key=lambda item: item[1]["total_sales"],
            reverse=True
        )
    )

    return sorted_region_data

# (c): Top selling products
def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold
    """

    product_data = {}

    # Aggregate quantity and revenue by product_name
    for txn in transactions:
        product = txn["product_name"]
        quantity = txn["quantity"]
        revenue = txn["quantity"] * txn["price"]

        if product not in product_data:
            product_data[product] = {
                "total_quantity": 0,
                "total_revenue": 0
            }

        product_data[product]["total_quantity"] += quantity
        product_data[product]["total_revenue"] += revenue

    # Convert to list of tuples
    result = []
    for product, values in product_data.items():
        result.append(
            (product, values["total_quantity"], values["total_revenue"])
        )

    # Sort by total quantity sold (descending)
    result.sort(key=lambda x: x[1], reverse=True)

    # Return top n products
    return result[:n]

# (d): Customer purchase analysis
def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns
    """

    customer_data = {}

    # Aggregate data per customer
    for txn in transactions:
        customer = txn["customer_id"]
        product = txn["product_name"]
        amount = txn["quantity"] * txn["price"]

        if customer not in customer_data:
            customer_data[customer] = {
                "total_spent": 0,
                "purchase_count": 0,
                "products_bought": set()
            }

        customer_data[customer]["total_spent"] += amount
        customer_data[customer]["purchase_count"] += 1
        customer_data[customer]["products_bought"].add(product)

    # Calculate average order value and format output
    result = {}

    for customer, data in customer_data.items():
        avg_order_value = data["total_spent"] / data["purchase_count"]

        result[customer] = {
            "total_spent": round(data["total_spent"], 2),
            "purchase_count": data["purchase_count"],
            "avg_order_value": round(avg_order_value, 2),
            "products_bought": list(data["products_bought"])
        }

    # Sort by total_spent (descending)
    sorted_result = dict(
        sorted(
            result.items(),
            key=lambda item: item[1]["total_spent"],
            reverse=True
        )
    )

    return sorted_result

# Task 2.2 (a): Daily sales trend
def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date
    """

    daily_data = {}

    # Group by date
    for txn in transactions:
        date = txn["date"]
        revenue = txn["quantity"] * txn["price"]
        customer = txn["customer_id"]

        if date not in daily_data:
            daily_data[date] = {
                "revenue": 0,
                "transaction_count": 0,
                "customers": set()
            }

        daily_data[date]["revenue"] += revenue
        daily_data[date]["transaction_count"] += 1
        daily_data[date]["customers"].add(customer)

    # Prepare final output
    result = {}
    for date in daily_data:
        result[date] = {
            "revenue": round(daily_data[date]["revenue"], 2),
            "transaction_count": daily_data[date]["transaction_count"],
            "unique_customers": len(daily_data[date]["customers"])
        }

    # Sort chronologically by date
    sorted_result = dict(sorted(result.items()))

    return sorted_result

# Task 2.2 (b): Peak sales day
def peak_sales_day(transactions):
    """
    Identifies the day with the highest total revenue
    """

    daily_revenue = {}

    # Aggregate revenue by date
    for txn in transactions:
        date = txn["date"]
        revenue = txn["quantity"] * txn["price"]

        if date not in daily_revenue:
            daily_revenue[date] = 0

        daily_revenue[date] += revenue

    # Find peak sales day
    peak_day = max(daily_revenue, key=daily_revenue.get)

    return {
        "date": peak_day,
        "revenue": round(daily_revenue[peak_day], 2)
    }


# Task 2.3: Low performing products
def low_performing_products(transactions, threshold=10):
    """
    Identifies products with low sales
    """

    product_summary = {}

    # Aggregate quantity and revenue by product
    for txn in transactions:
        product = txn["product_name"]
        quantity = txn["quantity"]
        revenue = txn["quantity"] * txn["price"]

        if product not in product_summary:
            product_summary[product] = {
                "total_quantity": 0,
                "total_revenue": 0.0
            }

        product_summary[product]["total_quantity"] += quantity
        product_summary[product]["total_revenue"] += revenue

    # Filter products below threshold
    low_products = []

    for product, data in product_summary.items():
        if data["total_quantity"] < threshold:
            low_products.append(
                (product, data["total_quantity"], round(data["total_revenue"], 2))
            )

    # Sort by total quantity ascending
    low_products.sort(key=lambda x: x[1])

    return low_products

# Task 4.1: Generates a comprehensive text report
import os
from datetime import datetime
from collections import defaultdict

def generate_sales_report(transactions, enriched_transactions, output_file='output/sales_report.txt'):

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as report:

        # 1. HEADER
        
        report.write("=" * 44 + "\n")
        report.write("           SALES ANALYTICS REPORT\n")
        report.write(f"     Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        report.write(f"     Records Processed: {len(transactions)}\n")
        report.write("=" * 44 + "\n\n")
