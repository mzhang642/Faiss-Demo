from sklearn.preprocessing import StandardScaler
import pandas as pd
import boto3 
from dotenv import load_dotenv
import os
import logging


def load_data_from_s3(bucket_name, file_name):
    
    logging.getLogger('botocore').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    
    # Load environment variables
    load_dotenv()
    
    # Access environment variables
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    
    # Initialize AWS S3 client
    s3 = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )
    try:
        obj = s3.get_object(Bucket=bucket_name, Key=file_name)
        return pd.read_csv(obj['Body'])
    except Exception as e:
        print(f"Error loading data from S3: {e}")
        return None

def normalize_data(df, columns):
    try:
        scaler = StandardScaler()
        df_copy = df.copy()
        df_copy[columns] = scaler.fit_transform(df_copy[columns])
        return df_copy, scaler
    except Exception as e:
        print(f"Error normalizing data: {e}")
        return None, None

def convert_to_numpy(df, columns):
    return df[columns].values.astype('float32')