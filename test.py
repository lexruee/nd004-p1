#!/usr/bin/env python

import psycopg2

db = psycopg2.connect(dbname='news')
cursor = db.cursor()
cursor.execute('select * from articles;')

rows = cursor.fetchall()
for row in rows:
	print(row)
