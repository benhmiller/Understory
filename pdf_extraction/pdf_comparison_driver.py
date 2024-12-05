from documentai_handler import documentai_process_pdf
'''
File to run and compare PDF table extraction performed by Google Document AI, camelot, and gmft
'''
if __name__ == '__main__':
    # Begin Input Loop
    user_input = input('Enter file name (enter \'q\' to quit): ')
    while user_input.lower() != "q":
        # Validate File Name
        file_path = f'../classification_model/loss_runs/input/{user_input}'
        print(file_path)

        # Call PDF Processors
        camelot_tables = camelot_process_pdf(file_path)
        gmft_tables = gmft_process_pdf(file_path)

        # Compare Outputs
        # ...

        # Document AI Fallback (saves API Calls)
        #docai_tables = documentai_process_pdf(file_path)
        
        # Continue input loop
        user_input = input('Enter file name (enter \'q\' to quit): ')
