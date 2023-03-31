from sqlalchemy import create_engine
from sqlalchemy.engine import URL

url = URL.create(
    drivername='postgresql',
    username='postgres',
    password='postgres',
    database="postgres",
    host='127.0.0.1',
    port=5432
)

db = create_engine(url)

# 'Dixon_c5222','William','Dixon','test@mail.com','19861001','12345678',True

db.execute(
    'INSERT INTO members (membership_id, first_name, last_name, email, date_of_birth, mobile_no, above_18) VALUES (\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\')'.format('Dixon_c5222','William','Dixon','test@mail.com','19861001','12345678',str(True))
    )

'''
db.execute(
    'INSERT INTO members (membership_id, first_name, last_name, email, date_of_birth, mobile_no, above_18) VALUES ({}, {}, {}, {}, {}, {}, {})'.format()
    )
'''