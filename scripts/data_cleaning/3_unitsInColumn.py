import pandas as pd

# Read the existing CSV file
df = pd.read_csv("numerical_nutri.csv")

# Dictionary to map existing column names to new names with units
column_rename_dict = {
    "Protein": "Protein (g)",
    "Total lipid (fat)": "Total Lipid (g)",
    "Carbohydrate, by difference": "Carbohydrate (g)",
    "Energy": "Energy (kcal)",
    "Calcium, Ca": "Calcium (mg)",
    "Iron, Fe": "Iron (mg)",
    "Sodium, Na": "Sodium (mg)",
    "Potassium, K": "Potassium (mg)",
    "Vitamin A, IU": "Vitamin A (IU)",
    "Vitamin C, total ascorbic acid": "Vitamin C (mg)",
    "Vitamin D (D2 + D3), International Units": "Vitamin D (IU)",
    "Vitamin B-12": "Vitamin B-12 (µg)",
    "Magnesium, Mg": "Magnesium (mg)",
    "Phosphorus, P": "Phosphorus (mg)",
    "Zinc, Zn": "Zinc (mg)",
    "Fiber, total dietary": "Dietary Fiber (g)",
    "Sugars, total including NLEA": "Total Sugars (g)",
    "Cholesterol": "Cholesterol (mg)",
    "Fatty acids, total saturated": "Fatty Acids, Saturated (g)",
    "Folate, total": "Folate (µg)",
    "Vitamin E": "Vitamin E (mg)",
    "Vitamin B-6": "Vitamin B-6 (mg)"
}

# Rename the columns
df.rename(columns=column_rename_dict, inplace=True)

# Save the DataFrame back to a new CSV file
df.to_csv("final_data.csv", index=False)

print("CSV file has been saved with new column names.")
