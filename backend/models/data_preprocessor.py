from sklearn.preprocessing import StandardScaler
import pandas as pd
import boto3 

def load_data_from_s3(bucket_name, file_name):
    try:
        s3 = boto3.client('s3')
        obj = s3.get_object(Bucket=bucket_name, Key=file_name)
        return pd.read_csv(obj['Body'])
    except Exception as e:
        print(f"Error loading data from S3: {e}")
        return None

def normalize_data(df, columns):
    try:
        scaler = StandardScaler()
        df[columns] = scaler.fit_transform(df[columns])
        return df, scaler
    except Exception as e:
        print(f"Error normalizing data: {e}")
        return None, None

def convert_to_numpy(df, columns):
    return df[columns].values.astype('float32')