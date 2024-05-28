import psycopg2

HOSTNAME = 'localhost'
USERNAME = 'postgres'
PASSWORD = '07111989'
DATABASE = 'support_israel'

connection = psycopg2.connect(host=HOSTNAME,user=USERNAME,password=PASSWORD,dbname =DATABASE)
cursor = connection.cursor()

query = """ 
    CREATE TABLE institutions (
	    id SERIAL PRIMARY KEY,
	    name VARCHAR(50) NOT NULL,
        category VARCHAR(50) NOT NULL,
        description VARCHAR(200),
        url VARCHAR(500) NOT NULL )"""

cursor.execute(query)


query = """
    CREATE TABLE donators (
	id SERIAL PRIMARY KEY,
	name VARCHAR(50) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    country VARCHAR(25),
    city VARCHAR(25),
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(25),
    password VARCHAR(8) NOT NULL,
    CONSTRAINT check_password CHECK (CHAR_LENGTH(password) = 8)) """

cursor.execute(query)


query = """ 
    CREATE TABLE donations (
	id SERIAL PRIMARY KEY,
	donator_id INT NOT NULL,
	institution_id INT NOT NULL,
    date DATE NOT NULL,
    value INT NOT NULL,
    currency VARCHAR(3) NOT NULL,
    payment_method VARCHAR(25) NOT NULL,
    frequency VARCHAR(13) NOT NULL,
    FOREIGN KEY (donator_id) REFERENCES donators(id),
    FOREIGN KEY (institution_id) REFERENCES institutions(id),
    CONSTRAINT check_payment_method CHECK (payment_method IN ('Credit Card' , 'Direct' , 'Bank Transfer' , 'BIT')),
    CONSTRAINT check_frequency CHECK (frequency IN ('one-time gift' , 'monthly-gift')) )"""

cursor.execute(query)


connection.commit()


cursor.close()
connection.close()













