#!/usr/bin/env python

import mysql.connector
import time

#USER = 'root'
#PASSWORD = 'root'
USER = 'hogehoge'
PASSWORD = 'hogehoge'
HOST = 'localhost'
PORT = 3306
DATABASE_NAME = 'signage_db'
CHARSET = 'utf8'
TABLE_NAME = 'ad'
#TABLE_NAME = 'age_gender'
#TABLE_NAME = None

class SignageDb():
    def __init__(self, tbl):
        self.db = mysql.connector.connect(
            user=USER,
            host=HOST,
            password=PASSWORD,
            database=DATABASE_NAME,
            charset=CHARSET
        )
        self.cursor = self.db.cursor(buffered=True)
        self.tbl = tbl

    def read(self):
        self.cursor.execute('select * from ' +  self.tbl)
        for row in self.cursor.fetchall():
            print(row)

    def delete(self):
        self.cursor.execute('delete from ' + self.tbl)

    def commit(self):
        self.db.commit()

    def close(self):
        self.cursor.close()
        self.db.commit()
        self.db.close()

    def write_age_gender(self, gender, age):
        if age < 18:
            age_class = 0
        elif age < 65:
            age_class = 1
        else:
            age_class = 2

        datetime = time.strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute('insert into age_gender (created_at, gender, age) values (%s, %s, %s)', (datetime, gender, age_class))
    
    def write_ad(self, ad_id):
        datetime = time.strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute('insert into ad (created_at, ad_id) values (%s, %s)', (datetime, ad_id))

    def write_rule(self, id1, id2, id3, id4, id5, id6):
        datetime = time.strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute('insert into rule (created_at, m_0, f_0, m_1, f_1, m_2, f_2) values (%s, %s, %s, %s, %s, %s, %s)', (datetime, id1, id2, id3, id4, id5, id6))

    def create_tbl_ad(self):
        self.cursor.execute('create table ad (id int not null auto_increment primary key, created_at datetime, ad_id varchar(128))');

    def create_tbl_age_gender(self):
        self.cursor.execute('create table age_gender(id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, created_at datetime, gender char(1), age tinyint unsigned)')

    def create_tbl_rule(self):
        self.cursor.execute('create table rule(id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, created_at datetime, m_0 varchar(128), f_0  varchar(128), m_1  varchar(128), f_1  varchar(128), m_2  varchar(128), f_2  varchar(128))')



def test_age_gender():
    global db
    db.write_age_gender('F', 22)

def test_ad():
    global db
    db.write_ad('db-bbadfasdf')

def test_rule():
    global db
    m_0 = 'KNST_AtBb8I'             # Switch
    f_0 = 'KNST_AtBb8I'             # Switch
    m_1 = '3IH7iJjMz7sgPFATtFgZgU'  # Gillete
    f_1 = 'GKQGJ9CjUZk'             # Shiseido
    m_2 = 'O6moWDnQRms'             # kaigo
    f_2 = 'O6moWDnQRms'             # kaigo
    db.write_rule(m_0, f_0, m_1, f_1, m_2, f_2)

if __name__ == '__main__':
    global db

    db = SignageDb('ad')
    #db.create_tbl_ad()
    test_ad()

    #db = SignageDb('age_gender')
    #db.create_tbl_age_gender()
    #test_age_gender()

    #db = SignageDb('rule')
    #db.create_tbl_rule()
    #test_rule()

    db.read()
    db.close()
