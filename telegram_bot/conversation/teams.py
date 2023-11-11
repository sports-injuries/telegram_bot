from telegram import ReplyKeyboardRemove, Update
from telegram.ext import (
    CallbackContext,
    ConversationHandler,
)

from telegram_bot.conversation.schemas import JSON
from telegram_bot.conversation import states
from telegram_bot.clients.api import client as api


def team_choice(update: Update, context: CallbackContext[JSON, JSON, JSON]) -> int:
    assert update.message is not None
    assert context.user_data is not None

    teams = api.teams.get_all()
    team_names = [team.name for team in teams]
    question = 'Выбери одну из следующих команд:\n{teams}'.format(teams='\n'.join(team_names))
    update.message.reply_text(question, reply_markup=ReplyKeyboardRemove())

    return states.TEAM_STAT


def team_stat(update: Update, context: CallbackContext[JSON, JSON, JSON]) -> int:
    text = ''  # noqa: F841
    team = update.message.text
    update.message.reply_text(f'Вот статистика по команде {team}')

    return ConversationHandler.END
