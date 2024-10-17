from dotenv import load_dotenv
import boto3
import time
import json
import os

# Load the environment variables from the .env file
load_dotenv()

# Initialize Textract client
textract = boto3.client('textract', region_name='us-east-1')

# Get Bucket Name from Environment Variable
bucket_name = os.getenv('BUCKET')

# Start the document analysis job
response = textract.start_document_analysis(
    DocumentLocation={
        'S3Object': {
            'Bucket': bucket_name,
            'Name': 'AndersonTest.pdf'
        }
    },
    FeatureTypes=['TABLES'],
)

job_id = response['JobId']
print(f"Job started with ID: {job_id}")

# Poll for the job result
while True:
    response = textract.get_document_analysis(JobId=job_id)
    
    # Check job status
    status = response['JobStatus']
    print(f"Job status: {status}")

    if status in ['SUCCEEDED', 'FAILED']:
        break

    time.sleep(5)  # Wait before checking again

# If the job succeeded, access the blocks
if status == 'SUCCEEDED':
    # Save blocks to a JSON file
    with open('textract_output.json', 'w') as json_file:
        json.dump(response, json_file, indent=4)  # Save with indentation for readability

    print("Blocks saved to textract_output.json")
else:
    print("Job failed.")