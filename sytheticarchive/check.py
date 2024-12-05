import json

# Load JSON file
with open("dustbin_entries.json", "r") as json_file:
    entries = json.load(json_file)

# Check if any value in "Total_amount" is greater than 100 or less than 0
invalid_total_amount = any(entry["Total_amount"] > 100 or entry["Total_amount"] < 0 for entry in entries)

# Check if any value in "Capacity_left" is less than 0 or greater than 100
invalid_capacity = any(entry["Capacity_left"] < 0 or entry["Capacity_left"] > 100 for entry in entries)

# Check if any value in "Amount_filled" is outside the range of -100 to 100
invalid_amount_filled = any(abs(entry["Amount_filled"]) > 100 for entry in entries)

if invalid_total_amount:
    print("Error: Total amount exceeds valid range (0-100) in some entries.")
else:
    print("All total amounts are within the valid range.")

if invalid_capacity:
    print("Error: Capacity left exceeds valid range (0-100) in some entries.")
else:
    print("All capacities left are within the valid range.")

if invalid_amount_filled:
    print("Error: Amount filled exceeds valid range (-100 to 100) in some entries.")
else:
    print("All amounts filled are within the valid range.")
