import boto3

def lambda_handler(event, context):
    # Initialize S3 client
    s3 = boto3.client('s3')
    
    # Get the bucket and object key from the event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']
    
    # Extract folder name (folder 1)
    folder_name = object_key.split('/')[1]
    
    # Generate new file name
    new_file_name = f'{folder_name}.json'
    
    # Copy the file with the new name to folder 2
    s3.copy_object(
        Bucket=bucket_name,
        CopySource={'Bucket': bucket_name, 'Key': object_key},
        Key=f'procesados/{new_file_name}'
    )
    
    # Delete the original file
    s3.delete_object(
        Bucket=bucket_name,
        Key=object_key
    )
    
    return {
        'statusCode': 200,
        'body': f'File {object_key} processed successfully'
    }
