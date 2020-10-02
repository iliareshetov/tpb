# import logging
#
# import psycopg2
#
# from config import DATABASE_HOST, DATABASE, USER, PASSWORD
#
#
# def insert_booking(user_id, first_name, booking_timestamp):
#     sqluser = """INSERT INTO users (user_id, first_name, create_time)
#                 VALUES(%s, %s, now())
#                 ON CONFLICT (user_id)
#                 DO NOTHING;
#             """
#
#     sqlbooking = """
#                 INSERT INTO bookings (user_id, create_time)
#                 VALUES(%s, %s) RETURNING booking_id;
#             """
#
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
#         cur.execute(sqluser, (user_id, first_name))
#         cur.execute(sqlbooking, (user_id, booking_timestamp))
#         # get the generated id back
#         inserted_id = cur.fetchone()[0]
#         # commit the changes to the database
#         conn.commit()
#         # close communication with the database
#         cur.close()
#     except (Exception, psycopg2.DatabaseError) as error:
#         logging.error("insert error", error)
#     finally:
#         if conn is not None:
#             conn.close()
#
#     return inserted_id
#
#
# def fetch_all_bookings_for_user(user_id):
#     sql = """SELECT b.create_time
#                 FROM users u
#                 INNER JOIN bookings b
#                 ON u.user_id = b.user_id
#                 WHERE u.user_id = %s
#                 ORDER BY b.booking_id;
#             """
#
#     conn = None
#     fetched_bookings = None
#     try:
#         # connect to the PostgreSQL database
#         conn = psycopg2.connect(
#             host=DATABASE_HOST,
#             database=DATABASE,
#             user=USER,
#             password=PASSWORD)
#         # create a new cursor
#         cur = conn.cursor()
#
#         cur.execute(sql, (user_id,))
#
#         fetched_bookings = cur.fetchall()
#
#         cur.close()
#     except (Exception, psycopg2.DatabaseError) as error:
#         logging.error(error)
#     finally:
#         if conn is not None:
#             conn.close()
#
#     return fetched_bookings