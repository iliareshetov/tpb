import os

import requests
import datetime
import json
from scheduler import book_timeslot
import re
# from telegram import InlineKeyboardButton, InlineKeyboardMarkup
# from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
# import logging

# from booking_system import inline_handler, get_users_bookings, calendar_handler
from config import TELEGRAM_KEY
# from services import create_tables, register_user
#
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
# logger = logging.getLogger(__name__)

def check_email(email):
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if (re.search(regex, email)):
        print("Valid Email")
        return True
    else:
        print("Invalid Email")
        return False

# Stages
# FIRST, SECOND = range(2)
# # Callback data
# ONE, TWO, THREE, FOUR = range(4)


# def start(update, context):
#     menu = '/newbooking - забронировать время в сервисе \n' \
#            '/showhistory - посмотреть историю бронирований';
#     context.bot.send_message(chat_id=update.effective_chat.id, text=menu)
#     user = update.message.from_user
#
#     logging.info(f'Start : {update}')
#     logging.info(f'Start will register new user: {user}')
#
#     inserted_id = register_user(user.id, user.first_name, user.is_bot, user.language_code)
#     logging.info(f'Start inserted user with id: {inserted_id}')

# def start(update, context):
#     """Send message on `/start`."""
#     # Get user that sent /start and log his name
#     user = update.message.from_user
#     logger.info("User %s started the conversation.", user.first_name)
    # Build InlineKeyboard where each button has a displayed text
    # and a string as callback_data
    # The keyboard is a list of button rows, where each row is in turn
    # a list (hence `[[...]]`).
    # keyboard = [
    #     [InlineKeyboardButton("1", callback_data=str(ONE)),
    #      InlineKeyboardButton("2", callback_data=str(TWO))]
    # ]
    # reply_markup = InlineKeyboardMarkup(keyboard)
    # # Send message with text and appended InlineKeyboard
    # update.message.reply_text(
    #     "Start handler, Choose a route",
    #     reply_markup=reply_markup
    # )
    # Tell ConversationHandler that we're in state `FIRST` now
    # return FIRST


# def start_over(update, context):
#     """Prompt same text & keyboard as `start` does but not as new message"""
#     # Get CallbackQuery from Update
#     query = update.callback_query
#     # CallbackQueries need to be answered, even if no notification to the user is needed
#     # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
#     query.answer()
#     keyboard = [
#         [InlineKeyboardButton("1", callback_data=str(ONE)),
#          InlineKeyboardButton("2", callback_data=str(TWO))]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     # Instead of sending a new message, edit the message that
#     # originated the CallbackQuery. This gives the feeling of an
#     # interactive menu.
#     query.edit_message_text(
#         text="Start handler, Choose a route",
#         reply_markup=reply_markup
#     )
#     return FIRST
#
#
# def one(update, context):
#     """Show new choice of buttons"""
#     query = update.callback_query
#     query.answer()
#     keyboard = [
#         [InlineKeyboardButton("3", callback_data=str(THREE)),
#          InlineKeyboardButton("4", callback_data=str(FOUR))]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     query.edit_message_text(
#         text="First CallbackQueryHandler, Choose a route",
#         reply_markup=reply_markup
#     )
#     return FIRST
#
#
# def two(update, context):
#     """Show new choice of buttons"""
#     query = update.callback_query
#     query.answer()
#     keyboard = [
#         [InlineKeyboardButton("1", callback_data=str(ONE)),
#          InlineKeyboardButton("3", callback_data=str(THREE))]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     query.edit_message_text(
#         text="Second CallbackQueryHandler, Choose a route",
#         reply_markup=reply_markup
#     )
#     return FIRST
#
#
# def three(update, context):
#     """Show new choice of buttons"""
#     query = update.callback_query
#     query.answer()
#     keyboard = [
#         [InlineKeyboardButton("Yes, let's do it again!", callback_data=str(ONE)),
#          InlineKeyboardButton("Nah, I've had enough ...", callback_data=str(TWO))]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     query.edit_message_text(
#         text="Third CallbackQueryHandler. Do want to start over?",
#         reply_markup=reply_markup
#     )
#     # Transfer to conversation state `SECOND`
#     return SECOND
#
#
# def four(update, context):
#     """Show new choice of buttons"""
#     query = update.callback_query
#     query.answer()
#     keyboard = [
#         [InlineKeyboardButton("2", callback_data=str(TWO)),
#          InlineKeyboardButton("4", callback_data=str(FOUR))]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     query.edit_message_text(
#         text="Fourth CallbackQueryHandler, Choose a route",
#         reply_markup=reply_markup
#     )
#     return FIRST
#
#
# def end(update, context):
#     """Returns `ConversationHandler.END`, which tells the
#     ConversationHandler that the conversation is over"""
#     query = update.callback_query
#     query.answer()
#     query.edit_message_text(
#         text="See you next time!"
#     )
#     return ConversationHandler.END
# def main():
def getLastMessage():
    url = "https://api.telegram.org/bot{}/getUpdates".format(TELEGRAM_KEY)
    response = requests.get(url)
    data = response.json()
    last_msg = data['result'][len(data['result']) - 1]['message']['text']
    chat_id = data['result'][len(data['result']) - 1]['message']['chat']['id']
    update_id = data['result'][len(data['result']) - 1]['update_id']
    if len(data['result']) < 100:
        return last_msg, chat_id, update_id
    else:
        print('offseting updates limit...')
        url = "https://api.telegram.org/bot{}/getUpdates?offset={}".format(TELEGRAM_KEY, update_id)
        response = requests.get(url)
        data = response.json()
        last_msg = data['result'][len(data['result']) - 1]['message']['text']
        chat_id = data['result'][len(data['result']) - 1]['message']['chat']['id']
        update_id = data['result'][len(data['result']) - 1]['update_id']
        return last_msg, chat_id, update_id

def sendMessage(chat_id, text_message):
    url = 'https://api.telegram.org/bot' + str(TELEGRAM_KEY) + '/sendMessage?text=' + str(
        text_message) + '&chat_id=' + str(
        chat_id)
    response = requests.get(url)
    return response

def sendInlineMessageForService(chat_id):
    text_message = 'zdarova loh'
    keyboard = {'keyboard': [
        [{'text': 'strizhka'}, {'text': 'huizhka'}],
        [{'text': 'kocherizhka'}, {'text': 'yahzesheche'}]
    ]}
    key = json.JSONEncoder().encode(keyboard)
    url = 'https://api.telegram.org/bot' + str(TELEGRAM_KEY) + '/sendmessage?chat_id=' + str(chat_id) + '&text=' + str(
        text_message) + '&reply_markup=' + key
    response = requests.get(url)
    return response

def sendInlineMessageForBookingTime(chat_id):
    text_message = 'Please choose a time slot...'
    current_time = datetime.datetime.now()
    current_hour = str(current_time)[11:13]
        # ----------- Chunk of if statement to determine which inline keyboard to reply user ----------------
    if int(current_hour) < 8:
        keyboard = {'keyboard': [
            [{'text': '08:00'}], [{'text': '10:00'}],
            [{'text': '12:00'}], [{'text': '14:00'}],
            [{'text': '16:00'}], [{'text': '18:00'}],
        ]}
    elif 8 <= int(current_hour) < 10:
        keyboard = {'keyboard': [
            [{'text': '10:00'}],
            [{'text': '12:00'}], [{'text': '14:00'}],
            [{'text': '16:00'}], [{'text': '18:00'}],
        ]}
    elif 10 <= int(current_hour) < 12:
        keyboard = {'keyboard': [
            [{'text': '12:00'}], [{'text': '14:00'}],
            [{'text': '16:00'}], [{'text': '18:00'}],
        ]}
    elif 12 <= int(current_hour) < 14:
        keyboard = {'keyboard': [
            [{'text': '14:00'}],
            [{'text': '16:00'}], [{'text': '18:00'}],
        ]}
    elif 14 <= int(current_hour) < 16:
        keyboard = {'keyboard': [
            [{'text': '16:00'}], [{'text': '18:00'}],
        ]}
    elif 16 <= int(current_hour) < 24:
        keyboard = {'keyboard': [
            [{'text': '19:00'}],
        ]}
    else:
        return sendMessage(chat_id, 'poprobui snova ili idi nahui')
        # ----------------------------------------------------------------------------------------------------
    key = json.JSONEncoder().encode(keyboard)
    url = 'https://api.telegram.org/bot' + str(TELEGRAM_KEY) + '/sendmessage?chat_id=' + str(chat_id) + '&text=' + str(
        text_message) + '&reply_markup=' + key
    response = requests.get(url)
    return response

def main():
    update_id_for_booking_of_time_slot = ''
    prev_last_msg, chat_id, prev_update_id = getLastMessage()
    while True:
        current_last_msg, chat_id, current_update_id = getLastMessage()
        if prev_last_msg == current_last_msg and current_update_id == prev_update_id:
            print('continue')
            continue
        else:
            if current_last_msg == '/start':
                sendInlineMessageForService(chat_id)
            if current_last_msg in ['Cut', 'strizhka', 'huizhka', 'otrizhka']:
                event_description = current_last_msg
                sendInlineMessageForBookingTime(chat_id)
            if current_last_msg in ['08:00', '10:00', '12:00', '14:00', '16:00', '18:00']:
                booking_time = current_last_msg
                update_id_for_booking_of_time_slot = current_update_id
                sendMessage(chat_id, "Please enter email address:")
            if current_last_msg == '/cancel':
                sendMessage(chat_id, "Please try another timeslot and try again tomorrow")
                break
                    # return
                continue
            if update_id_for_booking_of_time_slot != current_update_id and update_id_for_booking_of_time_slot != '':
                if check_email(current_last_msg) == True:
                    update_id_for_booking_of_time_slot = ''
                    sendMessage(chat_id, "Booking please wait.....")
                    input_email = current_last_msg
                    response = book_timeslot(event_description, booking_time, input_email)
                    if response == True:
                        sendMessage(chat_id, f"Appointment is booked.See you at {booking_time}")
                        continue
                    else:
                        update_id_for_booking_of_time_slot = ''
                        sendMessage(chat_id, "Please try another timeslot and try again tomorrow")
                        continue
                else:
                    sendMessage(chat_id,
                                    "Please enter a valid email.\nEnter /cancel to quit chatting with the bot\nThanks!")

        prev_last_msg = current_last_msg
        prev_update_id = current_update_id

# def main():

    # create_tables()
    #
    # updater = Updater(token=TELEGRAM_KEY, use_context=True)
    #
    # # Setup conversation handler with the states FIRST and SECOND
    # # Use the pattern parameter to pass CallbackQueries with specific
    # # data pattern to the corresponding handlers.
    # # ^ means "start of line/string"
    # # $ means "end of line/string"
    # # So ^ABC$ will only allow 'ABC'
    # conv_handler = ConversationHandler(
    #     entry_points=[CommandHandler('start', start)],
    #     states={
    #         FIRST: [CallbackQueryHandler(one, pattern='^' + str(ONE) + '$'),
    #                 CallbackQueryHandler(two, pattern='^' + str(TWO) + '$'),
    #                 CallbackQueryHandler(three, pattern='^' + str(THREE) + '$'),
    #                 CallbackQueryHandler(four, pattern='^' + str(FOUR) + '$')],
    #         SECOND: [CallbackQueryHandler(start_over, pattern='^' + str(ONE) + '$'),
    #                  CallbackQueryHandler(end, pattern='^' + str(TWO) + '$')]
    #     },
    #     fallbacks=[CommandHandler('start', start)],
    #     per_message=True,
    # )

    # add handlers
    # start_handler = CommandHandler('start', start)
    # updater.dispatcher.add_handler(start_handler)
    #
    # echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    # updater.dispatcher.add_handler(echo_handler)
    #
    # new_booking_handler = CommandHandler('newbooking', calendar_handler)
    # updater.dispatcher.add_handler(new_booking_handler)
    #
    # show_history_handler = CommandHandler('showhistory', get_users_bookings)
    # updater.dispatcher.add_handler(show_history_handler)
    # #
    # updater.dispatcher.add_handler(CallbackQueryHandler(inline_handler))
    #
    # updater.dispatcher.add_handler(conv_handler)
    #
    # port = int(os.environ.get('PORT', '8443'))

    # Start the Bot
    # updater.start_webhook(listen="0.0.0.0",
    #                       port=port,
    #                       url_path=TELEGRAM_KEY)
    # updater.bot.set_webhook("https://throw-shade-bot.herokuapp.com/" + TELEGRAM_KEY)

    # updater.start_polling()
    #
    # logging.info('Bot is running on ...')

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    # updater.idle()
