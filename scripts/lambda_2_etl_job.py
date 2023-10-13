import boto3
import json


def lambda_handler(event, context):
    s3_client = boto3.client("s3", "us-west-2")

    # Defining file_information parameters
    bucket_name = "proyecto-productos-amazon"
    file_information = "base_datos/files_information-raw.json"
    
    # read file_information from s3
    read_file_information = s3_client.get_object(
        Key=file_information,
        Bucket=bucket_name
    )
    
    file_data = read_file_information["Body"].read()
    file_info = json.loads(file_data)
    
    last_file_info = file_info[-1]
    file_name = last_file_info["file_name"].split(".")[0]
    
    glue = boto3.client('glue')
    
    if event['detail']['state'] == 'Succeeded': 
        # Check if file_name contains "meta"
        if "meta" in file_name:
            job_name = 'ppa-glue-etl-spark-meta'
            response = glue.start_job_run(JobName=job_name)
        else:
            job_name = 'ppa-glue-etl-spark-reviews'
            response = glue.start_job_run(JobName=job_name)
    else:
        print(f"Error: Glue Crawler run failed.")
