import secret_settings
import model
import logging


import telegram
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters, Updater
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

logging.basicConfig(
    format='[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

updater = Updater(token=secret_settings.BOT_TOKEN)
dispatcher = updater.dispatcher


def start(bot, update):
    chat_id = update.message.chat_id
    exist_user = ""
    if not model.add_user(chat_id):
        model.update_status(chat_id, 'start')
        exist_user = "back"

    message = f"Welcome {exist_user} to Go2Movie bot!\n" \
              "I'll give you some movies you may like, " \
              "that are being shown today in the cinema."

    # \
    # "\n\nGive me movie you're like to add it to your movies list."

    # custom_keyboard = [[location_keyboard]]
    # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    # bot.send_message(chat_id=update.message.chat_id, text="Would you mind sharing your location with me?",
    #                  reply_markup=reply_markup)

    logger.info(f"> Start chat #{chat_id}")
    keyboard = [[InlineKeyboardButton("Add movie", callback_data='1')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup)


def respond(bot, update):
    chat_id = update.message.chat_id
    text = update.message.text
    logger.info(f"= Got on chat #{chat_id}: {text!r}")
    if model.get_status(chat_id) == "add":
        model.add_movie(chat_id, text)

    # response = "cool! I'm going to find you a fit movie. wait a moment..."
    # bot.send_message(chat_id=update.message.chat_id, text=response)
    # recommended_movies = model.get_recommended_movies()
    # bot.send_message(chat_id=update.message.chat_id, text=recommended_movies)


def handle_location(bot, update):
  chat_id = update.message.chat_id
  logger.info(f"> location chat #{chat_id}")

  lon = update.message['location'].longitude
  lat = update.message['location'].latitude
  logger.info(f"& Got location on chat #{chat_id}: {lat!r} ,{lon}")

  print(lon)
  reply_markup = telegram.ReplyKeyboardRemove()
  bot.send_message(chat_id=update.message.chat_id, text=f"haifa is {response:.3f} km away from you.",
                   reply_markup=reply_markup)

  location_keyboard = telegram.KeyboardButton(text="",
                                              request_location=True)

def button(bot, update):
    query = update.callback_query
    chat_id = query.message.chat_id
    if query.data == "1":
        model.update_status(chat_id,"add")
        bot.send_message(chat_id=chat_id, text="no problem!, enter a movie name")
    elif query.data == "2":
        pass
    else:
        pass

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

echo_handler = MessageHandler(Filters.text, respond)
dispatcher.add_handler(echo_handler)

dispatcher.add_handler(echo_handler)
location_handler = MessageHandler(Filters.location, handle_location)

dispatcher.add_handler(CallbackQueryHandler(button))
logger.info("Start polling")
updater.start_polling()

