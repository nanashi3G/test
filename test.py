#!/usr/bin/env python

import mysql.connector

USER = 'hogehoge'
HOST = 'localhost'
PASSWORD = 'hogehoge'
DATABASE_NAME = 'db1'
TABLE_NAME = 'tbl1'
CHARSET = 'utf8'

def main():
    db = mysql.connector.connect(
        user=USER,
        host=HOST,
        password=PASSWORD,
        database=DATABASE_NAME,
        charset=CHARSET
    )

    cursor = db.cursor(buffered=True)

    id = 3
    num = 3
    name = 'aaa'
    cursor.execute('insert into tbl1 values (%s, %s, %s)', (id, num, name))

    cursor.execute('select * from tbl1')

    for row in cursor.fetchall():
        print(row[0], row[1], row[2])

    cursor.close()
    db.commit()
    db.close()


if __name__ == '__main__':
    main()
