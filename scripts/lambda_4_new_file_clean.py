import boto3
import json
import datetime


# Defining file_information parameters
bucket_name = "proyecto-productos-amazon"
file_information = "base_datos/files_information-clean.json"

s3_client = boto3.client("s3", "us-west-2")
client = boto3.client('glue')

def file_validation(file_name, file_type, file_size, upload_date):
    # ** Reading file_information **
    try:
        # read file_information from s3
        read_file_information = s3_client.get_object(
            Key=file_information,
            Bucket=bucket_name
        )
    except Exception as e:
        # File not found - Creating files_information file
        file_body = []
        save_to_s3 = s3_client.put_object(
            Key=file_information,
            Bucket=bucket_name,
            Body=(json.dumps(file_body).encode("utf-8"))
        )
        # Reading new file created
        read_file_information = s3_client.get_object(
            Key=file_information,
            Bucket=bucket_name
        )
    
    file_data = read_file_information["Body"].read()
    file_info = json.loads(file_data)
    
    # Add the new file information
    new_file_info = {
        "file_name": file_name,
        "file_type": file_type,
        "file_size": file_size,
        "upload_date": upload_date
    }
    file_info.append(new_file_info)
    
    # Update the file_information in S3
    s3_client.put_object(
        Key=file_information,
        Bucket=bucket_name,
        Body=(json.dumps(file_info).encode("utf-8"))
    )
    

def lambda_handler(event, context):
    # Get the S3 bucket and object key from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    # Get the file name
    file_name = key.split('/')[-1]
    
    # Get the file type
    file_type = file_name.split('.')[-1]
    
    # Get the file size
    s3 = boto3.client('s3')
    response = s3.head_object(Bucket=bucket, Key=key)
    file_size = response['ContentLength']
    
    # Get the upload date
    upload_date = response['LastModified'].strftime('%Y-%m-%d')
    
    file_validation(file_name, file_type, file_size, upload_date)
    
    # Check if file_name contains "meta"
    if "meta" in file_name:
        print('Crawler meta (ppa-crawler-s3-clean-meta) starting...')
        response = client.start_crawler(Name='ppa-crawler-s3-clean-meta')
        print(json.dumps(response))
    else:
        print('Crawler review (ppa-crawler-s3-clean-review) starting...')
        response = client.start_crawler(Name='ppa-crawler-s3-clean-review')
        print(json.dumps(response))