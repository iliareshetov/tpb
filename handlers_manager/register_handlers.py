import os

from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler
import logging

from booking_system import FIRST, inline_handler
from booking_system.state_manager import handle_calendar_selection, SECOND
from config import TELEGRAM_KEY
from services import create_tables, register_user, get_all_users

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context):
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)

    logging.info(f'Start will register new user: {user}')

    # inserted_id = register_user(user.id, user.first_name, user.is_bot, user.language_code)
    # logging.info(f'Start inserted user with id: {inserted_id}')

    list_users = get_all_users()
    logging.info(f'Fetch all users: {list_users}')

    menu_keyboard = list_users
    menu_markup = ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=False, resize_keyboard=True)

    update.message.reply_text(
        "Choose a user",
        reply_markup=menu_markup
    )
    # Tell ConversationHandler that we're in state `FIRST` now
    return FIRST


def echo(update, context):
    logging.info(f'echo update: {update}, context: {context}')
    update.message.reply_text(update.message.text)


def main():
    create_tables()

    updater = Updater(token=TELEGRAM_KEY, use_context=True)

    # Setup conversation handler with the states FIRST and SECOND
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FIRST: [MessageHandler(Filters.text & (~Filters.command), handle_calendar_selection)],
            SECOND: [MessageHandler(Filters.text & (~Filters.command), handle_calendar_selection)],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    updater.dispatcher.add_handler(conv_handler)

    updater.dispatcher.add_handler(CallbackQueryHandler(inline_handler))

    port = int(os.environ.get('PORT', '8443'))

    # Start the Bot
    # updater.start_webhook(listen="0.0.0.0",
    #                       port=port,
    #                       url_path=TELEGRAM_KEY)
    # updater.bot.set_webhook("https://throw-shade-bot.herokuapp.com/" + TELEGRAM_KEY)

    updater.start_polling()

    logging.info('Bot is running on ...')

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()
