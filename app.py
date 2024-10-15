import json
import pandas as pd

# Load your JSON data (assuming you have it in a file)
with open('textract_output.json', 'r') as json_file:
    data = json.load(json_file)

# Extract blocks from the JSON data
blocks = data['Blocks']

# Convert blocks to a DataFrame
df = pd.DataFrame(blocks)

# Display the DataFrame
print(df.head())