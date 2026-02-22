import sys
import pandas as pd


## uv run python scripts/xls_to_csv.py "data/Sample - Superstore.xls"

# Get the Excel file path from the command line
excel_file = sys.argv[1]

# Load the Excel file
xls = pd.ExcelFile(excel_file)

# Sheets to extract
sheets = ["Orders", "Returns"]

# Convert each sheet to CSV
for sheet in sheets:
    df = pd.read_excel(xls, sheet_name=sheet)
    sheet = sheet.lower()
    csv_file = f"data/{sheet}.csv"
    df.to_csv(csv_file, index=False)
    print(f"Saved {sheet} sheet to {csv_file}")