"""
This module helps to interact with PostgreSQL database.
"""

__version__ = '0.1'
__author__ = 'Ilia Reshetov, Emil Khaibrakhmanov'

from services.booking_service import insert_booking, fetch_all_bookings_for_user
from services.initdb import create_tables
from services.user_service import register_user

__all__ = ('insert_booking', 'create_tables', 'fetch_all_bookings_for_user', 'register_user')
