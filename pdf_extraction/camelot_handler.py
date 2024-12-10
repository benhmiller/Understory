from typing import List
import pandas as pd

'''
Handler for PDF table extraction with camelot library

See https://gmft.readthedocs.io/en/latest/index.html
For installation issues, see: https://stackoverflow.com/questions/74939758/camelot-deprecationerror-pdffilereader-is-deprecated
'''
def camelot_process_pdf(file_path: str) -> List[pd.Dataframe]:
    pass