from telegram.ext import *
from telegram import *
import logging
import os
from dotenv import load_dotenv
load_dotenv()
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
token = os.getenv('BOT_TOKEN')
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher

current_user = {}
CLASS_1_DATA = []
CLASS_2_DATA = []

CLASS_1 = "T15"
CLASS_2 = "T16"

CLASS_1_FILENAME = "T15.txt"
CLASS_2_FILENAME = "T16.txt"

def start(update, context):
    buttons = [[InlineKeyboardButton("Register Attendance for " + CLASS_1, callback_data=CLASS_1)],
               [InlineKeyboardButton("Register Attendance for " + CLASS_2, callback_data=CLASS_2)]]
    context.bot.send_message(chat_id=update.effective_chat.id, text="What may I do for you today?",
                             reply_markup=InlineKeyboardMarkup(buttons))


def write_to_txt(tut):
    if tut == CLASS_1:
        file = open(CLASS_1_FILENAME, "w+")
        for name in CLASS_1_DATA:
            file.write(name + "\n")
    elif tut == CLASS_2:
        file = open(CLASS_2_FILENAME, "w+")
        for name in CLASS_2_DATA:
            file.write(name + "\n")


def inline_query(update, context):
    query = update.callback_query.data
    update.callback_query.answer()
    context.bot.edit_message_reply_markup(
        message_id = update.callback_query.message.message_id,
        chat_id = update.callback_query.message.chat.id,
        reply_markup=None)
    if query == CLASS_1:
        current_user[update.effective_chat.id] = {}
        current_user[update.effective_chat.id]['state'] = CLASS_1
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Please type in the code followed by your name\nE.g. 1001 William Lee")
    elif query == CLASS_2:
        current_user[update.effective_chat.id] = {}
        current_user[update.effective_chat.id]['state'] = CLASS_2
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Please type in the code followed by your name\nE.g. 1002 William Lee")

def message_handler(update, context):
    global current_user
    if current_user.get(update.effective_chat.id) is None or current_user[update.effective_chat.id].get('state') is None:
        context.bot.send_message(chat_id=update.effective_chat.id, text="If you'd like to register your attendance, please choose your class first.")
    else:
        msg = update.message.text
        if current_user[update.effective_chat.id]['state'] == CLASS_1:
            if msg.startswith("1402 "):
                name = msg.split("1402 ")[1]
                CLASS_1_DATA.append(name)
                CLASS_1_DATA.sort()
                write_to_txt(CLASS_1)
                context.bot.send_message(chat_id=update.effective_chat.id, text=name + " registered!")
                print("total: " + str(len(CLASS_1_DATA)))
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text="Wrong code/format, include a space after the code if you forgot to.")
        elif current_user[update.effective_chat.id]['state'] == CLASS_2:
            if msg.startswith("1403 "):
                name = msg.split("1403 ")[1]
                CLASS_2_DATA.append(name)
                CLASS_2_DATA.sort()
                write_to_txt(CLASS_2)
                context.bot.send_message(chat_id=update.effective_chat.id, text=name + " registered!")
                print("total: " + str(len(CLASS_2_DATA)))
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text="Wrong code/format, include a space after the code if you forgot to.")
                print("Failed input")




start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

query_handler = CallbackQueryHandler(inline_query)
dispatcher.add_handler(query_handler)

catchall_handler = MessageHandler(Filters.text, message_handler)
dispatcher.add_handler(catchall_handler)

updater.start_polling()
updater.idle()
