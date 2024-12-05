import json
from datetime import datetime, timedelta

# Define the parameters
dustbins = {
    1: "Location 1, Mumbai",
    2: "Location 2, Mumbai",
    3: "Location 3, Mumbai",
    4: "Location 4, Mumbai",
    5: "Location 5, Mumbai",
    6: "Location 6, Mumbai"
}
days_in_April = 3
dustbin_count = 6
hours = [f"{i:02}:00" for i in range(6, 19)]  # 6 am to 6 pm
regular_days = [1, 2, 3, 4, 5]  # Monday to Friday
holidays = []  # Holiday in February 2024 (Valentine's Day)

# Function to generate random amount filled within the specified range
import random
def generate_amount_filled(total_amount, capacity_left):
    if total_amount == 0:
        return random.randint(1, 4) * 10  # Positive amount filled between 10 and 40
    elif total_amount >= 100:
        return -100  # Maximum negative amount to empty the dustbin
    else:
        max_fill = min(capacity_left, 40)  # Maximum positive amount filled cannot exceed capacity left
        min_fill = -1 * min(total_amount, 100) if total_amount > 0 else -100
        return random.randint(min_fill, max_fill)

# Function to generate JSON entries for a given date and dustbin
def generate_entries(date, dustbin_id):
    entries = []
    total_amount = 0
    capacity_left = 100
    for hour in hours:
        time = f"{date} {hour}"
        amount_filled = generate_amount_filled(total_amount, capacity_left)
        if amount_filled < 0:
            total_amount = max(0, total_amount + amount_filled)  # Update total amount after negative fill
        else:
            total_amount += amount_filled
            total_amount = min(100, total_amount)  # Ensure total_amount does not exceed 100
        capacity_left = 100 - total_amount
        entry = {
            "Date": date,
            "Time": hour,
            "Dustbin_ID": dustbin_id,
            "Dustbin_Location": dustbins[dustbin_id],
            "Amount_filled": amount_filled,
            "Total_amount": total_amount,
            "Capacity_left": capacity_left
        }
        entries.append(entry)
    return entries

# Generate JSON entries for each day of February
entries = []
start_date = datetime(2024, 4, 1)
last_total_amount = 0  # Variable to keep track of the last total amount
for day in range(1, days_in_April + 1):
    date = (start_date + timedelta(days=day-1)).strftime("%Y-%m-%d")
    for dustbin_id in range(1, dustbin_count + 1):
        # Varying frequency on holidays vs regular days
        if datetime.strptime(date, "%Y-%m-%d").day in holidays:
            if random.random() < 0.8:  # 80% chance of having entries on holidays
                entries.extend(generate_entries(date, dustbin_id))
        elif datetime.strptime(date, "%Y-%m-%d").weekday() + 1 in regular_days:
            if random.random() < 0.6:  # 60% chance of having entries on regular days
                entries.extend(generate_entries(date, dustbin_id))

    last_total_amount = entries[-1]["Total_amount"] if entries else 0

# Write the entries to a JSON file
with open("dustbin_entries_april.json", "w") as json_file:
    json.dump(entries, json_file, indent=4)

print("JSON file generated successfully for February!")
