import io
import json
import pandas as pd
import boto3

# Initialize S3 client
s3 = boto3.client('s3')

# Define the bucket and file names
bucket_name = 'fooddata-central-branded-food'
json_file_name = 'brandedDownload.json'
csv_file_name = 'new_cleaned_data.csv'

# Load JSON data from S3
response = s3.get_object(Bucket=bucket_name, Key=json_file_name)
data = json.loads(response['Body'].read().decode('utf-8'))

# Initialize an empty list to store the cleaned data
cleaned_data = []

# Initialize a set to store unique nutrient names
unique_nutrients = set()

# Iterate through each food item in the JSON data
for food in data['BrandedFoods']:
    # Initialize a dictionary to store cleaned food data
    cleaned_food = {}
    
    # Extract basic attributes
    cleaned_food['description'] = food.get('description', '')
    cleaned_food['brandOwner'] = food.get('brandOwner', '')
    cleaned_food['brandedFoodCategory'] = food.get('brandedFoodCategory', '')
    cleaned_food['ingredients'] = food.get('ingredients', '')
    cleaned_food['servingSize'] = food.get('servingSize', '')
    cleaned_food['servingSizeUnit'] = food.get('servingSizeUnit', '')
    
    # Extract nutrients
    nutrients = {}
    for nutrient in food.get('foodNutrients', []):
        nutrient_name = nutrient.get('nutrient', {}).get('name', '')
        nutrient_amount = nutrient.get('amount', 0)
        nutrient_unit = nutrient.get('nutrient', {}).get('unitName', '')

        # Scale the nutrient amount according to serving size
        scaled_nutrient_amount = (nutrient_amount / 100) * cleaned_food['servingSize']

        # Add nutrient to unique set
        unique_nutrients.add(nutrient_name)
        
        # Store nutrient amount and unit
        nutrients[nutrient_name] = f"{scaled_nutrient_amount} {nutrient_unit}"
    
    # Add nutrients to cleaned_food
    cleaned_food.update(nutrients)
    
    # Add cleaned_food to cleaned_data
    cleaned_data.append(cleaned_food)

# Create a DataFrame
df = pd.DataFrame(cleaned_data)

# Fill missing nutrients with '0'
for nutrient in unique_nutrients:
    df[nutrient] = df[nutrient].fillna('0')

# Save DataFrame to CSV
csv_buffer = io.StringIO()
df.to_csv(csv_buffer, index=False)

# Upload CSV to S3
s3.put_object(Body=csv_buffer.getvalue(), Bucket=bucket_name, Key=csv_file_name)

