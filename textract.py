import boto3
import time

# Initialize Textract client
textract = boto3.client('textract', region_name='us-east-1')

# Start the document text detection job
response = textract.start_document_text_detection(
    DocumentLocation={
        'S3Object': {
            'Bucket': 'understorysubmissionsbucket',
            'Name': 'Dealer Loss History 3-YEAR.pdf'
        }
    }
)

job_id = response['JobId']
print(f"Job started with ID: {job_id}")

# Poll for the job result
while True:
    response = textract.get_document_text_detection(JobId=job_id)
    
    # Check job status
    status = response['JobStatus']
    print(f"Job status: {status}")

    if status in ['SUCCEEDED', 'FAILED']:
        break

    time.sleep(5)  # Wait before checking again

# If the job succeeded, access the blocks
if status == 'SUCCEEDED':
    blocks = response['Blocks']
    print("Blocks:", blocks)
else:
    print("Job failed.")