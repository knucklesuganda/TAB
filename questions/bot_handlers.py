import json

from telebot import TeleBot
from dependency_injector.wiring import inject, Provide
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

import messages
from containers import MainContainer
from questions.services.commands import create_question
from questions.services.queries import filter_question_by_text, get_question_by_id, filter_forwarded_questions
from questions.schemas import CreateQuestionSchema


@inject
def get_question_handler(message, bot: TeleBot = Provide[MainContainer.bot]):
    questions = filter_question_by_text(message.text)
    keyboard = InlineKeyboardMarkup()

    if not questions:
        bot.send_message(message.from_user.id, messages.no_answer)
    else:
        for question in questions:
            keyboard.add(InlineKeyboardButton(text=question.text[:30], callback_data=question.id))

        bot.send_message(message.from_user.id, messages.choose_question, reply_markup=keyboard)


@inject
def create_question_handler(message, bot: TeleBot = Provide[MainContainer.bot]):
    try:
        try:
            question_data = CreateQuestionSchema.parse_raw(message.text.replace('/add_question', ''))
            question_id = create_question(question_data)
        except json.JSONDecodeError:
            bot.send_message(message.from_user.id, messages.json_error)
            return

        bot.send_message(message.from_user.id, messages.question_added.format(question_id))

    except Exception as exc:
        bot.send_message(message.from_user.id, str(exc))


@inject
def create_handlers(bot: TeleBot = Provide[MainContainer.bot]):

    @bot.callback_query_handler(func=lambda call: True)
    def button_handlers(call):
        try:
            question = get_question_by_id(id=call.data)
            bot.delete_message(call.message.chat.id, call.message.message_id)
            keyboard = InlineKeyboardMarkup()

            if not question.forward:
                message_text = f"Answer: {question.answer if question.answer else 'No text answer'}." \
                               f" \n\n{question.url}"

                bot.send_message(call.message.chat.id, message_text)
                return

            forwarded_questions = filter_forwarded_questions(forward=question.forward)
            if not forwarded_questions:
                bot.send_message(call.message.chat.id, messages.no_answer)
                return

            for forwarded_question in forwarded_questions:
                keyboard.add(InlineKeyboardButton(
                    text=forwarded_question.text,
                    callback_data=forwarded_question.pk,
                ))

            bot.send_message(call.message.chat.id, messages.choose_question, reply_markup=keyboard)
        except Exception as exc:
            bot.send_message(call.message.chat.id, messages.does_not_exist)
