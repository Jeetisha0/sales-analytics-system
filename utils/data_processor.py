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
            "TransactionID": transaction_id,
            "Date": date,
            "ProductID": product_id,
            "ProductName": product_name,
            "Quantity": quantity,
            "UnitPrice": unit_price,
            "CustomerID": customer_id,
            "Region": region
        })

    return cleaned_transactions
