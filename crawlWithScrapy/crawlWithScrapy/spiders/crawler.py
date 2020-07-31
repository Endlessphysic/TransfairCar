# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.
import logging
import copy
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from crawlWithScrapy.crawlWithScrapy.spiders.crawScrapy import PostsSpider
import re

# Eckert Token 1357061283:AAE1cc3aIU2qk5TTeq_LkgewTpl6O2OM5g0

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

crawler = PostsSpider()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def gib_mir(update, context):
    """Send a message when the command /help is issued."""
    everything = crawl_everything()
    out = format_everything(everything)
    update.message.reply_text('Auftrag xyz \n' +
                             out)


def was_gibts_aus_bw(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Eckert mach so schnell er kann...')
    everything = crawl_everything()
    bw = gib_mir_bw(everything)
    out = format_everything(bw)
    update.message.reply_text('Auftrag xyz \n' +
                              out)


def was_gibts_aus_bayern(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Döberin schaut nach Aufträgen...')
    everything = crawl_everything()
    bayern = gib_mir_bayern(everything)
    out = format_everything(bayern)
    update.message.reply_text('Auftrag xyz \n' +
                              out)


def gib_mir_bayern(everything):
    regex = re.compile('[8-9][0-9]{4}')
    i = 0
    bayern = []
    for item in everything:
        if bool(regex.search(item['start'])) or bool(regex.search(item['destination'])):
            bayern.append(copy.deepcopy(everything[i]))
        i += 1
    return bayern


def gib_mir_bw(everything):
    regex = re.compile('[6-7][0-9]{4}')
    i = 0
    bw = []
    for item in everything:
        if bool(regex.search(item['start'])) or bool(regex.search(item['destination'])):
            bw.append(copy.deepcopy(everything[i]))
        i += 1
    return bw


def crawl_everything():
    crawler.process.crawl(PostsSpider)
    crawler.process.start()
    return crawler.everything[0]


def format_everything(everything):
    out = ''
    for item in everything:
        out += '\n' + 'Preis: ' + item['price']
        out += '\n' + 'Start: ' + item['start']
        out += '\n' + 'Ziel: ' + item['destination']
        out += '\n \n'
    return out


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help! \n' +
                              'You can hit: \n' +
                              '/start \n' +
                              '/help \n' +
                              '/GIB_MIR_ALLES \n' +
                              '/was_gibts_in_BW \n' +
                              '/was_gibts_in_Bayern')


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1357061283:AAE1cc3aIU2qk5TTeq_LkgewTpl6O2OM5g0", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("GIB_MIR_ALLES", gib_mir))
    dp.add_handler(CommandHandler("was_gibts_in_BW", was_gibts_aus_bw))
    dp.add_handler(CommandHandler("was_gibts_in_Bayern", was_gibts_aus_bayern))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()










# print(bot.get_me())