import sqlite3


class DataSource(object):
    def get_answers(self):
        raise NotImplementedError()

    def get_questions(self):
        raise NotImplementedError()

    def get_questions_forward(self):
        raise NotImplementedError()


class DataBase(DataSource):
    def __init__(self, name):
        self.conn = sqlite3.connect(name, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def get_answers(self):
        self.cursor.execute("SELECT text, url FROM answers;")
        return self.cursor.fetchall()

    def get_questions(self):
        self.cursor.execute("SELECT text, forward FROM questions;")
        return self.cursor.fetchall()

    def get_questions_forward(self):
        self.cursor.execute("SELECT forward FROM questions;")
        tmp = self.cursor.fetchall()
        forwards = [str(x[0]) for x in tmp]
        return forwards
