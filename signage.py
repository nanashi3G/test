#!/usr/bin/env python

import mysql.connector
import time

USER = 'hogehoge'
HOST = 'localhost'
PASSWORD = 'hogehoge'
DATABASE_NAME = 'signage_db'
TABLE_NAME = 'age_gender'
CHARSET = 'utf8'

class SignageDb():
    def __init__(self):
        self.db = mysql.connector.connect(
            user=USER,
            host=HOST,
            password=PASSWORD,
            database=DATABASE_NAME,
            charset=CHARSET
        )
        self.cursor = self.db.cursor(buffered=True)

    def write(self, gender, age):
        datetime = time.strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute('insert into age_gender (created_at, gender, age) values (%s, %s, %s)', (datetime, gender, age))
    
    def read(self):
        self.cursor.execute('select * from age_gender')
        for row in self.cursor.fetchall():
            print(row)

    def delete(self):
        self.cursor.execute('delete from age_gender')

    def commit(self):
        self.db.commit()

    def close(self):
        self.cursor.close()
        self.db.commit()
        self.db.close()

def test():
    aa = SignageDb()
    aa.write('F', 22)
    aa.read()
    aa.close()

if __name__ == '__main__':
    test()
