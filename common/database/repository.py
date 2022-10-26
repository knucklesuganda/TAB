from abc import ABC, abstractmethod


class Repository(ABC):
    def __init__(self, session):
        self.session = session

    @abstractmethod
    def get(self, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def filter(self, *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def save(self, obj):
        raise NotImplementedError()

    @abstractmethod
    def update(self, obj):
        raise NotImplementedError()

    @abstractmethod
    def filter_regex(self, column: str, regex: str):
        raise NotImplementedError()
