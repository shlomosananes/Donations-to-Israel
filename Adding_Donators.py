import psycopg2

HOSTNAME = 'localhost'
USERNAME = 'postgres'
PASSWORD = '07111989'
DATABASE = 'support_israel'

connection = psycopg2.connect(host=HOSTNAME,user=USERNAME,password=PASSWORD,dbname =DATABASE)
cursor = connection.cursor()

query = r"""
    INSERT INTO donators (name, last_name, country, city, email, phone, password) VALUES
    ('Shlomo' , 'Sananes' , 'Israel' , 'Tel Aviv' , 'shlomo.sananes@gmail.com' , '+972525963020' , '11111111'),
    ('Rachel' , 'Timstit' , 'Israel' , 'Rehovot' , 'rachel.timstit@gmail.com' , '+972505005050' , '22222222'),
    ('Shaul' , 'Morel' , 'Israel' , 'Harish' , 'shaul.morel@gmail.com' , '+972525205252' , '33333333'),
    ('Raissa' , 'Bogomoltz' , 'New Zealand' , 'Auckland' , 'raissa.bogomoltz@gmail.com' , '+6498765432' , '44444444'),
    ('Daniel' , 'Rascovschi' , 'Brazil' , 'Belem' , 'daniel.racovschi@gmail.com' , '+5591988889977' , '55555555'),
    ('Ian' , 'Diesendruck' , 'Brazil' , 'Sao Paulo' , 'diesendruck.ian@gmail.com' , '+5511977668899' , '66666666'),
    ('Marina' , 'Oren' , 'United States' , 'Dalas' , 'marina_oren@gmail.com' , '+2145596993' , '77777777') ; """

cursor.execute(query)

connection.commit()

cursor.close()
connection.close()