import logging

import psycopg2

from config import DATABASE_HOST, DATABASE, USER, PASSWORD


def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id bigint PRIMARY KEY,
            username text,
            first_name text NOT NULL,
            is_bot boolean,
            language_code text NOT NULL, 
            create_time timestamp NOT NULL,
            interaction_counter bigint,
            interaction_last_time timestamp NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS bookings (
            booking_id SERIAL PRIMARY KEY,
            user_id bigint NOT NULL,
            create_time timestamp NOT NULL,
            CONSTRAINT fk_user
                FOREIGN KEY(user_id) 
	            REFERENCES users(user_id)
	            ON DELETE CASCADE
	            ON UPDATE CASCADE
        )
        """,
    )
    conn = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(
            host=DATABASE_HOST,
            database=DATABASE,
            user=USER,
            password=PASSWORD)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error("db error", error)
    finally:
        if conn is not None:
            conn.close()
