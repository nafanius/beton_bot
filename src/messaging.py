"""summary"""

from db_driver.data_sql_bot import add_id_chat_or_turn_on, add_id_chat_or_turn_off, add_all_acive_chat_id
import threading

db_lock = threading.Lock()


def on(chat_id):
    """Add id chat or turn on the existing one in the database.

    Args:
        chat_id (str): Chat identifier.

    Returns:
        str: Message indicating the status of operational information reception.
    """    
    with db_lock:
        add_id_chat_or_turn_on(chat_id)

    return f"Otrzymywanie informacji operacyjnych włączone"


def off(chat_id):
    """Add id chat or turn off the existing one in the database.

    Args:
        chat_id (str): Chat identifier.

    Returns:
        str: Message indicating the status of operational information reception.
    """    
    with db_lock:
        add_id_chat_or_turn_off(chat_id)

    return f"Otrzymywanie informacji operacyjnych wyłączone"


def get_all_chat():
    """Get all active chat IDs from the database with is_active set to True.

    Returns:
        list: list of active chat IDs.
    """    
    with db_lock:
        return add_all_acive_chat_id()

