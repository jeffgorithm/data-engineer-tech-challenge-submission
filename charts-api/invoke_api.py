import requests
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Starting application...')

country = 'singapore'
start_date = '2020-01-23T00:00:00Z'
end_date = '2023-03-30T00:00:00Z'

logger.info('Country: {}'.format(country))
logger.info('Start Date: {}'.format(start_date))
logger.info('End Date: {}'.format(end_date))

api_url = 'https://api.covid19api.com/country/{}/status/confirmed?from={}&to={}'.format(country, start_date, end_date)

logger.info('Invoking API...')

response = requests.get(api_url)

logger.info('Response Status Code: {}'.format(response.status_code))

logger.info('Writing JSON file...')

with open('covid_cases.json', 'w') as f:
    json.dump(obj=response.json(), fp=f, indent=4)

logger.info('Complete...')
