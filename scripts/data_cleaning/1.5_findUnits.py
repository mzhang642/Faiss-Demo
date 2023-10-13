import pandas as pd

def extract_units(value):
    # Split the string by space and take the last element as the unit
    parts = str(value).split()
    return parts[-1] if len(parts) > 1 else None

# Read the original CSV file
df = pd.read_csv("filtered_foodNutrients.csv", encoding='utf-8')  # Ensure proper encoding

# List of nutrient columns you're interested in
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

# Initialize an empty dictionary to store unique units for each nutrient
unique_units = {}

# Iterate through each nutrient column to find the unique units
for column in nutrient_columns:
    # Apply the extract_units function to each cell in the column
    units_column = df[column].apply(extract_units)
    
    # Find the unique units in the column
    unique_units_in_column = units_column.dropna().unique()
    
    # Store the unique units in the dictionary
    unique_units[column] = unique_units_in_column

# Print out the units for each nutrient
for nutrient, units in unique_units.items():
    print(f"The units for {nutrient} are: {', '.join(units)}")
