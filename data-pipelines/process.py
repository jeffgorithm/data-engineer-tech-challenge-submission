import pandas as pd
import argparse
import os
from dateutil.parser import parse
from datetime import datetime, timedelta
from hashlib import sha256
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

    # Validate mobile_no
    dataframe['valid_mobile_no'] = dataframe['mobile_no'].apply(lambda row: validate_mobile_no(row))
    
    # Validate email
    dataframe['valid_email'] = dataframe['email'].str.match(r"^.+@.+\..{2,}$")

    # Process date
    dataframe['cleaned_date'] = dataframe['date_of_birth'].apply(lambda row: clean_date(row))
    dataframe['dob'] = pd.to_datetime(dataframe['cleaned_date'])
    date = datetime.strptime("2022-01-01", '%Y-%m-%d')
    dataframe['age_days'] = (date - dataframe['dob'])
    dataframe['above_18'] = dataframe['age_days'].apply(lambda row: is_above_18(row))
    dataframe['date_of_birth'] = dataframe['dob'].apply(lambda row: format_birthday(row))

    # Process name field
    dataframe['empty_name'] = dataframe['name'].isnull()
    dataframe['name'] = dataframe['name'].apply(lambda row: filter_salutation(row))
    dataframe['name'] = dataframe['name'].apply(lambda row: filter_title(row))
    dataframe['first_name'] = dataframe['name'].apply(lambda row: format_first_name(row))
    dataframe['last_name'] = dataframe['name'].apply(lambda row: format_last_name(row))

    # Generate membership_id
    dataframe['membership_id'] = dataframe.apply(create_membership_id, axis=1)
    dataframe['success'] = dataframe.apply(validate_applications, axis=1)

    # Separate successful and unsuccessful applications
    success_df = dataframe[dataframe['success'] == True]
    success_df.reset_index(drop=True, inplace=True)
    unsuccessful_df = dataframe[dataframe['success'] == False]
    unsuccessful_df.reset_index(drop=True, inplace=True)

    final_cols = ['first_name', 'last_name', 'date_of_birth', 'above_18', 'membership_id']

    success_output_path = os.path.join(success_dir, 'output.csv')
    unsuccessful_output_path = os.path.join(unsuccessful_dir, 'output.csv')

    success_df[final_cols].to_csv(path_or_buf=success_output_path, index=False)
    unsuccessful_df[final_cols].to_csv(path_or_buf=unsuccessful_output_path, index=False)

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

def validate_applications(row):
    if row['valid_mobile_no'] == False or row['valid_email'] == False or row['above_18'] == False or row['empty_name'] == True:
        return False
    else:
        return True

# Function that ensures that mobile_no is 8 digits
def validate_mobile_no(mobile_no):
    if len(mobile_no) == 8:
        return True
    else:
        return False

def is_above_18(row):
    # Create a new field named above_18 based on the applicant's birthday
    if row >= timedelta(days=(18 * 365)):
        return True
    else:
        return False

def filter_salutation(name):
    # Filter salutations in prefix such as Mr., Dr. etc.
    salutations = ['Mr. ', 'Dr. ', 'Ms. ', 'Mrs. ']

    for salutation in salutations:
        if salutation in name:
            new_name = name.strip(salutation)

            return new_name
    
    return name

def filter_title(name):
    # Filter titles from postfix such as MD, etc.
    titles = [' MD']

    for title in titles:
        if title in name:
            new_name = name.strip(title)

            return new_name
    
    return name

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
    # Format birthday field into YYYYMMDD
    try:
        return row.strftime('%Y%m%d')
    except Exception as e:
        logger.error(e)
        logger.error('Error when parsing datetime: {}'.format(row))

        return None
    

def create_membership_id(row):
    # Create membership_id for successful applications should be the user's last name, followed by a SHA256 hash of the applicant's birthday, truncated to first 5 digits of hash (i.e <last_name>_<hash(YYYYMMDD)>)
    m = sha256()
    m.update(str(row['dob']).encode('utf-8'))
    digest = m.hexdigest()
    membership_id = '{}_{}'.format(str(row['last_name']), digest[:5])

    return membership_id

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
    