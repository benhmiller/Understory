import json
import pandas as pd

# Load the JSON file containing the Textract output
with open('textract_output.json', 'r') as json_file:
    textract_response = json.load(json_file)

def extract_tables_from_json(response):
    # Create a dictionary to map Block Ids to Blocks for faster lookup
    block_map = {block['Id']: block for block in response['Blocks']}
    
    tables = []
    for block in response['Blocks']:
        if block['BlockType'] == 'TABLE':
            table = {}
            for relationship in block.get('Relationships', []):
                if relationship['Type'] == 'CHILD':
                    cell_ids = relationship['Ids']
                    for cell_id in cell_ids:
                        cell_block = block_map.get(cell_id)
                        if cell_block and cell_block['BlockType'] == 'CELL':
                            row = cell_block['RowIndex']
                            col = cell_block['ColumnIndex']
                            cell_text = ''
                            
                            # Get the text from the WORD blocks inside the CELL block
                            for rel in cell_block.get('Relationships', []):
                                if rel['Type'] == 'CHILD':
                                    for word_id in rel['Ids']:
                                        word_block = block_map.get(word_id)
                                        if word_block and word_block['BlockType'] == 'WORD':
                                            cell_text += word_block['Text'] + ' '
                            
                            # Add the cell text to the table dictionary
                            if row not in table:
                                table[row] = {}
                            table[row][col] = cell_text.strip()
            tables.append(table)
    return tables

if __name__ == '__main__':
    # Call the function to extract tables
    tables = extract_tables_from_json(textract_response)

    # Display the extracted table data as DataFrames for better readability
    for table in tables:
        print(table)
        # Convert the extracted table into a DataFrame
        df = pd.DataFrame.from_dict(table, orient='index')
        #print(df)
    
    print(df.head(2))
