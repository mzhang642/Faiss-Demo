import pandas as pd
import numpy as np
import math

def extract_value_and_convert(value, column):
    # Handle zeros specifically
    if value == 0 or value == "0":
        return 0
    
    # Handle plain numbers
    if isinstance(value, (int, float)):
        return math.ceil(value)
    
    # Split the value by space
    parts = str(value).split(" ")
    
    if len(parts) < 1:
        return np.nan
    
    num_value, unit = parts[0], parts[1]
    num_value = float(num_value)
    
    # Convert Energy from kJ to kcal if needed
    if column == "Energy" and unit == "kJ":
        num_value = num_value / 4.184  # 1 kcal = 4.184 kJ
    
    # Round up the value
    num_value = math.ceil(num_value)
    
    return int(num_value)

# Read the original CSV file
df = pd.read_csv("filtered_foodNutrients.csv")

# List of nutrient columns to process
nutrient_columns = [
    "Protein",
    "Total lipid (fat)",
    "Carbohydrate, by difference",
    "Energy",
    "Calcium, Ca",
    "Iron, Fe",
    "Sodium, Na",
    "Potassium, K",
    "Vitamin A, IU",
    "Vitamin C, total ascorbic acid",
    "Vitamin D (D2 + D3), International Units",
    "Vitamin B-12",
    "Magnesium, Mg",
    "Phosphorus, P",
    "Zinc, Zn",
    "Fiber, total dietary",
    "Sugars, total including NLEA",
    "Cholesterol",
    "Fatty acids, total saturated",
    "Folate, total",
    "Vitamin E",
    "Vitamin B-6"
]

# Process each nutrient column
for column in nutrient_columns:
    df[column] = df[column].apply(lambda x: extract_value_and_convert(x, column))

# Save the processed DataFrame to a new CSV file
df.to_csv("numerical_nutri.csv", index=False)