import os
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Load:
    def __init__(self, success_dir, unsuccessful_dir):
        logger.info('Initialising loader')
        self.success_dir = success_dir
        self.unsuccessful_dir = unsuccessful_dir

        self.create_directories()
        logger.info('Initialised loader')

    def create_directories(self):
        logger.info('Checking if output directories exist')
        if not os.path.exists(self.success_dir):
            os.makedirs(self.success_dir)
            logger.info('Creating directory: {}'.format(self.success_dir))
        
        if not os.path.exists(self.unsuccessful_dir):
            os.makedirs(self.unsuccessful_dir) 
            logger.info('Creating directory: {}'.format(self.unsuccessful_dir))

    def load(self, df, dest='success'):
        if dest == 'success':
            logger.info('Begin loading to: {}'.format(self.success_dir))
            output_path = os.path.join(
                self.success_dir, 
                str(datetime.now()) + '.csv'
                )
            df.to_csv(
                path_or_buf=output_path, 
                index=False
                )
        else:
            logger.info('Begin loading to: {}'.format(self.unsuccessful_dir))
            output_path = os.path.join(
                self.unsuccessful_dir, 
                str(datetime.now()) + '.csv'
                )
            df.to_csv(
                path_or_buf=output_path, 
                index=False
                )
            
        logger.info('Loaded file to: {}'.format(output_path))