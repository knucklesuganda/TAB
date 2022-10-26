from telebot import TeleBot

import settings
import messages
from containers import MainContainer
from questions.bot_handlers import create_handlers as question_handlers, get_question_handler, create_question_handler

container = MainContainer()
bot: TeleBot = container.bot()


@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.from_user.id, messages.write_question)
    bot.register_next_step_handler(message, get_question_handler)


@bot.message_handler(commands=['help'])
def start_handler(message):
    bot.send_message(message.from_user.id, messages.help_message)


@bot.message_handler(commands=['add_question'])
def add_question_handler(message):
    if message.from_user.username in settings.ADMINS_USERNAMES:
        bot.send_message(message.from_user.id, messages.add_question)
        bot.register_next_step_handler(message, create_question_handler)
    else:
        bot.send_message(message.from_user.id, messages.not_admin)


def main():
    if settings.DEBUG:
        question_handlers()
        bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    main()
