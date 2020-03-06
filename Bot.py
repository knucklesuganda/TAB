import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

import config
import messages
from Database import DataBase
from time import sleep
import logging


def bot_start():
    bot = telebot.TeleBot(config.token)
    database = DataBase(config.database_name)

    logger = logging.getLogger("information")
    logger.setLevel(logging.INFO)

    fh = logging.FileHandler("information.log")
    fh.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    logger.addHandler(fh)

    @bot.message_handler(content_types=['text'])
    def main_handle(message):
        logger.info(f"User {message.from_user.username} sent {message.text}")
        message.text = message.text.lower()

        if message.text == "/start":
            keyboard = InlineKeyboardMarkup()

            for question in database.get_questions():
                keyboard.add(InlineKeyboardButton(text=question[0], callback_data=question[1]))

            bot.send_message(message.from_user.id, messages.start, reply_markup=keyboard)

        elif message.text == "/help":
            bot.send_message(message.from_user.id, messages.help)

        else:
            logger.info("User {message.from_user.username} have found nothing")
            bot.send_message(message.from_user.id, messages.not_found)

    @bot.callback_query_handler(func=lambda call: True)
    def button_handlers(call):
        if call.data in database.get_questions_forward():
            logger.info(f"Button with '{call.data}' text pressed")

            for x, answer in enumerate(database.get_answers()):
                message_text = f"{x + 1}) {answer[0]}\n{answer[1]}\n"
                bot.send_message(call.message.chat.id, message_text)

            bot.delete_message(call.message.chat.id, call.message.message_id)

        else:
            bot.send_message(call.message.chat.id, messages.no_answer)

    logger.info("Bot started")
    bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    bot_start()
