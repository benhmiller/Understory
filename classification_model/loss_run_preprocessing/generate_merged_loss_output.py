import os
import pandas as pd

# Function to load file based on its extension
def load_file(file_path):
    # Get the file extension
    file_extension = os.path.splitext(file_path)[1]

    # Conditional logic to load the file
    if file_extension == '.csv':
        # Load CSV file
        df = pd.read_csv(file_path)
    elif file_extension == '.xlsx':
        # Load Excel file
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format. Please provide a CSV or XLSX file.")
    
    # Use loc to slice the DataFrame up to column 'description' (inclusive)
    df = df.loc[:, :'description']
    return df

if __name__ == '__main__': 
    frames = []

    # Convert all output files into single dataframe
    for filename in os.listdir('loss_runs/output'):
        f = os.path.join('loss_runs/output', filename)
        # checking if it is a file
        if os.path.isfile(f):
            frames.append(load_file(f))

    # Merge all output dataframes
    merged_output_frames = pd.concat(frames)
    merged_output_frames.to_csv('merged_loss_runs.csv', index=False)