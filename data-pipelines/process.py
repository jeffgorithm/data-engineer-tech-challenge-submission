import pandas as pd
import argparse
import os
from dateutil.parser import parse
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process(input_dir, success_dir, unsuccessful_dir):
    files = os.listdir(path=input_dir)

    dataframe = pd.DataFrame()

    for file in files:
        file_path = os.path.join(input_dir, file)
        df = pd.read_csv(
            filepath_or_buffer=file_path
            )
        
        dataframe = pd.concat([dataframe, df])

    dataframe['valid_mobile_no'] = dataframe['mobile_no'].apply(lambda row: validate_mobile_no(row))
    dataframe['valid_email'] = dataframe['email'].str.match(r"^.+@.+\..{2,}$")
    dataframe['cleaned_date'] = dataframe['date_of_birth'].apply(lambda row: clean_date(row))
    dataframe['dob'] = pd.to_datetime(dataframe['cleaned_date'])
    date = datetime.strptime("2022-01-01", '%Y-%m-%d')
    dataframe['age'] = (date - dataframe['dob'])
    dataframe['empty_name'] = dataframe['name'].isnull()
    dataframe['first_name'] = dataframe['name'].apply(lambda row: format_first_name(row))
    dataframe['last_name'] = dataframe['name'].apply(lambda row: format_last_name(row))

    print(dataframe.head())

    output_path = os.path.join(success_dir, 'output.csv')
    dataframe.to_csv(output_path)

def clean_date(date):
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

# Function that ensures that mobile_no is 8 digits
def validate_mobile_no(mobile_no):
    if len(mobile_no) == 8:
        return True
    else:
        return False
    
def validate_age(row):
    # TODO: Validate age
    # Applicant is over 18 years old as of 1 Jan 2022
    pass

def filter_salutation(name):
    # TODO: Filter salutations such as Mr., Dr. etc.
    pass

# Function to extract first_name from name
def format_first_name(name):
    # Split name into first_name 
    split = name.split(' ')

    if len(split) >= 1:
        return split[0]
    else:
        return None
    
# Function to extract last_name from name
def format_last_name(name):
    # Split name into last_name
    split = name.split(' ')

    if len(split) >= 1:
       return ' '.join(split[1:len(split)])
    else:
        return None

def format_birthday(row):
    # TODO: Format birthday field into YYYYMMDD
    pass

def is_above_18(row):
    # TODO: Create a new field named above_18 based on the applicant's birthday
    pass

def create_membership_id(row):
    # TODO: Membership IDs for successful applications should be the user's last name, followed by a SHA256 hash of the applicant's birthday, truncated to first 5 digits of hash (i.e <last_name>_<hash(YYYYMMDD)>)
    pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                        prog='Membership Data Pipeline',
                        description='Process membership data from input folder and writes to output directory'
                        )
    
    parser.add_argument(
        '--input_dir', 
        required=True
        )
    parser.add_argument(
        '--success_dir', 
        required=True
        )
    
    parser.add_argument(
        '--unsuccessful_dir', 
        required=True
        )

    args = parser.parse_args()

    process(
        input_dir=args.input_dir,
        success_dir=args.success_dir,
        unsuccessful_dir=args.unsuccessful_dir
        )
    