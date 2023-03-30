import os
import pandas as pd

class Extract:
    def __init__(self, input_dir):
        self.input_dir = input_dir

    def extract_data(self):
        files = os.listdir(path=self.input_dir)

        dataframe = pd.DataFrame()

        for file in files:
            file_path = os.path.join(self.input_dir, file)
            df = pd.read_csv(
                filepath_or_buffer=file_path
                )
            
            dataframe = pd.concat([dataframe, df])

        return dataframe