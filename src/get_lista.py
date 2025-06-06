import threading
import db_driver.data_sql_list as data_sql_list
from src.setting import Settings
import time
from datetime import datetime, timedelta



db_lock = threading.Lock()

def lista_in_bot(lista):
    """convert the list of tuples to a formatted string for sending to the bot

    Args:
        lista (list): list of tuples, where each tuple contains a datetime object and a person's name

    Returns:
        str: formatted string with the time and person's name for each item in the list
    """    

    if not lista:
        return ""
    lista_text = ""
    number_of_item = 1
    for time_send, person in lista:
        lista_text += f"{number_of_item}. {time_send.strftime('%H:%M')} {person}\n"
        number_of_item += 1
    return lista_text




def combination_of_some_days_list(today=False):
    """Get the list for today or the next day, checking if there is a new list

    Args:
        today (bool, optional): if True, get the list for today, otherwise for the next day. Defaults to False.

    Returns:
        str: text to be sent to the bot with the list for today or the next day, or a message that there is no data.
    """    

    text_to_bot = ""

    def get_text_lista(day, text):
        """Check if there is a new list for the given day and update the text to be sent to the bot.

        Args:
            day (datatime): date to check for a new list
            text (str): current text that will be updated if a new list is found

        Returns:
            str: updated text to be sent to the bot
        """        
        date = day.strftime('%d.%m.%Y')

        with db_lock:
            currant_lista,  id_event_time, status = data_sql_list.get_newest_list_beton_or_lista('lista', date, 0)
        with db_lock:
            old_stan_lista = data_sql_list.get_newest_list_beton_or_lista('lista', date, 1)[0]

        if old_stan_lista != currant_lista:
            if status == 0:
                text = text + f"<b>{date}\nDyspozytor <tg-spoiler>kurwa</tg-spoiler> dodał rozkład, on jeszcze może się zmienić. Jeśli się zmieni, dam znać\n</b>{lista_in_bot(currant_lista)}\n\n"
        
        if id_event_time:
            with db_lock:
                data_sql_list.update_status('lista', id_event_time)
        
        return text



    if today:
        now = datetime.now()

        if now.weekday() > 5:
            now = now + timedelta(days=1) # if today is weekend, we take next day

        date = now.strftime('%d.%m.%Y')

        threshold = time.time() - Settings.time_of_compare  * 3600

        with db_lock:
            data_sql_list.delete_records_below_threshold(threshold, "list")

        with db_lock:
            list_of_send_from_base = data_sql_list.get_newest_list_beton_or_lista("lista", date, 0)[0]

        if list_of_send_from_base:
            text_to_bot = f"**{date}**\n{lista_in_bot(list_of_send_from_base)}\n\n"
        else:
            text_to_bot = "Brak danych"
 
    else:
        now = datetime.now()
        check_day = datetime.now() + timedelta(days=1)

        if now.weekday() == 4:
            for i in [0,2]:
                check_day = check_day + timedelta(days=i)

                text_to_bot = get_text_lista(check_day, text_to_bot)

                
        else:
            text_to_bot = get_text_lista(check_day, text_to_bot)


    return text_to_bot


if __name__ == '__main__':
    print(combination_of_some_days_list(True))
