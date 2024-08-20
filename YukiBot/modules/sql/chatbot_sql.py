import threading

from sqlalchemy import Column, String

from YukiBot.modules.sql import BASE, SESSION


class YukiChats(BASE):
    __tablename__ = "yuki_chats"
    chat_id = Column(String(14), primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = chat_id


YukiChats.__table__.create(checkfirst=True)
INSERTION_LOCK = threading.RLock()


def is_yuki(chat_id):
    try:
        chat = SESSION.query(YukiChats).get(str(chat_id))
        return bool(chat)
    finally:
        SESSION.close()


def set_yuki(chat_id):
    with INSERTION_LOCK:
        yukichat = SESSION.query(YukiChats).get(str(chat_id))
        if not yukichat:
            yukichat = YukiChats(str(chat_id))
        SESSION.add(yukichat)
        SESSION.commit()


def rem_yuki(chat_id):
    with INSERTION_LOCK:
        yukichat = SESSION.query(YukiChats).get(str(chat_id))
        if yukichat:
            SESSION.delete(yukichat)
        SESSION.commit()