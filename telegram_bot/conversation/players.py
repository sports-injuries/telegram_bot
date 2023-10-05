from telegram_bot.conversation.errors import AppError
from telegram import ReplyKeyboardRemove, Update
from telegram.ext import (
    CallbackContext,
    ConversationHandler,
)

from telegram_bot.conversation.schemas import JSON
from telegram_bot.conversation import states


def player_choice(update: Update, context: CallbackContext[JSON, JSON, JSON]) -> int:
    question = 'Какой игрок?'
    if context.user_data is not None:
        context.user_data['player'] = update.message.text
    else:
        raise AppError('empty context.user_data')
    update.message.reply_text(question, reply_markup=ReplyKeyboardRemove())

    return states.PLAYER_STAT


def player_stat(update: Update, context: CallbackContext[JSON, JSON, JSON]) -> int:
    text = ''  # noqa: F841
    player = update.message.text
    update.message.reply_text(f'Вот статистика по игроку {player}')

    return ConversationHandler.END
