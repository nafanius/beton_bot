import logging
from datetime import datetime, timedelta

import threading
import data_sql_list
import form_lista_with_teg

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

def check_del_add_lista(change_status):
    del_lista = []
    add_lista = []
    now = datetime.now()

    if now.weekday() > 5: 
        now = now + timedelta(days=1) # если воскресенье давай инащкьацию понедельника

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
    # del_lista = del_lista + currant_list_beton[2:5]
    # add_lista = add_lista + currant_list_beton[0:3]

    # меняем статус
    if id_event_time and change_status:
        with db_lock:
            data_sql_list.update_status('beton', id_event_time)
            
    del_lista = list(map(form_lista_with_teg.converter, del_lista))
    add_lista = list(map(form_lista_with_teg.converter, add_lista))
    currant_list_beton = list(map(form_lista_with_teg.converter, currant_list_beton))

    del_lista, add_lista = form_lista_with_teg.compare_lists_by_tuples(del_lista, add_lista)


    del_add =  del_lista + add_lista

    del_add = sorted(del_add, key=lambda event: (event[1], event[2], event[3]))
    inf(f"________________{del_add}_____________")
    return del_add, currant_list_beton


def lista_in_text_beton(del_add_lista=True):
    """ "фотрмируем list в текстовый формат для высолки в бот"""
    lista_beton_del_add, lista_beton = check_del_add_lista(del_add_lista)


    if not lista_beton_del_add and del_add_lista:
        return ""
    
    if not lista_beton and not del_add_lista:
        return 'Brak danych'
    
    lista_text = ''

    if del_add_lista:

        for metres, times, firm, name, uwagi, przebieg, tel, wenz in lista_beton_del_add:
        
            lista_text += (
                f'<b>To kurwa dyspozytor zmienił:</b>\n'
                f'{firm}\n'
                f'{times} {metres} węzeł {wenz}\n'
                f'{name} {uwagi + " " + przebieg}\n'
                f'--------------------\n')

        return lista_text
    
    else:
        for metres, times, firm, name, uwagi, przebieg, tel, wenz in lista_beton:

            lista_text += (f"{times} {metres} węzeł {wenz}\n"
                           f'{firm}\n'
                           f'{name} {uwagi + " " + przebieg}\n'
                           f'{tel}\n'
                           f"--------------------\n")
            
        return lista_text


if __name__ == '__main__':
    # print(check_del_add_lista())
    print(lista_in_text_beton(True))
