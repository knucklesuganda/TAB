import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

import config
import messages
import logging

from os import environ
import django

environ.setdefault("DJANGO_SETTINGS_MODULE", "telegram_bot.settings")
django.setup()

from Question.models import Question
from django.core.exceptions import ObjectDoesNotExist


def bot_start():
    bot = telebot.TeleBot(config.token)
    new_question = Question()

    logger = logging.getLogger("information")
    logger.setLevel(logging.INFO)

    fh = logging.FileHandler("information.log")
    fh.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    logger.addHandler(fh)

    def get_question_from_user(message):
        questions = Question.objects.filter(text__iregex=message.text)
        keyboard = InlineKeyboardMarkup()

        if not questions:
            bot.send_message(message.from_user.id, messages.no_answer)
            return

        for question in questions:
            keyboard.add(InlineKeyboardButton(text=question.text[:30], callback_data=question.pk))

        bot.send_message(message.from_user.id, messages.choose_question, reply_markup=keyboard)

    def add_question(message):
        try:
            new_question.text, new_question.answer, new_question.back,\
                new_question.forward, new_question.url = message.text.split(";")
            new_question.save()
            bot.send_message(message.from_user.id, messages.question_added.format(new_question.id))

        except Exception as exc:
            bot.send_message(message.from_user.id, str(exc))

    @bot.message_handler(content_types=['text'])
    def main_handle(message):
        logger.info(f"User {message.from_user.username} sent {message.text}")
        message.text = message.text.lower()

        if message.text == "/start":
            bot.send_message(message.from_user.id, messages.write_question)
            bot.register_next_step_handler(message, get_question_from_user)

        elif message.text == "/help":
            bot.send_message(message.from_user.id, messages.help_message)

        elif message.text == "/add_question":
            if message.from_user.username == config.admin_username:
                bot.send_message(message.from_user.id, messages.add_question)
                bot.register_next_step_handler(message, add_question)
            else:
                bot.send_message(message.from_user.id, messages.not_admin)

        else:
            logger.info(f"User {message.from_user.username} have found nothing")
            bot.send_message(message.from_user.id, messages.not_found)

    @bot.callback_query_handler(func=lambda call: True)
    def button_handlers(call):
        try:
            question = Question.objects.get(pk__exact=call.data)
            bot.delete_message(call.message.chat.id, call.message.message_id)
            keyboard = InlineKeyboardMarkup()

            if not question.forward:
                message_text = f"Answer: {question.answer if question.answer else 'No text answer'}." \
                               f" \n\n{question.url}"

                bot.send_message(call.message.chat.id, message_text)
                return

            forwarded_questions = Question.objects.filter(back__exact=question.forward)
            if not forwarded_questions:
                bot.send_message(call.message.chat.id, messages.no_answer)
                return

            for forwarded_question in forwarded_questions:
                keyboard.add(InlineKeyboardButton(text=forwarded_question.text,
                                                  callback_data=forwarded_question.pk))

            bot.send_message(call.message.chat.id, messages.choose_question,
                             reply_markup=keyboard)

        except ObjectDoesNotExist as exc:
            bot.send_message(call.message.chat.id, messages.does_not_exist)

    logger.info("Bot started")
    bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    bot_start()
