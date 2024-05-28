import psycopg2

HOSTNAME = 'localhost'
USERNAME = 'postgres'
PASSWORD = '07111989'
DATABASE = 'support_israel'

connection = psycopg2.connect(host=HOSTNAME,user=USERNAME,password=PASSWORD,dbname =DATABASE)
cursor = connection.cursor()

query = r"""
    COPY institutions (name, category, description, url)
    FROM 'C:\Users\salom\Documents\DI-Bootcamp\Hackathon1_Support_Israel\Institutions.csv'
    DELIMITER ','
    CSV HEADER ; """

cursor.execute(query)


connection.commit()


cursor.close()
connection.close()