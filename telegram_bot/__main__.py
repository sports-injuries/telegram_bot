import logging
import os

from errors import AppError
from typing import Any
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    ConversationHandler,
    Filters,
    MessageHandler,
    Updater
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CHOOSING = 1
TEAM_STAT = 3
PLAYER_STAT = 4

reply_keyboard = [
    ['Team', 'Player'],
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

JSON = dict[str, Any]


def start(update: Update, context: CallbackContext[JSON, JSON, JSON]) -> int:
    question = """Привет.
Команда или игрок?
"""
    update.message.reply_text(text=question, reply_markup=markup)

    return CHOOSING


def team_choice(update: Update, context: CallbackContext[JSON, JSON, JSON]) -> int:
    question = 'Какую команду?'
    if context.user_data is not None:
        context.user_data['team'] = update.message.text
    else:
        raise AppError('empty context.user_data')
    update.message.reply_text(question, reply_markup=ReplyKeyboardRemove())

    return TEAM_STAT


def player_choice(update: Update, context: CallbackContext[JSON, JSON, JSON]) -> int:
    question = 'Какой игрок?'
    if context.user_data is not None:
        context.user_data['player'] = update.message.text
    else:
        raise AppError('empty context.user_data')
    update.message.reply_text(question, reply_markup=ReplyKeyboardRemove())

    return PLAYER_STAT


def team_stat(update: Update, context: CallbackContext[JSON, JSON, JSON]) -> int:
    text = ''  # noqa: F841
    team = update.message.text
    update.message.reply_text(f'Вот статистика по команде {team}')

    return ConversationHandler.END


def player_stat(update: Update, context: CallbackContext[JSON, JSON, JSON]) -> int:
    text = ''  # noqa: F841
    player = update.message.text
    update.message.reply_text(f'Вот статистика по игроку {player}')

    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext[JSON, JSON, JSON]) -> int:
    text = 'До скорого'
    update.message.reply_text(text)

    return ConversationHandler.END


def main() -> None:
    updater = Updater(os.environ['BOT_TOKEN'])
    dispatcher = updater.dispatcher  # type: ignore

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING: [
                MessageHandler(Filters.regex('^(Team)$'), team_choice),
                MessageHandler(Filters.regex('^(Player)$'), player_choice),
            ],
            TEAM_STAT: [
                MessageHandler(Filters.text, team_stat)
            ],
            PLAYER_STAT: [
                MessageHandler(Filters.text, player_stat)
            ]
        },
        fallbacks=[
            CommandHandler('cancel', cancel)
        ]
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
