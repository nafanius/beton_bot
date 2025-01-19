import threading
import data_sql_list
from setting import Settings
import time
from datetime import datetime, timedelta
import os



db_lock = threading.Lock()

def lista_in_bot(lista):
    """"фотрмируем list в текстовый формат для высолки в бот """

    if not lista:
        return ""
    lista_text = ""
    for time_from_datatime, person in lista:
        lista_text += f"{time_from_datatime.strftime('%H:%M')} {person}\n"

    return lista_text




def combination_of_some_days_list(today=False):
    """формируем общий лист на несколько дней в зависимости от дня недели"""

    text_to_bot = ""
    if today:
        now = datetime.now()
        date = now.strftime('%d.%m.%Y')

        threshold = time.time() - Settings.time_of_compare  * 3600

        with db_lock:
            data_sql_list.delete_records_below_threshold(threshold, "list")

        with db_lock:   
            text_to_bot += f"**{date}**\n{lista_in_bot(data_sql_list.get_newest_list_beton_or_lista("lista", date, 0)[0])}\n\n"
 
    else:
       pass

    return text_to_bot


if __name__ == '__main__':
    print(combination_of_some_days_list(True))
