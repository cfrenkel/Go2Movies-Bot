import secret_settings
import model
import logging
from telegram.ext import CommandHandler
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

    logger.info(f"> Start chat #{chat_id}")
    keyboard = [[InlineKeyboardButton("Add movie", callback_data='1')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup)


def respond(bot, update):
    chat_id = update.message.chat_id
    text = update.message.text
    logger.info(f"= Got on chat #{chat_id}: {text!r}")
    # if model.get_status(chat_id) == "start":

    response = "cool! I'm going to find you a fit movie. wait a moment..."
    bot.send_message(chat_id=update.message.chat_id, text=response)
    recommended_movies = model.get_recommended_movies()
    bot.send_message(chat_id=update.message.chat_id, text=recommended_movies)


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

echo_handler = MessageHandler(Filters.text, respond)
dispatcher.add_handler(echo_handler)

logger.info("Start polling")
updater.start_polling()
