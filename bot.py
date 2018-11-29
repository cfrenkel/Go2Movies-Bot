import secret_settings
import model
import logging
import db_management
import datetime

import settings
import pymongo.mongo_client

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
jobs = updater.job_queue

def start(bot, update):

    chat_id = update.message.chat_id
    db_management.DBManagementHelper().update_index(chat_id, 0)
    db_management.DBManagement().update_movie(chat_id)
    exist_user = ""
    if not model.add_user(chat_id):
        model.update_status(chat_id, 'start')
        exist_user = "back"

    message = f"Welcome {exist_user} to Go2Movie bot!\n" \
              "Give me an example of a movie you like and I'll find you a movie you'll like."

    logger.info(f"> Start chat #{chat_id}")

    keyboard = [[InlineKeyboardButton("Add movie", callback_data='1')]] if not exist_user else \
        [[InlineKeyboardButton("Add movie", callback_data='1'),
          InlineKeyboardButton("Get recommendations", callback_data='2')]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup)


def help(bot, update):
    chat_id = update.message.chat_id
    message = "*Bot options:*\n\nI can do some searching for you." \
              " If you'll give a movie you liked I'll find some good movies playing today at your area." \
              "\n\n/start: add a movie to get recommended movies.\n"
    bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')


def publish_result(movies_list, bot, chat_id):
    index = db_management.DBManagementHelper().get_index(chat_id)
    movie = movies_list[index]
    m = movie['cinema']
    message = f"Movie name: {movie['movie_name']}\n" \
              f"Hour: {movie['movie_hour']}\n" \
              f"Cinema: {m['cinema_name']}\n" \
              f"Address: {m['address']}\n"

    if index == 2:
        keyboard = [[InlineKeyboardButton("I want to go watch this one!", callback_data='10' + str(index))]]
    else:
        keyboard = [[InlineKeyboardButton("I want to go watch this one!", callback_data='10' + str(index)),
                     InlineKeyboardButton("Show me more movie...", callback_data='3')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_message(chat_id=chat_id, text=message)
    bot.send_video(chat_id=chat_id, text=message, video=movie['trailers'], supports_streaming=True,
                   reply_markup=reply_markup)
    db_management.DBManagementHelper().update_index(chat_id, index + 1)

def respond(bot, update):
    chat_id = update.message.chat_id
    text = update.message.text
    status = model.get_status(chat_id)

    logger.info(f"= Got on chat #{chat_id}: {text!r}")
    if status == "add":
        # ORIGINAL CODE HERE:
        # model.add_movie(chat_id, text)

        message = "All right! Press Add movie to add more movie, or Get recommendations to find movie you'll like."
        keyboard = [[InlineKeyboardButton("Add movie", callback_data='1'),
                     InlineKeyboardButton("Get recommendations", callback_data='2')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup)

    elif status == "get_movies":
        # ORIGINAL CODE HERE:
        # db_management.DBManagementHelper().insert_movie_list(chat_id, model.get_recommended_movies
        # (chat_id, model.get_lat(chat_id), model.get_lon(chat_id), text))

        publish_result(db_management.DBManagementHelper().get_movies_list(chat_id), bot, chat_id)


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
        bot.send_message(chat_id=chat_id, text="Ok, Enter a movie name.")
    elif query.data == "2":
        model.update_status(chat_id, "get_movies")
        bot.send_message(chat_id=chat_id, text="Share your location with us!")

    elif query.data == "3":
        m = db_management.DBManagementHelper().get_movies_list(chat_id)
        print(query.message)
        publish_result(m, bot, chat_id)
    elif query.data == "100":
        model.choose_movie(chat_id, db_management.DBManagementHelper().get_movies_list(chat_id)[0])
        bot.send_message(chat_id=chat_id, text="Great choice!")
        jobs.run_once(notify, 60)
    elif query.data == "101":
        model.choose_movie(chat_id, db_management.DBManagementHelper().get_movies_list(chat_id)[1])
        bot.send_message(chat_id=chat_id, text="Great choice!")
        jobs.run_once(notify, 60)
    elif query.data == "102":
        model.choose_movie(chat_id, db_management.DBManagementHelper().get_movies_list(chat_id)[2])
        bot.send_message(chat_id=chat_id, text="Great choice!")
        jobs.run_once(notify, 60)


def invite(bot, update):
    if model.get_chosen_movie(update.message.chat_id):
        bot.send_message(chat_id=update.message.chat_id,
                         text=f'send to your friend :)\nhttps://telegram.me/movie2go_bot?start={chat_id}"')


def notify(bot,update, job):
    bot.send_message(chat_id=update.message.chat_id,
                    text="your movie going to start!!")


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)

invite_handler = CommandHandler('invite', start)
dispatcher.add_handler(invite_handler)

echo_handler = MessageHandler(Filters.text, respond)
dispatcher.add_handler(echo_handler)

location_handler = MessageHandler(Filters.location, handle_location)
dispatcher.add_handler(location_handler)

dispatcher.add_handler(CallbackQueryHandler(button))
logger.info("Start polling")
updater.start_polling()
