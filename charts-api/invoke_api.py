import requests
import json

country = 'singapore'

start_date = '2020-01-23T00:00:00Z'
end_date = '2023-03-30T00:00:00Z'

api_url = 'https://api.covid19api.com/country/{}/status/confirmed?from={}&to={}'.format(country, start_date, end_date)

response = requests.get(api_url)

with open('covid_cases.json', 'w') as f:
    json.dump(obj=response.json(), fp=f, indent=4)

