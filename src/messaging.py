"""summary"""

from db_driver.data_sql_bot import add_id_chat_or_turn_on, add_id_chat_or_turn_off, add_all_acive_chat_id
import threading

db_lock = threading.Lock()


def on(chat_id):
    with db_lock:
        add_id_chat_or_turn_on(chat_id)

    return f"Otrzymywanie informacji operacyjnych włączone"


def off(chat_id):
    with db_lock:
        add_id_chat_or_turn_off(chat_id)

    return f"Otrzymywanie informacji operacyjnych wyłączone"


def get_all_chat():
    with db_lock:
        return add_all_acive_chat_id()

