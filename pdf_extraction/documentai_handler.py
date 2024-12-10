from typing import List
import pandas as pd
from extraction_utils.documentai_utils import (
    get_client, 
    get_processor_name, 
    process_pdf,
    table_extraction
)


'''
Handler for PDF table extraction with Google's Document AI

See https://cloud.google.com/document-ai?hl=en
'''
def documentai_process_pdf(file_path: str) -> List[pd.DataFrame]:
    # Initialize document AI client
    client = get_client()
    name = get_processor_name(client)
    mime_type = 'application/pdf'

    # Process Document
    document = process_pdf(client, name, file_path, mime_type)
    tables = table_extraction(document)
    # for table in tables:
    #     print(table)
    
    return tables