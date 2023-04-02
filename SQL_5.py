import psycopg2


def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
        DROP TABLE client
         """)
        cur.execute("""
        DROP TABLE phone_number
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS client(
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(40) NOT NULL,
            last_name VARCHAR(40) NOT NULL,
            email VARCHAR(60) NOT NULL
        );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS phone_number(
            id SERIAL PRIMARY KEY,
            client_id INTEGER REFERENCES client(id)
            phone INTEGER NULL DEFAULT (0)
        );
        """)
        conn.commit()
    pass


def add_client(conn, first_name, last_name, email, phones=None):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO client(first_name, last_name, email) VALUES(%s, 
        %s, %s) RETURNING id;
        """)
        cur.fetchall()
    pass


def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO client(client_id, phone) VALUES(%s, 
        %s) RETURNING id;
        """)
        cur.fetchall()
    pass


def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
    with conn.cursor() as cur:
        if first_name != None:
            cur.execute("""
            UPDATE client SET name=%s WHERE id=%s;
            """,)
            cur.execute("""
            SELECT * FROM client;
            """)
            print(cur.fetchall())
    pass


def delete_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM phone_number WHERE client_id=%s;
        """)
        print(cur.fetchall())
    pass


def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM client WHERE client_id=%s;
        """)
        print(cur.fetchall())
    pass


def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    with conn.cursor() as cur:
        cur.execute("""
        SELECT first_name, last_name, email, phone FROM client c
        JOIN phone_number pn ON c.id = pn.client_id;
        """)
    print(cur.fetchall())
    pass


with psycopg2.connect(database="clients_db", user="postgres", password="postgres") as conn:
    create_db(conn)
    add_client(conn, first_name=input('Введите имя'),
               last_name=input('Введите фамилию'),
               email=input('Введите email'),
               phones=None)
    add_phone(conn, client_id=input('Введите id клиента'), phone=input('Введите номер клиента'))
    change_client(conn, client_id=input('Введите id клиента'),
                  first_name=None, last_name=None,
                  email=None, phones=None)
    delete_phone(conn, client_id=input('Введите id клиента'),
                 phone=input('Введите номер клиента'))
    delete_client(conn, client_id=input('Введите id клиента'))
    find_client(conn, first_name=None, last_name=None, email=None,
                phone=None)
    pass

conn.close()