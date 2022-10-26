from common.database.repository import Repository
from questions.database.models import Question


class QuestionRepository(Repository):
    def get(self, **kwargs):
        return self.session.query(Question).filter_by(**kwargs).one()

    def filter(self, *args, **kwargs):
        return self.session.query(Question).filter(*args).filter_by(**kwargs).all()

    def save(self, obj):
        self.session.add(obj)

    def update(self, obj):
        self.session.add(obj)

    def filter_regex(self, column: str, regex: str):
        return self.filter(getattr(Question, column).like(regex))
