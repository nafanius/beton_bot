import logging
import re
from datetime import datetime, timedelta

import threading
import data_sql_list

# region logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
lg = logging.debug
cr = logging.critical
inf = logging.info
exp = logging.exception
# logging.disable(logging.DEBUG)
# logging.disable(logging.INFO)
# logging.disable(logging.CRITICAL)
# logging_end
# endregion

db_lock = threading.Lock()

def check_del_add_lista():
    del_lista = []
    add_lista = []
    now = datetime.now()
    # now = now+timedelta(days=1) # for check
    date_of_lista = now.strftime('%d.%m.%Y')

    with db_lock:
        currant_list_beton,  id_event_time, status = data_sql_list.get_newest_list_beton_or_lista('beton', date_of_lista, 0)

    with db_lock:
        old_stan_lista_beton = data_sql_list.get_newest_list_beton_or_lista('beton', date_of_lista, 1)[0]
    inf(status)
    inf(id_event_time)

    if not old_stan_lista_beton:
        old_stan_lista_beton = currant_list_beton

    if status == 0:
        for i in old_stan_lista_beton:
            if i not in currant_list_beton:
                del_lista.append(i)
        for i in currant_list_beton:
            if i not in old_stan_lista_beton:
                add_lista.append(i)
    

    # для контроля отображения
    # del_lista = del_lista + currant_list_beton[2:3]
    # add_lista = add_lista + currant_list_beton[0:2]


    if id_event_time:
        with db_lock:
            data_sql_list.update_status('beton', id_event_time)

    del_lista = [tup + (1,) for tup in del_lista]
    add_lista = [tup + (2,) for tup in add_lista]
    del_add =  del_lista + add_lista

    del_add = sorted(del_add, key=lambda event: (event[1], event[2], event[3]))

    return del_add, currant_list_beton


def lista_in_text_beton(del_add_lista=True):
    """ "фотрмируем list в текстовый формат для высолки в бот"""
    lista_beton_del_add, lista_beton = check_del_add_lista()



    def convert_to_string(data):
        if not data:
            return ""
        try:
            data = str(data)
            data = data.strip()
            data = re.sub(r"\s+", " ", data)
            return data
        except (TypeError, ValueError):
            return ""

    if not lista_beton_del_add and del_add_lista:
        return ""
    
    if not lista_beton and not del_add_lista:
        return 'Brak danych'
    
    lista_text = ''

    if del_add_lista:


        for metres, times, firm, name, uwagi, przebieg, tel, wenz, sort in lista_beton_del_add:
            times = times.strftime("%H:%M")
            if tel:
                if isinstance(tel, float):
                    tel = str(int(tel)).strip()
                elif isinstance(tel, str):
                    tel = tel.strip()
            else:
                tel = ""

            przebieg = convert_to_string(przebieg)
            firm = convert_to_string(firm)
            name = convert_to_string(name)
            tel = convert_to_string(tel)
            uwagi = convert_to_string(uwagi)
            metres = str(metres).strip()
            if sort == 1:
                lista_text += (
                    f'<b>To kurwa dyspozytor usunął:</b>\n'
                    f'<s>{times} {metres} węzeł {wenz}</s>\n'
                    f'<s>{name} {uwagi + " " + przebieg}</s>\n'
                    f'--------------------\n')

            elif sort == 2:
                lista_text += (
                    f'<b>To kurwa dyspozytor dodał:</b>\n'
                    f'{times} {metres} węzeł {wenz}\n'
                    f'{name} {uwagi + " " + przebieg}\n'
                    f'--------------------\n')
            else:
                lista_text =  ''

        return lista_text
    
    else:
         for metres, times, firm, name, uwagi, przebieg, tel, wenz in lista_beton:
            times = times.strftime("%H:%M")
            if tel:
                if isinstance(tel, float):
                    tel = str(int(tel)).strip()
                elif isinstance(tel, str):
                    tel = tel.strip()
            else:
                tel = ""

            przebieg = convert_to_string(przebieg)
            firm = convert_to_string(firm)
            name = convert_to_string(name)
            tel = convert_to_string(tel)
            uwagi = convert_to_string(uwagi)
            metres = str(metres).strip()

            lista_text += (f"{times} {metres} węzeł {wenz}\n"
                           f'{firm}\n'
                           f'{name} {uwagi + " " + przebieg}\n'
                           f'{tel}\n'
                           f"--------------------\n")
            
         return lista_text


if __name__ == '__main__':
    # print(check_del_add_lista())
    print(lista_in_text_beton(False))
