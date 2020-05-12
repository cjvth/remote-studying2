from os import getenv

import telegram
from telegram.ext import Updater, MessageHandler, Filters


def echo(update, context):
    update.message.reply_text(update.message.text)


def bot():
    if getenv("PROXY_URL"):
        updater = Updater(getenv('TOKEN'), use_context=True,
                          request_kwargs={'proxy_url': getenv("PROXY_URL")})
    else:
        updater = Updater(getenv('TOKEN'), use_context=True)
    dp = updater.dispatcher
    text_handler = MessageHandler(Filters.text, echo)
    dp.add_handler(text_handler)
    updater.start_polling()
    try:
        updater.idle()
    except ValueError as e:
        print(e)
        pass


if __name__ == '__main__':
    bot()
