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
CLASS_DATA = {}
CLASS_PART = {}
CLASS_CODES = {"T15": "1402",
               "T16": "1403"}
ALL_CLASSES = ["T15", "T16"]

for c in ALL_CLASSES:
    CLASS_DATA[c] = []
    CLASS_PART["participation_" + c] = []

def start(update, context):
    buttons = []
    for each_class in ALL_CLASSES:
        buttons.append([InlineKeyboardButton("Register Attendance for " + each_class, callback_data=each_class)])
        buttons.append([InlineKeyboardButton("Register Participation for " + each_class, callback_data="participation_" + each_class)])
    context.bot.send_message(chat_id=update.effective_chat.id, text="What may I do for you today?",
                             reply_markup=InlineKeyboardMarkup(buttons))

def write_to_txt(tut, type):
    if type == "T":
        file = open(tut + ".txt", "w+")
        for name in CLASS_DATA[tut]:
            file.write(name + "\n")
    else:
        file = open(tut + "Part.txt", "w+")
        for name in CLASS_PART["participation_" + tut]:
            file.write(name + "\n")

def inline_query(update, context):
    query = update.callback_query.data
    update.callback_query.answer()
    context.bot.edit_message_reply_markup(
        message_id = update.callback_query.message.message_id,
        chat_id = update.callback_query.message.chat.id,
        reply_markup=None)
    current_user[update.effective_chat.id] = {}
    if query.startswith("participation_"):
        current_user[update.effective_chat.id]['class'] = query.split("_")[1]
    else:
        current_user[update.effective_chat.id]['class'] = query
    if query.startswith("participation_"):
        current_user[update.effective_chat.id]['state'] = "participation"
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Please type in your name.")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Please type in the code followed by your name\nE.g. 1001 William Lee")

def message_handler(update, context):
    global current_user
    if current_user.get(update.effective_chat.id) is None or current_user[update.effective_chat.id].get('class') is None:
        context.bot.send_message(chat_id=update.effective_chat.id, text="If you'd like to register your attendance, please choose your class first.")
    msg = update.message.text
    curr_class = current_user[update.effective_chat.id]['class']
    if current_user[update.effective_chat.id].get('state') == "participation":
        CLASS_PART["participation_" + curr_class].append(msg)
        CLASS_PART["participation_" + curr_class].sort()
        write_to_txt(curr_class, "P")
        context.bot.send_message(chat_id=update.effective_chat.id, text=msg + " registered!")
    else:
        password = CLASS_CODES.get(curr_class)
        if password is None:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Wrong code/format, include a space after the code if you forgot to.")
        elif msg.startswith(password):
            name = msg.split(password + " ")[1]
            CLASS_DATA[curr_class].append(name)
            CLASS_DATA[curr_class].sort()
            write_to_txt(curr_class, "T")
            context.bot.send_message(chat_id=update.effective_chat.id, text=name + " registered!")
            print("Total: " + str(len(CLASS_DATA[curr_class])))

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

query_handler = CallbackQueryHandler(inline_query)
dispatcher.add_handler(query_handler)

catchall_handler = MessageHandler(Filters.text, message_handler)
dispatcher.add_handler(catchall_handler)

updater.start_polling()
updater.idle()
