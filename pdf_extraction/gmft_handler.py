from gmft_pymupdf import PyMuPDFDocument
from gmft.auto import AutoTableDetector, AutoTableFormatter, AutoFormatConfig
from typing import List
import pandas as pd

def gmft_process_pdf(file_path: str) -> List[pd.DataFrame]:
    # Open Document
    doc = PyMuPDFDocument(file_path)

    # Initialize Detector and Formatter
    detector = AutoTableDetector()
    formatter = AutoTableFormatter()
    config = AutoFormatConfig(
        semantic_spanning_cells=True,  # If tables have merged cells
        verbosity=3
    )

    # Extract Tables
    tables = []
    for page in doc:
        tables += detector.extract(page)
    
    # Convert Tables to Dataframes
    dfs = []
    for table in tables:
        ft = formatter.extract(table)
        dfs.append(ft.df()) # formatter's tables automatically uses settings of config
    
    return dfs