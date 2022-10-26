from dependency_injector.wiring import Provide, inject

from common.database.repository import Repository
from containers import MainContainer
from questions.database.models import Question


@inject
def filter_question_by_text(text: str, repository: Repository = Provide[MainContainer.question_repository]):
    return repository.filter_regex(column='text', regex=f"%{text.lower()}%")


@inject
def get_question_by_id(id, repository: Repository = Provide[MainContainer.question_repository]):
    return repository.get(id=id)


@inject
def filter_forwarded_questions(forward: Question, repository: Repository = Provide[MainContainer.question_repository]):
    return repository.filter(back=forward)
