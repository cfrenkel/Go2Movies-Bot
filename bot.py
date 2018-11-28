import secret_settings
import logging
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater

logging.basicConfig(
    format='[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

updater = Updater(token=secret_settings.BOT_TOKEN)
dispatcher = updater.dispatcher


def start(bot, update):
    chat_id = update.message.chat_id
    logger.info(f"> Start chat #{chat_id}")
    bot.send_message(chat_id=chat_id, text="Welcome to Go2Movie bot! \n " \ 
                                           " I'll give you some movies you may like, " \ 
                                           "that are being shown today in the cinema.")


def respond(bot, update):
    chat_id = update.message.chat_id
    text = update.message.text
    logger.info(f"= Got on chat #{chat_id}: {text!r}")
    response = "Hi :)"
    bot.send_message(chat_id=update.message.chat_id, text=response)


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

echo_handler = MessageHandler(Filters.text, respond)
dispatcher.add_handler(echo_handler)

logger.info("Start polling")
updater.start_polling()