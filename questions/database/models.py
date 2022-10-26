from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship, backref

from common.database.database_setup import Base


class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer(), primary_key=True)
    text = Column(Text())
    answer = Column(Text())
    url = Column(Text())

    forward_id = Column(Integer, ForeignKey("questions.id", ondelete='SET NULL'), nullable=True, default=None)
    forward = relationship(
        "Question",
        primaryjoin='questions.c.id==questions.c.forward_id',
        remote_side='Question.id',
        backref=backref("children"),
    )

    back_id = Column(Integer, ForeignKey("questions.id", ondelete='SET NULL'), nullable=True, default=None)
    back = relationship(
        "Question",
        primaryjoin='questions.c.back_id==questions.c.id',
        remote_side='Question.id',
        backref=backref("next", uselist=False),
    )
