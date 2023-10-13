import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

s3 = boto3.client('s3')

try:
    # Your S3 code here, for example:
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket="fooddata-central-branded-food", Key="final_data.csv")
    s3.list_buckets()
except NoCredentialsError:
    print("No credentials could be found.")
except PartialCredentialsError:
    print("Incomplete credentials provided.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
