from extraction_utils.documentai_utils import (
    get_client, get_processor_name, process_file
)

if __name__ == '__main__':
    # Initialize document AI client
    client = get_client()
    name = get_processor_name(client)
    mime_type = 'application/pdf'
    print(client)

    user_input = input('Enter file name (enter \'q\' to quit): ')
    while input.lower() != "q":
        file_path = f'../classification_model/loss_runs/input/{user_input}'

        #document = process_file(client, name, file_path, mime_type)
        user_input = input('Enter file name (enter \'q\' to quit): ')