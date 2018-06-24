# coding: utf-8

import os

from telegram.ext import CallbackQueryHandler
from telegram.ext import CommandHandler
from telegram.ext import ConversationHandler
from telegram.ext import Updater

import handlers

updater = Updater(os.environ('TOKEN'))

dispatcher = updater.dispatcher

puzzle_handler = ConversationHandler(
    entry_points=[CommandHandler('begin', handlers.begin_puzzle)],

    states={
        'step': [CallbackQueryHandler(handlers.step)],
    },

    fallbacks=[CommandHandler('cancel', handlers.cancel)]
)
start_handler = CommandHandler('start', handlers.start)
help_handler = CommandHandler('help', handlers.help)
lang_handler = CommandHandler('lang', handlers.lang, pass_args=True)

dispatcher.add_handler(puzzle_handler)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(lang_handler)

updater.start_polling()

updater.idle()
