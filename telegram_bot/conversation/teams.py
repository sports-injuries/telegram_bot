from telegram_bot.conversation.errors import AppError
from telegram import ReplyKeyboardRemove, Update
from telegram.ext import (
    CallbackContext,
    ConversationHandler,
)

from telegram_bot.conversation.schemas import JSON
from telegram_bot.conversation import states


def team_choice(update: Update, context: CallbackContext[JSON, JSON, JSON]) -> int:
    question = 'Какую команду?'
    if context.user_data is not None:
        context.user_data['team'] = update.message.text
    else:
        raise AppError('empty context.user_data')
    update.message.reply_text(question, reply_markup=ReplyKeyboardRemove())

    return states.TEAM_STAT


def team_stat(update: Update, context: CallbackContext[JSON, JSON, JSON]) -> int:
    text = ''  # noqa: F841
    team = update.message.text
    update.message.reply_text(f'Вот статистика по команде {team}')

    return ConversationHandler.END
