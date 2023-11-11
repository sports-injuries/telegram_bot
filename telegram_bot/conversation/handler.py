from telegram.ext import (
    CommandHandler,
    ConversationHandler,
    Filters,
    MessageHandler,
)

from telegram_bot.conversation import states
from telegram_bot.conversation.core import start, cancel
from telegram_bot.conversation.teams import team_choice, team_stat
from telegram_bot.conversation.players import player_choice, player_stat

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        states.CHOOSING: [
            MessageHandler(Filters.regex('^(Получить статистику по команде)$'), team_choice),
            MessageHandler(Filters.regex('^(Получить статистику по игроку)$'), player_choice),
        ],
        states.TEAM_STAT: [
            MessageHandler(Filters.text, team_stat)
        ],
        states.PLAYER_STAT: [
            MessageHandler(Filters.text, player_stat)
        ]
    },
    fallbacks=[
        CommandHandler('cancel', cancel)
    ]
)
