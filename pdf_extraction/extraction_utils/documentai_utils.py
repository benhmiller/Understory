from google.cloud import documentai_v1 as docai
from google.oauth2 import service_account
import os

# Fetch environment variables
PROJECT_ID = 'verdant-cargo-443521-j3' #os.getenv("PROJECT_ID", "")
API_LOCATION = 'us' # os.getenv("API_LOCATION", "")
PROCESSOR_ID = 'f2db9bcc34ed8bb5' # os.getenv("PROCESSOR_ID", "")
CREDENTIAL_FILE_PATH = "../secret/verdant-cargo-443521-j3-8d56893a2e2e.json" # os.getenv("CREDENTIAL_FILE_PATH", "")

assert PROJECT_ID, "PROJECT_ID is undefined"
assert API_LOCATION in ("us", "eu"), "API_LOCATION is incorrect"

# Load the service account key
credentials = service_account.Credentials.from_service_account_file(
    CREDENTIAL_FILE_PATH
)

def get_client() -> docai.DocumentProcessorServiceClient:
    '''
    Construct DocAI client
    '''
    client_options = {"api_endpoint": f"{API_LOCATION}-documentai.googleapis.com"}
    return docai.DocumentProcessorServiceClient(client_options=client_options, credentials=credentials)

def get_processor_name(client: docai.DocumentProcessorServiceClient) -> str:
    '''
    Constructs processesor name for API call
    '''
    return client.processor_path(PROJECT_ID, API_LOCATION, PROCESSOR_ID)

def process_file(
    client: docai.DocumentProcessorServiceClient,
    name: str,
    file_path: str,
    mime_type: str,
) -> docai.Document:
    '''
    Invokes Doc AI file processing
    See https://codelabs.developers.google.com/codelabs/cloud-documentai-manage-processors-python#6 
    '''

    with open(file_path, "rb") as document_file:
        document_content = document_file.read()

    document = docai.RawDocument(content=document_content, mime_type=mime_type)
    
    request = docai.ProcessRequest(raw_document=document, name=name)

    response = client.process_document(request)

    return response.document