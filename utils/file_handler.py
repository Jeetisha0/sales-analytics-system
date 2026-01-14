# Responsible for safely reading sales data file

import os

def read_sales_file(file_path):
    """
    Reads the sales data file safely handling encoding issues.
    Returns a list of raw data lines .
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    lines = []

    # Try utf-8 first, then fallback to latin-1
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
    except UnicodeDecodeError:
        with open(file_path, "r", encoding="latin-1") as file:
            lines = file.readlines()

    # Remove header and empty lines
    cleaned_lines = []
    for line in lines[1:]:  # skip header
        line = line.strip()
        if line:
            cleaned_lines.append(line)

    return cleaned_lines
