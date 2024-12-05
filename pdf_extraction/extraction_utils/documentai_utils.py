from google.cloud import documentai_v1 as docai
from google.oauth2 import service_account
import os
from typing import Sequence, List
import pandas as pd

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

'''
DOCUMENT AI BUILD AND CALL FUNCTIONS
'''
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

def process_pdf(
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

'''
RESPONSE ANALYSIS FUNCTIONS
'''
def table_extraction(
    document: docai.Document
) -> List[pd.DataFrame]:
    '''
    Function to extract tables from document AI output and convert to pandas Dataframe
    '''
    # Extract document text
    full_text = document.text
    tables_as_dataframes = []

    # Iterate over available pages and handle each available table
    for page in document.pages:
        for table in page.tables:
            # Extract header and body rows
            headers = extract_table_rows(table.header_rows, full_text)
            body = extract_table_rows(table.body_rows, full_text)

            # Use the first header row (if available) as column names
            if headers:
                df = pd.DataFrame(body, columns=headers[0])
            else:
                # If no headers, create generic column names
                num_columns = max(len(row) for row in body) if body else 0
                df = pd.DataFrame(body, columns=[f"Column {i+1}" for i in range(num_columns)])
            
            # Append the DataFrame for this table
            tables_as_dataframes.append(df)
    
    return tables_as_dataframes

def extract_table_rows(
    table_rows: Sequence[docai.Document.Page.Table.TableRow], text: str
) -> List[List[str]]:
    '''
    Extracts rows of text from Document AI table rows
    '''
    rows = []
    for table_row in table_rows:
        row_data = []
        for cell in table_row.cells:
            cell_text = layout_to_text(cell.layout, text).strip()
            row_data.append(cell_text)
        rows.append(row_data)
    return rows

def layout_to_text(layout: docai.Document.Page.Layout, text: str) -> str:
    """
    Document AI identifies text in different parts of the document by their
    offsets in the entirety of the document"s text. This function converts
    offsets to a string.
    """
    # If a text segment spans several lines, it will
    # be stored in different text segments.
    return "".join(
        text[int(segment.start_index) : int(segment.end_index)]
        for segment in layout.text_anchor.text_segments
    )
