from extraction_utils.documentai_utils import (
    get_client, 
    get_processor_name, 
    process_file,
    table_extraction
)

if __name__ == '__main__':
    # Initialize document AI client
    client = get_client()
    name = get_processor_name(client)
    mime_type = 'application/pdf'

    # Begin Input Loop
    user_input = input('Enter file name (enter \'q\' to quit): ')
    while user_input.lower() != "q":
        file_path = f'../classification_model/loss_runs/input/{user_input}'
        print(file_path)

        # Process Document
        document = process_file(client, name, file_path, mime_type)
        tables = table_extraction(document)
        for table in tables:
            print(table)
        
        # Continue input loop
        user_input = input('Enter file name (enter \'q\' to quit): ')
