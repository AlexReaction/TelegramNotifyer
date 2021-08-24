from telegram.ext import Updater
from telegram.ext import CommandHandler
import logging
from telegram.ext import MessageHandler, Filters
import databaseConnector
import globals
from mysql.connector import IntegrityError

updater = Updater(token=globals.API_TOKEN, use_context=True)

dispatcher = updater.dispatcher

savedURLS = []


def start(update, context):
    splitted_message = update.message.text.split(" ")
    print(f"Url: {splitted_message}");
    if len(splitted_message) != 2:
        context.bot.send_message(update.effective_chat.id, "Wrong input!")
    else:
        url = splitted_message[1]
        if url not in savedURLS:
            print(f"Saving new url: {url}")
            databaseConnector.insertAddress(url, chatID=update.effective_chat.id)
            print("Url saved!")
            savedURLS.append(url)
            context.bot.send_message(chat_id=update.effective_chat.id,text="Added: " + url + " to your notify list.")
        else:
            try:
                databaseConnector.updateSubscribedChat(url, chatID=update.effective_chat.id)
                print("Added new subscriber")
                context.bot.send_message(chat_id=update.effective_chat.id,text="Added: " + url + " to your notify list.")

            except IntegrityError:
                print("Error occurred")
                context.bot.send_message(chat_id=update.effective_chat.id, text=url + " is already subscribed")

            except ValueError:
                print("Subscriber already present!")
                context.bot.send_message(chat_id=update.effective_chat.id, text=url + " is already subscribed")


def echoMessage(update, context):
    context.bot.send_message(update.effective_chat.id, text=update.message.text)




logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)



start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


echo_handler = MessageHandler(None, echoMessage)
dispatcher.add_handler(echo_handler)

print("Bot started")
databaseConnector.createTable()

updater.start_polling()
