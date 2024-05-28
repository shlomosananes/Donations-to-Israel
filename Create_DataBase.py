import psycopg2

HOSTNAME = 'localhost'
USERNAME = 'postgres'
PASSWORD = '07111989'

connection = psycopg2.connect(host=HOSTNAME,user=USERNAME,password=PASSWORD)

cursor = connection.cursor()
connection.autocommit = True
# connection.autocommit = True  is an alternative for writing the line connection.commit() after every query. Each statements is a TRANSACTION on its own.
# If we leave it as FALSE or UNSET, we can do multiple cursor.execute and only in the end run connection.commit() and we will be grouping multiple SQL statements
# into a single TRANSACTION.

cursor.execute("""DROP DATABASE if exists support_israel;""")
cursor.execute("""CREATE DATABASE support_israel;""")

cursor.close()
connection.close()

