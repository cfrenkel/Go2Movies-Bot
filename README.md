# Go2Movie Bot
Get examples of favorite movies, and find more movies that you may like and being shown today in the cinema.
 <https://t.me/go2movie_bot>

* Tali Badichi
* Ruhami Bichman
* Chani Frenkel

## Screenshots

![SCREESHOT DECSRIPTION](screenshots/bot_in_phone.png)

## How to Run This Bot
* start: add new movies until get recommended movies requests  
* get recommended movies:
* share location with the telegram bot
* enter the date
* get the recommended movie include cinema information,trailer and more
* show more or choose the movie
* Movie Time Notification!

### Prerequisites
* Python 3.7
* pipenv
* MongoDB

### Setup
* Clone this repo from github
* Install dependencies: `pipenv install`
* Get a BOT ID from the [botfather](https://telegram.me/BotFather).
* Create a `secret_settings.py` file:

        BOT_TOKEN = "your-bot-token-here"

### Run
To run the bot use:

    pipenv run python bot.py

(Or just `python bot.py` if running in a pipenv shell.)

## Credits and References
* [Telegram Docs](https://core.telegram.org/bots)
* [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
* [Movieglu API](https://developer.movieglu.com/)

