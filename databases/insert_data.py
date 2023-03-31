from sqlalchemy import create_engine
from sqlalchemy.engine import URL

def read_data(path):
    data = []

    with open(path, 'r') as f:
        for line in f.readlines():
            split = line.strip('\n').split(',')
            data.append(split)

    f.close()

    return data

data = read_data('data/members.csv')

url = URL.create(
    drivername='postgresql',
    username='postgres',
    password='postgres',
    database="postgres",
    host='127.0.0.1',
    port=5432
)

db = create_engine(url)

for record in data:
    db.execute(
        'INSERT INTO members (membership_id, first_name, last_name, email, date_of_birth, mobile_no, above_18) VALUES (\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\')'.format(record[0],record[1],record[2],record[3],record[4],record[5],record[6])
        )
    
print('Insertion to members table complete')