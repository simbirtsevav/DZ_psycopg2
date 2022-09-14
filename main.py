import psycopg2

def connect():
    conn = psycopg2.connect(database='dz5_db', user='postgres',  password='admin')
    return conn
def db_create():
    conn = connect()
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS client(
        client_id SERIAL PRIMARY KEY,
        client_name VARCHAR(30) NOT NULL,
        client_surname VARCHAR(30) NOT NULL,
        client_mail VARCHAR(60) UNIQUE
        );
        
        CREATE TABLE IF NOT EXISTS phone(
        phone_id SERIAL PRIMARY KEY,
        phone_number INTEGER UNIQUE,
        client_id INTEGER REFERENCES client(client_id)
        );
        """)
        conn.commit()
    conn.close()


def new_client(name, surname, mail, phone=None):
    conn = connect()
    with conn.cursor() as cur:
        cur.execute(f" INSERT INTO client (client_name, client_surname, client_mail) VALUES( '{name}', '{surname}', '{mail}') RETURNING client_id;")
        id = cur.fetchone()
        conn.commit()
    if phone is not None:
        with conn.cursor() as cur:
            cur.execute(f" INSERT INTO phone (phone_number, client_id) VALUES ('{phone}', '{id[0]}');")
            conn.commit()
    conn.close()


def new_phone(id, phone):
    conn = connect()
    with conn.cursor() as cur:
        cur.execute(f" INSERT INTO phone (phone_number, client_id) VALUES ('{phone}', '{id}');")
        conn.commit()
    conn.close()


def new_clientdata(id, name=None, surname=None, mail=None, phone=None):
    conn = connect()
    with conn.cursor() as cur:
        if mail is not None:
            cur.execute(f"UPDATE client SET client_name='{name}',  client_surname='{surname}', client_mail='{mail}' WHERE client_id = '{id}';")
        else:
            cur.execute(f"UPDATE client SET client_name='{name}',  client_surname='{surname}' WHERE client_id = '{id}';")
        if phone is not None:
            cur.execute(f" INSERT INTO phone (phone_number, client_id) VALUES ('{phone}', '{id}');")
    conn.commit()
    conn.close()


def delete_phone(id, phone):
    conn = connect()
    with conn.cursor() as cur:
        cur.execute(f"DELETE FROM phone WHERE client_id='{id}' AND phone_number='{phone}';")
    conn.commit()
    conn.close()


def delete_client(id):
    conn = connect()
    with conn.cursor() as cur:
        cur.execute(f" DELETE FROM phone WHERE client_id='{id}'")
        cur.execute(f"DELETE FROM client WHERE client_id='{id}'")
    conn.commit()
    conn.close()


def find_client(name=None, surname=None, mail=None, phone=None):
    conn = connect()
    with conn.cursor() as cur:
        if mail is not None:
            cur.execute("""SELECT client_id, client_name, client_surname FROM client
            WHERE client_mail=%s""", (mail,))
            print(cur.fetchone())
        elif phone is not None:
            cur.execute("""SELECT client.client_id, client_name, client_surname FROM client
            JOIN phone ON phone.client_id=client.client_id
            WHERE phone_number=%s;
                        """, (phone,))
            print(cur.fetchone())
        elif name is not None and surname is not None:
            cur.execute("""SELECT client_id, client_name, client_surname FROM client 
            WHERE client_name=%s and client_surname=%s""", (name, surname))
            print(cur.fetchone())
        elif name is not None:
            cur.execute("""SELECT client_id, client_name, client_surname FROM client
            WHERE client_name=%s""", (name,))
            print(cur.fetchall())
        else:
            cur.execute("""SELECT client_id, client_name, client_surname FROM client
            WHERE client_surname=%s""", (surname,))
            print(cur.fetchall())
    conn.close()



# db_create()
# new_client('alex', 'petrov', 'mail@mail1', '111')
# new_client('ivan', 'ivanov', 'mail@mail2', '222')
# new_client('petr', 'petrov', 'mail@mail3', '333')
# new_phone('2', '1237')
# new_clientdata(id=2, name='alex', surname='alexeev',mail='mail@mail.ru', phone='345')
# delete_phone('2', '222')
# delete_client('3')
find_client(phone='345')
find_client(mail='mail@mail1')
find_client(surname='alexeev')
find_client(name='alex')


