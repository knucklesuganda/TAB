from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Factory, Singleton, Object
from telebot import TeleBot

import settings
from common.database.sessions import Session
from common.database.unit_of_work import AlchemyUnitOfWork
from common.loggers import main_logger
from questions.database.repository import QuestionRepository


class MainContainer(DeclarativeContainer):
    wiring_config = WiringConfiguration(
        packages=[
            "questions",
            'common',
        ],
        modules=[
            '__main__',
        ]
    )

    logger = Object(main_logger)
    bot = Singleton(TeleBot, settings.BOT_KEY)
    session_creator = Factory(Session)

    question_repository = Factory(QuestionRepository, session=session_creator)
    question_uow = Factory(AlchemyUnitOfWork, repository=question_repository)
