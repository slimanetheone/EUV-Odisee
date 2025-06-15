import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

seed_value = 42
max_votes = 100000
np.random.seed(seed_value)
random.seed(seed_value)

num_records_per_country = max_votes

country_mobile_formats = {
    "BE": "+32 4{0:02d} {1:03d} {2:03d}",
    "FR": "+33 6 {0:02d} {1:02d} {2:02d} {3:02d}",
    "DE": "+49 15{0:01d} {1:03d} {2:04d}",
    "CH": "+41 7{0:01d} {1:03d} {2:02d} {3:02d}",
    "IT": "+39 3{0:02d} {1:03d} {2:03d}",
    "ES": "+34 6{0:01d} {1:02d} {2:02d} {3:02d}",
    "MA": "+212 6{0:01d} {1:02d} {2:02d} {3:02d}",
    "UK": "+44 7{0:02d} {1:03d} {2:04d}",
    "SE": "+46 7{0:01d} {1:03d} {2:03d}",
    "PT": "+351 9{0:02d} {1:03d} {2:03d}",
    "NL": "+31 6 {0:02d} {1:03d} {2:03d}"
}

def generate_mobile_number(country_code):
    if country_code == "BE":
        return country_mobile_formats[country_code].format(
            random.randint(70, 99),
            random.randint(100, 999),
            random.randint(100, 999)
        )
    elif country_code == "IT":
        return country_mobile_formats[country_code].format(
            random.randint(0, 99),
            random.randint(100, 999),
            random.randint(100, 999)
        )
    # Voeg andere landen toe zoals in je documentatie
    else:
        return country_mobile_formats.get(country_code, "+00 000 000 000").format(
            random.randint(0, 99),
            random.randint(100, 999),
            random.randint(100, 999)
        )

# Hoofdlogica
choice = os.environ.get("VOTE_COUNTRY_MODE")
if not choice:
    print("Do you want to generate votes for Italy only or all EU festival countries?")
    choice = input("Type 'IT' for Italy only or 'ALL' for all countries: ").strip().upper()
else:
    choice = choice.strip().upper()

if choice == 'IT':
    selected_countries = ['IT']
elif choice == 'ALL':
    selected_countries = list(country_mobile_formats.keys())
else:
    print("Invalid choice, defaulting to Italy only.")
    selected_countries = ['IT']

current_time = datetime.now()
os.makedirs("/data", exist_ok=True)

for country_code in selected_countries:
    data = {
        "COUNTRY CODE": [],
        "MOBILE NUMBER": [],
        "SONG NUMBER": [],
        "TIMESTAMP": []
    }
    
    for _ in range(num_records_per_country):
        data["COUNTRY CODE"].append(country_code)
        data["MOBILE NUMBER"].append(generate_mobile_number(country_code))
        data["SONG NUMBER"].append(random.randint(1, 25))
        random_seconds = random.randint(0, 3600)
        timestamp = current_time - timedelta(seconds=random_seconds)
        data["TIMESTAMP"].append(timestamp.strftime('%Y-%m-%dT%H:%M:%S'))
    
    filename = f"/data/{country_code.lower()}_votes.txt"
    pd.DataFrame(data).to_csv(filename, index=False, header=False)
    print(f"File '{filename}' has been saved.")
