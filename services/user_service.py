# import logging
# import datetime
# import psycopg2
# import pytz
#
# from config import DATABASE_HOST, DATABASE, USER, PASSWORD
#
# tz = pytz.timezone('Europe/Helsinki')
#
#
# def register_user(user_id, first_name, is_bot, language_code):
#     now = datetime.datetime.now(tz=tz)
#
#     sql = """INSERT INTO users (user_id, first_name, is_bot, language_code, create_time, interaction_counter, interaction_last_time)
#                 VALUES(%s, %s, %s, %s, %s, %s, %s)
#                 ON CONFLICT (user_id)
#                 DO NOTHING
#                 RETURNING user_id;
#             """
#     conn = None
#     inserted_id = None
#     try:
#         # connect to the PostgreSQL database
#         conn = psycopg2.connect(
#             host=DATABASE_HOST,
#             database=DATABASE,
#             user=USER,
#             password=PASSWORD)
#         # create a new cursor
#         cur = conn.cursor()
#         # execute the INSERT statement
#         cur.execute(sql, (user_id, first_name, is_bot, language_code, now, 1, now))
#         # get the generated id back
#         inserted_id = cur.fetchone()[0]
#         # commit the changes to the database
#         conn.commit()
#         # close communication with the database
#         cur.close()
#     except (Exception, psycopg2.DatabaseError) as error:
#         logging.error(error)
#     finally:
#         if conn is not None:
#             conn.close()
#
#     return inserted_id
