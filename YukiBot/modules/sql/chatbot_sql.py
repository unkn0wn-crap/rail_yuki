import threading
from sqlalchemy import Column, String
from YukiBot.modules.sql import BASE, SESSION

class MukeshChats(BASE):
    __tablename__ = "mukesh_chats"
    chat_id = Column(String(14), primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = chat_id

MukeshChats.__table__.create(checkfirst=True)
INSERTION_LOCK = threading.RLock()

def is_mukesh(chat_id):
    try:
        chat = SESSION.query(MukeshChats).get(str(chat_id))
        return bool(chat)
    except Exception as e:
        print(f"Error in is_mukesh: {e}")
        return False
    finally:
        SESSION.close()

def set_mukesh(chat_id):
    with INSERTION_LOCK:
        try:
            mukeshchat = SESSION.query(MukeshChats).get(str(chat_id))
            if not mukeshchat:
                mukeshchat = MukeshChats(str(chat_id))
                SESSION.add(mukeshchat)
            SESSION.commit()
        except Exception as e:
            print(f"Error in set_mukesh: {e}")
            SESSION.rollback()
        finally:
            SESSION.close()

def rem_mukesh(chat_id):
    with INSERTION_LOCK:
        try:
            mukeshchat = SESSION.query(MukeshChats).get(str(chat_id))
            if mukeshchat:
                SESSION.delete(mukeshchat)
            SESSION.commit()
        except Exception as e:
            print(f"Error in rem_mukesh: {e}")
            SESSION.rollback()
        finally:
            SESSION.close()