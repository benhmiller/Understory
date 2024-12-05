from extraction_utils.documentai_utils import (
    get_client, 
    get_processor_name, 
    process_pdf,
    table_extraction
)

def documentai_process_pdf(file_path: str):
    # Initialize document AI client
    client = get_client()
    name = get_processor_name(client)
    mime_type = 'application/pdf'

    # Process Document
    document = process_pdf(client, name, file_path, mime_type)
    tables = table_extraction(document)
    for table in tables:
        print(table)
        
