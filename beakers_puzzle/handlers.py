# coding: utf-8

import gettext

from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram.ext import ConversationHandler
from telegram.ext.dispatcher import run_async

import constants as c
from puzzle_scheme import CHOICES
from puzzle_scheme import WINNING_STEPS


MESSAGE = None

def make_markup(choice):
    keyboard = [
        [InlineKeyboardButton(direction, callback_data=step)]
        for step, direction in CHOICES[choice]
    ]
    keyboard.append(
        [InlineKeyboardButton(c.RESET.title(), callback_data=c.RESET)])
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup


def make_reply_text(choice):
    one, two, three = choice.split('-')
    text = f'{one}/10    {two}/7    {three}/5'
    return text


@run_async
def start(bot, update):
    update.message.reply_text(c.START_TEXT)


@run_async
def help(bot, update):
    update.message.reply_text(c.HELP_TEXT)


@run_async
def lang(bot, update, args):
    if len(args) != 1:
        update.message.reply_text(c.WRONG_ARGS)
        return
    lang_str = args[0]
    if lang_str not in ['en', 'ru']:
        update.message.reply_text(c.WRONG_ARGS)
        return
    new_lang = gettext.translation(
        'beakers_puzzle', languages=[lang_str])
    new_lang.install()
    update.message.reply_text(c.DONE)


@run_async
def begin_puzzle(bot, update):
    global MESSAGE
    update.message.reply_text(c.DESCRIPTION)
    reply_markup = make_markup(c.S_10_0_0)
    reply_text = make_reply_text(c.S_10_0_0)

    message = update.message.reply_text(reply_text, reply_markup=reply_markup)
    MESSAGE = message.message_id
    return c.STEP


@run_async
def step(bot, update):
    query = update.callback_query
    choice = query.data
    chat_id = query.message.chat_id
    if choice in WINNING_STEPS:
        bot.edit_message_text(
            text=c.DONE, chat_id=chat_id, message_id=query.message.message_id)
        return ConversationHandler.END
    else:
        if choice == c.RESET:
            choice = c.S_10_0_0
        reply_markup = make_markup(choice)
        reply_text = make_reply_text(choice)
        bot.edit_message_text(
            text=reply_text, chat_id=chat_id,
            message_id=query.message.message_id, reply_markup=reply_markup)
        return c.STEP


@run_async
def cancel(bot, update):
    bot.edit_message_text(
        text=c.CANCEL, chat_id=update.message.chat_id, message_id=MESSAGE)
    return ConversationHandler.END
