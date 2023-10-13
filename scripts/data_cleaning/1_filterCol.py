import pandas as pd

# Define the list of important nutrients
keep = [
    "description","brandOwner","brandedFoodCategory","ingredients","servingSize","servingSizeUnit",
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
    "Vitamin B-6"  # Including B-6 as it is also important
]

# Read the original CSV file
df = pd.read_csv("foodNutrients.csv")

# Filter the DataFrame based on the important nutrients
filtered_df = df[keep]

# Save the filtered DataFrame to a new CSV file
filtered_df.to_csv("filtered_foodNutrients.csv", index=False)

print("Filtered CSV has been saved as filtered.csv")
