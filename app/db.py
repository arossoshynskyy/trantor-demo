from tinydb import TinyDB


def get_db():
    with TinyDB as db:
        return db
