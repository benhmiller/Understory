

from google.cloud import documentai_v1 as documentai
from google.oauth2 import service_account
import base64
import json

# Prepare variables
project_id = 'verdant-cargo-443521-j3'
location = 'us'
processor_id = 'f2db9bcc34ed8bb5'

file_path = '/path/to/local/file/.pdf'
mime_type = 'application/pdf'

# Load the service account key
credentials = service_account.Credentials.from_service_account_file(
    "secret/verdant-cargo-443521-j3-8d56893a2e2e.json"
)

opts = {
    "api_endpoint" : f"{location}-documentai.googleapis.com"
}

# Configure the processor client (i.e. prepare the endpoint)
client = documentai.DocumentProcessorServiceClient(client_options=opts, credentials=credentials)

name = client.processor_path(project_id, location, processor_id)

#Open File
with open('loss_runs/input/Loss_Run___len stoler 8-24_page_5.pdf', 'rb') as pdf_file:
    pdf_data = pdf_file.read()

# Construct the request
raw_document = documentai.RawDocument(content=pdf_data, mime_type=mime_type)

request = documentai.ProcessRequest(name=name, raw_document=raw_document)

# Analyze output
result = client.process_document(request=request)

document = result.document
print(document)

# with open('documentai_results/result.json', 'w') as file:
#     json.dump(document, file, indent=4)  # Writes the Python dict to the file in JSON format