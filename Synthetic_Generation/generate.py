import random
import json
import datetime

# Define locations and their IDs
bins = [
    {"id": 1, "location": "Thane"},
    {"id": 2, "location": "Malad East"},
    {"id": 3, "location": "Kandivali"},
    {"id": 4, "location": "Goregaon East"},
    {"id": 5, "location": "Andheri West"},
    {"id": 6, "location": "Pathanwadi"}
]

# Hindu and Islamic holiday dates for 2023 and 2024 (major holidays + multi-day festivals)
hindu_holidays = [
    # Single-day festivals
    "2023-08-15",  # Janmashtami
    "2023-10-24",  # Dussehra
    "2023-11-12",  # Diwali (main day)
    "2024-03-08",  # Holi
    "2024-04-09",  # Ram Navami
    "2024-08-19",  # Raksha Bandhan
    "2024-10-12",  # Navratri start (10 days until 2024-10-22)
    "2024-11-01",  # Diwali (next year)
    
    # Multi-day festivals
    *["2023-09-19", "2023-09-20", "2023-09-21", "2023-09-22", "2023-09-23",
      "2023-09-24", "2023-09-25", "2023-09-26", "2023-09-27", "2023-09-28"],  # Ganesh Chaturthi (10 days)
    
    *["2023-10-15", "2023-10-16", "2023-10-17", "2023-10-18", "2023-10-19",
      "2023-10-20", "2023-10-21", "2023-10-22", "2023-10-23", "2023-10-24", "2023-10-25"],  # Navratri (11 days)

    # Similar pattern for 2024
    *["2024-09-07", "2024-09-08", "2024-09-09", "2024-09-10", "2024-09-11",
      "2024-09-12", "2024-09-13", "2024-09-14", "2024-09-15", "2024-09-16"],  # Ganesh Chaturthi (2024)

    *["2024-10-12", "2024-10-13", "2024-10-14", "2024-10-15", "2024-10-16",
      "2024-10-17", "2024-10-18", "2024-10-19", "2024-10-20", "2024-10-21", "2024-10-22"],  # Navratri (2024)
]

islamic_holidays = [
    # Single-day festivals
    "2023-04-22",  # Eid al-Fitr
    "2023-06-28",  # Eid al-Adha
    "2023-07-19",  # Islamic New Year (Muharram)
    "2023-09-27",  # Milad un-Nabi
    "2024-04-10",  # Eid al-Fitr (next year)
    "2024-06-17",  # Eid al-Adha (next year)
    "2024-07-06",  # Islamic New Year (next year)

    # Ramadan begins (waste might increase slightly during the evening)
    *["2023-03-23", "2023-03-24", "2023-03-25", "2023-03-26", "2023-03-27",
      "2023-03-28", "2023-03-29", "2023-03-30", "2023-03-31", "2023-04-01", 
      "2023-04-02", "2023-04-03", "2023-04-04", "2023-04-05", "2023-04-06", 
      "2023-04-07", "2023-04-08", "2023-04-09", "2023-04-10", "2023-04-11"],  # Ramadan (20 days)

    *["2024-03-11", "2024-03-12", "2024-03-13", "2024-03-14", "2024-03-15",
      "2024-03-16", "2024-03-17", "2024-03-18", "2024-03-19", "2024-03-20", 
      "2024-03-21", "2024-03-22", "2024-03-23", "2024-03-24", "2024-03-25",
      "2024-03-26", "2024-03-27", "2024-03-28", "2024-03-29", "2024-03-30"],  # Ramadan (next year)
]

# Generate waste generation multipliers for each bin on holidays
holiday_increase = {
    "hindu": {
        "Thane": 1.5, "Malad East": 1.2, "Kandivali": 1.5,
        "Goregaon East": 1.3, "Andheri West": 1.5, "Pathanwadi": 1.0
    },
    "islamic": {
        "Thane": 1.0, "Malad East": 1.2, "Kandivali": 1.0,
        "Goregaon East": 1.5, "Andheri West": 1.2, "Pathanwadi": 1.5
    }
}

# Function to check if the day is a Hindu or Islamic holiday
def is_holiday(date_str, holidays):
    return date_str in holidays

# Function to generate fill status for a day, with integer fill values
def generate_fill_status():
    fill_status = []
    current_fill = random.randint(1, 2)  # Start with some waste in the bin (0 to 2)
    for _ in range(12):  # 12 hours from 8 AM to 8 PM
        increment = random.randint(1, 3)  # Waste fills incrementally (1 to 3 units at a time)
        current_fill = min(current_fill + increment, 10)  # Ensure it stays between 0 and 10
        fill_status.append(current_fill)
    return fill_status

# Generate random time for emptying the bin (between 10 AM and 2 PM)
def get_emptying_time():
    hour = random.randint(10, 13)
    minute = random.choice([0, 15, 30, 45])
    return hour, minute

# Function to apply waste generation multiplier on holidays
def apply_holiday_multiplier(date, location, fill_status):
    date_str = date.strftime('%Y-%m-%d')
    multiplier = 1.0
    if is_holiday(date_str, hindu_holidays) and location in holiday_increase["hindu"]:
        multiplier = holiday_increase["hindu"][location]
    elif is_holiday(date_str, islamic_holidays) and location in holiday_increase["islamic"]:
        multiplier = holiday_increase["islamic"][location]
    return [min(int(f * multiplier), 10) for f in fill_status]

# Main function to generate synthetic data
# Updated logic for resetting fill levels after emptying
def apply_emptying_logic(fill_status, empty_index):
    for i in range(empty_index, len(fill_status)):
        # Gradually reduce fill level after emptying instead of setting to zero
        fill_status[i] = max(fill_status[i] - random.randint(1, 3), 0)
    return fill_status

# Main function to generate synthetic data with improved emptying logic
def generate_waste_data(start_date, end_date):
    data = []
    current_date = start_date
    entry_id = 1  # Initialize entry_id counter

    while current_date <= end_date:
        day_of_week = current_date.strftime('%A')
        date_str = current_date.strftime('%Y-%m-%d')

        for bin_info in bins:
            # Generate fill status for the day
            fill_status = generate_fill_status()

            # Apply holiday multiplier if applicable
            fill_status = apply_holiday_multiplier(current_date, bin_info["location"], fill_status)

            # Randomly decide the time of emptying for only 80% of bins each day
            if random.random() < 0.8:  # 80% chance that a bin will be emptied
                empty_hour, empty_minute = get_emptying_time()
                empty_index = empty_hour - 8  # Map to 8 AM - 8 PM range
                fill_status = apply_emptying_logic(fill_status, empty_index)

            # Simulate 12-hour recording of fill status
            for hour in range(12):
                hour_time = (8 + hour) % 24  # Starting from 8 AM
                time_str = f'{hour_time}:00'

                # Append data
                data.append({
                    "entry_ID": entry_id,  # Add entry_ID to track entries
                    "dustbin_id": bin_info["id"],
                    "location": bin_info["location"],
                    "filled_capacity": fill_status[hour],
                    "date": date_str,
                    "time": time_str,
                    "day_of_week": day_of_week
                })

                # Increment entry_id after each entry
                entry_id += 1

        # Increment to next day
        current_date += datetime.timedelta(days=1)

    return data


# Define date range (1st July 2023 to 18th September 2024)
start_date = datetime.date(2023, 7, 1)
end_date = datetime.date(2024, 9, 18)

# Generate the dataset
dataset = generate_waste_data(start_date, end_date)

# Save to JSON file
with open('synthetic_waste_data.json', 'w') as json_file:
    json.dump(dataset, json_file, indent=4)

print(f"Data generation complete. {len(dataset)} entries saved to 'synthetic_waste_data.json'.")
