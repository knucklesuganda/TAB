from dependency_injector.wiring import Provide, inject

from common.database.unit_of_work import UnitOfWork
from containers import MainContainer
from questions.database.models import Question
from questions.schemas import CreateQuestionSchema


@inject
def create_question(data: CreateQuestionSchema, uow: UnitOfWork = Provide[MainContainer.question_uow]):
    with uow:
        question = Question(
            text=data.text,
            answer=data.answer,
            url=data.url,
            forward_id=data.forward,
            back_id=data.back,
        )
        uow.repository.save(question)
        uow.commit()
        return question.id
