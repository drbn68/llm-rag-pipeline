# app/aws_util.py

import boto3
import os
from dotenv import load_dotenv
from botocore.exceptions import NoCredentialsError, ClientError

# Load environment variables from the .env file
load_dotenv()

# Debugging: Check if the credentials are loaded
print("AWS_ACCESS_KEY_ID:", os.getenv('AWS_ACCESS_KEY_ID'))
print("AWS_SECRET_ACCESS_KEY:", os.getenv('AWS_SECRET_ACCESS_KEY'))
print("AWS_DEFAULT_REGION:", os.getenv('AWS_DEFAULT_REGION'))

# Initialize S3 client with error handling
def initialize_s3_client():
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_DEFAULT_REGION')
        )
        print("✅ S3 client initialized successfully.")
        return s3_client
    except NoCredentialsError:
        print("❌ AWS credentials not found. Check your .env file.")
    except Exception as e:
        print(f"❌ Unexpected error initializing S3 client: {e}")
    return None

# Initialize the S3 client globally
s3 = initialize_s3_client()

# Upload a file to S3
def upload_file_to_s3(file_path, bucket_name, object_name=None):
    if s3 is None:
        print("❌ S3 client is not initialized. Check AWS credentials.")
        return

    if object_name is None:
        object_name = os.path.basename(file_path)

    try:
        s3.upload_file(file_path, bucket_name, object_name)
        print(f"✅ File '{file_path}' uploaded to '{bucket_name}/{object_name}' successfully.")
    except ClientError as e:
        print(f"❌ Client error occurred: {e.response['Error']['Message']}")
    except Exception as e:
        print(f"❌ Unexpected error uploading file: {e}")

# List files in an S3 bucket
def list_files_in_s3(bucket_name):
    if s3 is None:
        print("❌ S3 client is not initialized. Check AWS credentials.")
        return []

    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in response:
            return [obj['Key'] for obj in response['Contents']]
        else:
            print(f"ℹ️ The bucket '{bucket_name}' is empty.")
            return []
    except NoCredentialsError:
        print("❌ AWS credentials not available.")
    except ClientError as e:
        print(f"❌ Client error occurred: {e.response['Error']['Message']}")
    except Exception as e:
        print(f"❌ Unexpected error listing files: {e}")
    return []
