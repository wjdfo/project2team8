import os
import json
import numpy as np
import pandas as pd

class Edgar:
    '''
    parent class of edgar_cralwer.py & edgar_extractor.py
    and
    class that deal with corperation metadatas

    Method:
        getCorpsList() : Get dictionary which represents { corp : filings date : filings html link }

    '''
    def __init__(self):
        # Load the configuration file
        with open('config.json') as fin:
            self.config = json.load(fin)
            
        self.DATASET_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'edgar-datasets')
        if not os.path.exists(self.DATASET_DIR):
            os.mkdir(self.DATASET_DIR)

        # Define the directories and filepaths
        self.raw_filings_folder = os.path.join(self.DATASET_DIR, self.config['raw_filings_folder'])
        self.indices_folder = os.path.join(self.DATASET_DIR, self.config['indices_folder'])
        self.filings_metadata_filepath = os.path.join(self.DATASET_DIR, self.config['filings_metadata_file'])

        # Check if at least one filing type is provided
        if len(self.config['filing_types']) == 0:
            print('Please provide at least one filing type')
            exit()

        # If the indices and/or download folder doesn't exist, create them
        if not os.path.isdir(self.indices_folder):
            os.mkdir(self.indices_folder)
        if not os.path.isdir(self.raw_filings_folder):
            os.mkdir(self.raw_filings_folder)

        self.extracted_filings_folder = os.path.join(
            self.DATASET_DIR, self.config["extracted_filings_folder"]
        )

        # Create the extracted filings folder if it doesn't exist
        if not os.path.isdir(self.extracted_filings_folder):
            os.mkdir(self.extracted_filings_folder)

            

    def getReportUrl(self, company_name : str):
        # Check if the filings metadata file exists
        if os.path.exists(self.filings_metadata_filepath):
            df = pd.read_csv(self.filings_metadata_filepath, dtype=str)
            df = df.replace({np.nan: None})
        else:
            print(f'No such file "{self.filings_metadata_filepath}"')
            return

        length = len(df['Company'])
        url_dict = {}
        for i in range(length):
            url_dict[company_name] = {}
        for i in range(length):
            if df['Company'][i] == company_name:
                url_dict[company_name][df['Date'][i]] = df['htm_file_link'][i]

        return url_dict