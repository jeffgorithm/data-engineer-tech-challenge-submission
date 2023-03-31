import pandas as pd
from dateutil.parser import parse
from datetime import datetime, timedelta
from hashlib import sha256
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Transform:
    def __init__(self):
        logger.info('Initialising transformer')
        self.final_cols = [
            'first_name', 'last_name', 'date_of_birth', \
            'above_18', 'membership_id'
            ]
        logger.info('Initialised transformer')
        
    def transform(self, df):
        logger.info('Starting transfomation')
        # Validate mobile_no
        df['valid_mobile_no'] = df['mobile_no'].apply(lambda row: self.validate_mobile_no(row))
        
        # Validate email
        df['valid_email'] = df['email'].str.match(r"^.+@.+\..{2,}$")

        # Process date
        df['cleaned_date'] = df['date_of_birth'].apply(lambda row: self.clean_date(row))
        df['dob'] = pd.to_datetime(df['cleaned_date'])
        date = datetime.strptime("2022-01-01", '%Y-%m-%d')
        df['age_days'] = (date - df['dob'])
        df['above_18'] = df['age_days'].apply(lambda row: self.is_above_18(row))
        df['date_of_birth'] = df['dob'].apply(lambda row: self.format_birthday(row))

        # Process name field
        df['empty_name'] = df['name'].isnull()
        df['name'] = df['name'].apply(lambda row: self.filter_salutation(row))
        df['name'] = df['name'].apply(lambda row: self.filter_title(row))
        df['first_name'] = df['name'].apply(lambda row: self.format_first_name(row))
        df['last_name'] = df['name'].apply(lambda row: self.format_last_name(row))

        # Generate membership_id
        df['membership_id'] = df.apply(self.create_membership_id, axis=1)
        df['success'] = df.apply(self.validate_applications, axis=1)

        # Separate successful and unsuccessful applications
        success_df = df[df['success'] == True]
        success_df.reset_index(drop=True, inplace=True)
        logger.info('No. of successful rows: {}'.format(str(len(success_df.index))))

        unsuccessful_df = df[df['success'] == False]
        unsuccessful_df.reset_index(drop=True, inplace=True)
        logger.info('No. of unsuccessful rows: {}'.format(str(len(unsuccessful_df.index))))

        logger.info('Completed transformation')

        return success_df[self.final_cols], unsuccessful_df[self.final_cols]

    def clean_date(self, date):
        try:
            if '-' in date:
                date = date.replace('-', '/')

            split = date.split('/')

            if len(split[0]) == 4:
                order = [split[2], split[1], split[0]]
                new_date = '/'.join(order)
            else:
                new_date = '/'.join(split)

            parsed_date = parse(new_date)

            return parsed_date
        except Exception as e:
            logger.error(e)
            logger.error('Invalid date format/value: {}'.format(date))

            return None

    def validate_applications(self, row):
        if row['valid_mobile_no'] == False or row['valid_email'] == False or row['above_18'] == False or row['empty_name'] == True:
            return False
        else:
            return True

    # Function that ensures that mobile_no is 8 digits
    def validate_mobile_no(self, mobile_no):
        if len(mobile_no) == 8:
            return True
        else:
            return False

    def is_above_18(self, row):
        # Create a new field named above_18 based on the applicant's birthday
        if row >= timedelta(days=(18 * 365)):
            return True
        else:
            return False

    def filter_salutation(self, name):
        # Filter salutations in prefix such as Mr., Dr. etc.
        salutations = ['Mr. ', 'Dr. ', 'Ms. ', 'Mrs. ']

        for salutation in salutations:
            if salutation in name:
                new_name = name.strip(salutation)

                return new_name
        
        return name

    def filter_title(self, name):
        # Filter titles from postfix such as MD, etc.
        titles = [' MD']

        for title in titles:
            if title in name:
                new_name = name.strip(title)

                return new_name
        
        return name

    # Function to extract first_name from name
    def format_first_name(self, name):
        # Split name into first_name 
        split = name.split(' ')

        if len(split) >= 1:
            return split[0]
        else:
            return None
        
    # Function to extract last_name from name
    def format_last_name(self, name):
        # Split name into last_name
        split = name.split(' ')

        if len(split) >= 1:
            return ' '.join(split[1:len(split)])
        else:
            return None

    def format_birthday(self, row):
        # Format birthday field into YYYYMMDD
        try:
            return row.strftime('%Y%m%d')
        except Exception as e:
            logger.error(e)
            logger.error('Error when parsing datetime: {}'.format(row))

            return None
        

    def create_membership_id(self, row):
        # Create membership_id for successful applications should be the user's last name, followed by a SHA256 hash of the applicant's birthday, truncated to first 5 digits of hash (i.e <last_name>_<hash(YYYYMMDD)>)
        m = sha256()
        m.update(str(row['dob']).encode('utf-8'))
        digest = m.hexdigest()
        membership_id = '{}_{}'.format(str(row['last_name']), digest[:5])

        return membership_id