from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext, ConversationHandler

from telegram_bot.conversation import states
from telegram_bot.conversation.schemas import JSON

reply_keyboard = [
    ['Team', 'Player'],
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def start(update: Update, context: CallbackContext[JSON, JSON, JSON]) -> int:
    question = """Привет.
Команда или игрок?
"""
    update.message.reply_text(text=question, reply_markup=markup)

    return states.CHOOSING


def cancel(update: Update, context: CallbackContext[JSON, JSON, JSON]) -> int:
    text = 'До скорого'
    update.message.reply_text(text)

    return ConversationHandler.END
