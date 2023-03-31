import os
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Extract:
    def __init__(self, input_dir):
        logger.info('Initialising extractor')
        self.input_dir = input_dir
        logger.info('Initialised extractor')

    def extract_data(self):
        logger.info('Begin extracting data')
        files = os.listdir(path=self.input_dir)
        logger.info('No. of files: {}'.format(str(len(files))))
        logger.info(files)

        dataframe = pd.DataFrame()

        for file in files:
            file_path = os.path.join(self.input_dir, file)
            df = pd.read_csv(
                filepath_or_buffer=file_path
                )
            
            dataframe = pd.concat([dataframe, df])
        
        logger.info('Extracted {} rows'.format(str(len(dataframe.index))))

        return dataframe
    
    def delete_files(self):
        logger.info('Begin deleting files from input directory')
        files = os.listdir(path=self.input_dir)
        logger.info(files)

        for file in files:
            file_path = os.path.join(self.input_dir, file)
            os.remove(file_path)
        
        logger.info('Deleted files from input directory')