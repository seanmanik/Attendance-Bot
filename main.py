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
t15 = []
t16 = []

def start(update, context):
    buttons = [[InlineKeyboardButton("Register Attendance for T15", callback_data="t15")],
               [InlineKeyboardButton("Register Attendance for T16", callback_data="t16")]]
    context.bot.send_message(chat_id=update.effective_chat.id, text="What may I do for you today?",
                             reply_markup=InlineKeyboardMarkup(buttons))


def write_to_txt(tut):
    if tut == "t15":
        filet15 = open("T15.txt", "w+")
        for name in t15:
            filet15.write(name + "\n")
    elif tut == "t16":
        filet16 = open("T16.txt", "w+")
        for name in t16:
            filet16.write(name + "\n")


def inline_query(update, context):
    query = update.callback_query.data
    update.callback_query.answer()
    context.bot.edit_message_reply_markup(
        message_id = update.callback_query.message.message_id,
        chat_id = update.callback_query.message.chat.id,
        reply_markup=None)
    if query == "t15":
        current_user[update.effective_chat.id] = {}
        current_user[update.effective_chat.id]['state'] = "t15"
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Please type in the code followed by your name\nE.g. 1402 William Lee")
    elif query == "t16":
        current_user[update.effective_chat.id] = {}
        current_user[update.effective_chat.id]['state'] = "t16"
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Please type in the code followed by your name\nE.g. 1403 William Lee")

def message_handler(update, context):
    global current_user
    if current_user.get(update.effective_chat.id) is None or current_user[update.effective_chat.id].get('state') is None:
        context.bot.send_message(chat_id=update.effective_chat.id, text="If you'd like to register your attendance, please choose your class first.")
    else:
        msg = update.message.text
        if current_user[update.effective_chat.id]['state'] == "t15":
            if msg.startswith("1402 "):
                name = msg.split("1402 ")[1]
                t15.append(name)
                t15.sort()
                write_to_txt("t15")
                context.bot.send_message(chat_id=update.effective_chat.id, text=name + " registered!")
                print(name + ", total: " + str(len(t15)))
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text="Wrong code/format, include a space after the code if you forgot to.")
        elif current_user[update.effective_chat.id]['state'] == "t16":
            if msg.startswith("1403 "):
                name = msg.split("1403 ")[1]
                t16.append(name)
                t16.sort()
                write_to_txt("t16")
                context.bot.send_message(chat_id=update.effective_chat.id, text=name + " registered!")
                print(name + ", total: " + str(len(t16)))
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text="Wrong code/format, include a space after the code if you forgot to.")




start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

query_handler = CallbackQueryHandler(inline_query)
dispatcher.add_handler(query_handler)

catchall_handler = MessageHandler(Filters.text, message_handler)
dispatcher.add_handler(catchall_handler)

updater.start_polling()
updater.idle()
