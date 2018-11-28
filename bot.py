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



    logger.info(f"> Start chat #{chat_id}")

    keyboard = [[InlineKeyboardButton("Add movie", callback_data='1')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup)


def publish_result(movies_list):
    print(movies_list)
    # for movie in movies_list:
    #     m = movie['cinema']
    #     print(m['cinema_name'], m['address'])
    #     print(m['movie_name'], m['trailers'], m['images'])

def respond(bot, update):
    chat_id = update.message.chat_id
    text = update.message.text
    status = model.get_status(chat_id)

    logger.info(f"= Got on chat #{chat_id}: {text!r}")
    if status == "add":
        model.add_movie(chat_id, text)

        message = "All right! Press Add to add more movie, or Get movies to find fit movie."
        keyboard = [[InlineKeyboardButton("Add movie", callback_data='1')],
                    [InlineKeyboardButton("Get movies", callback_data='2')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup)

    elif status == "get_movies":
        publish_result(model.get_recommended_movies(chat_id, model.get_lat(chat_id), model.get_lon(chat_id), text))
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

    model.update_lon(chat_id, lon)
    model.update_lat(chat_id, lat)
    # reply_markup = telegram.ReplyKeyboardRemove()
    # bot.send_message(chat_id=update.message.chat_id, reply_markup=reply_markup)

    bot.send_message(chat_id=chat_id, text="Insert date in YYYY-MM-DD format.")


def button(bot, update):
    query = update.callback_query
    chat_id = query.message.chat_id
    if query.data == "1":
        model.update_status(chat_id, "add")
        bot.send_message(chat_id=chat_id, text="No problem! Enter a movie name")
    elif query.data == "2":
        model.update_status(chat_id, "get_movies")
        # location_keyboard = telegram.KeyboardButton(text="send_location", request_location=True)
        # custom_keyboard = [[location_keyboard]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="share your location with us!")

    else:
        pass


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

echo_handler = MessageHandler(Filters.text, respond)
dispatcher.add_handler(echo_handler)

location_handler = MessageHandler(Filters.location, handle_location)
dispatcher.add_handler(location_handler)


dispatcher.add_handler(CallbackQueryHandler(button))
logger.info("Start polling")
updater.start_polling()



