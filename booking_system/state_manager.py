import logging

from telegram.ext import ConversationHandler

# States
from booking_system.inline_calendar import create_calendar

FIRST, SECOND, THREE = range(3)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def handle_calendar_selection(update, context):
    selected_user = update.message.text

    logging.info(f'selected_user: {selected_user}')

    update.message.reply_text(f'You selected the user: {selected_user}, please select the date ...',
                              reply_markup=create_calendar())
    return SECOND


def end(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text="See you next time!"
    )
    return ConversationHandler.END
