#small echo bot for Telegram

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Simple Bot to provide random quote from the DevOps_Borat fortune file
This program is dedicated to the public domain under the CC0 license.
This Bot uses the Updater class to handle the bot.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
"""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ChatAction
import logging
import os
import fun

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

#some useful constants
VERSION = os.getenv("OPENSHIFT_BUILD_NAME")
SOURCE = os.getenv("OPENSHIFT_BUILD_SOURCE")

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('I\'m a bot, please talk to me!\nenter "/fortune" to get random quote, "/info" to get bot status')

def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def fortune(bot, update):
    """provide random quote."""
    chat_id = update.message.chat_id
    #bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
    logger.info('User wants some fortune in update %s',update)
    update.message.reply_text(fun.get_one())

def about(bot, update):
    """Information about current instance"""
    logger.info('User wants some info in update %s',update)
    update.message.reply_text('build version is '+VERSION)
    update.message.reply_text('running in OpenShift POD '+os.getenv("HOSTNAME"))
    update.message.reply_text('built from '+SOURCE)
    update.message.reply_text('using fortune.py from https://github.com/goerz/fortune.py')
    update.message.reply_text('using Devops_Borat fortune database from Noah Sussman')

def default(bot, update):
    """Echo the user message."""
    update.message.reply_text('can\'t understand this request. enter "/fortune" to get random quote, "/info" to get bot status')


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    if "BOT_CONFIG_token" in os.environ: TOKEN = os.environ.get("BOT_CONFIG_token")
    else: print ("Please set environment variable BOT_CONFIG_token to contain the Telegram bot token.\nexiting...");exit(255)
    updater = Updater(TOKEN)
    fun.init()

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("fortune", fortune))
    #dp.add_handler(CommandHandler("about", about))
    dp.add_handler(CommandHandler("info", about))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, default))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    # if the environment variable BOT_CONFIG_service_url - register the webhook
    if "BOT_CONFIG_service_url" in os.environ:
        my_webhook_url=os.environ.get("BOT_CONFIG_service_url")
        updater.start_webhook(listen='0.0.0.0',
                      port=8080,
                      url_path=TOKEN)
        #print('setting webhook to: '+my_webhook_url+'/'+TOKEN)
        updater.bot.set_webhook(webhook_url=my_webhook_url+'/'+TOKEN)
    else:
        updater.start_polling()
        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        updater.idle()


if __name__ == '__main__':
	main()
