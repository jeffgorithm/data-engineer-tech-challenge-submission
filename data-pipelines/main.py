import argparse
import logging
from extract import Extract
from transform import Transform
from load import Load

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main(input_dir, success_dir, unsuccessful_dir):
    extractor = Extract(input_dir=input_dir)
    df = extractor.extract_data()

    transformer = Transform()
    success_df, unsuccessful_df = transformer.transform(df=df)

    loader = Load(
        success_dir=success_dir,
        unsuccessful_dir=unsuccessful_dir
        )
    
    loader.load(df=success_df)
    loader.load(df=unsuccessful_df, dest='unsuccess')


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

    main(
        input_dir=args.input_dir,
        success_dir=args.success_dir,
        unsuccessful_dir=args.unsuccessful_dir
        )
    