from tinydb import TinyDB


def get_db():
    with TinyDB("db.json") as db:
        return db
