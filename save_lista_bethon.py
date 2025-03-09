import logging
from datetime import datetime, timedelta
import re
import pandas as pd
import threading
import data_sql_list
import form_lista_with_teg

# region logging

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
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
        # если воскресенье давай инащкьацию понедельника
        now = now + timedelta(days=1)

    date_of_lista = now.strftime("%d.%m.%Y")

    with db_lock:
        currant_list_beton, id_event_time, status = (
            data_sql_list.get_newest_list_beton_or_lista(
                "beton", date_of_lista, 0)
        )

    with db_lock:
        old_stan_lista_beton = data_sql_list.get_newest_list_beton_or_lista(
            "beton", date_of_lista, 1
        )[0]
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
            data_sql_list.update_status("beton", id_event_time)

    del_lista = list(map(form_lista_with_teg.converter, del_lista))
    add_lista = list(map(form_lista_with_teg.converter, add_lista))
    currant_list_beton = list(
        map(form_lista_with_teg.converter, currant_list_beton))

    del_lista, add_lista = form_lista_with_teg.compare_lists_by_tuples(
        del_lista, add_lista
    )

    del_add = del_lista + add_lista

    del_add = sorted(del_add, key=lambda event: (event[1], event[2], event[3]))

    inf(f"________________{del_add}_____________")
    return del_add, currant_list_beton



def split_string_by_newline(input_string, max_length=4095):

    if len(input_string) <= max_length:
        list_string = input_string.replace('ZZZ', "")
        
        return [input_string]

    parts = []
    chank =''

    list_string = input_string.split('ZZZ')

    for number, i in enumerate(list_string):

        if len(chank) < max_length:
            chank = chank+i
            if number == len(list_string)-1:
                parts.append(chank)
        else:
            parts.append(chank)
            chank = i
    
    return parts

def lista_in_text_beton(del_add_lista=True):
    """ "фотрмируем list в текстовый формат для высолки в бот"""
    lista_beton_del_add, _ = check_del_add_lista(del_add_lista)

    if not lista_beton_del_add and del_add_lista:
        return ""

    # todo del it if not be able any problems
    # if not lista_beton and not del_add_lista:
    #     return "Brak danych"

    lista_text = ""

    if del_add_lista:

        for (
            metres,
            times,
            firm,
            name,
            uwagi,
            przebieg,
            tel,
            wenz,
            *_,
        ) in lista_beton_del_add:

            lista_text += (
                f"{times} {metres} węzeł {wenz}\n"
                f"{firm}\n"
                f'{name} {uwagi + " " + przebieg}\n'
                f"--------------------\n"
            )

        return "<b>To kurwa dyspozytor zmienił:</b>\n" + lista_text

    else:
        query_try = f'SELECT * FROM actual_after '
        
        with db_lock:
            df_try = pd.read_sql_query(query_try, con=data_sql_list.engine)

        df_try['time'] = pd.to_datetime(df_try['time'])

        if df_try.empty:
            lista_text = ['dzisiaj nie ma wysyłek kurwa']
        else:
            df_try.set_index('index', inplace=True)
            df_try = df_try.drop(['id', 'mat'], axis=1)
            df_try['time'] = df_try['time'].dt.strftime("%H:%M")
            df_try['m3'] = df_try['m3'].round(1)
            df_try['res'] = df_try['res'].round(1)
            df_try = df_try.astype(str)
            df_try['time'] = '<b>'+df_try['time'].str.strip()+'</b>'
            df_try['k'] = 'kurs-'+df_try['k'].str.strip()
            df_try['wenz'] = 'węnz-'+df_try['wenz'].str.strip()+':::'
            df_try['res'] = 'reszta-'+df_try['res'].str.strip()
            df_try['budowa'] = df_try['budowa'].str.strip()+':::'
            df_try['p/d'] = (df_try['p/d'].str.strip()).replace({'d':'dzwig:::','p':'pompa:::'})
            df_try['split'] = '------------ZZZ'

            df_try = df_try.reindex(['time', 'm3', 'k', 'wenz', 'budowa', 'res','p/d','split'], axis=1)

            lista_text = df_try.to_string(header=False)
            lista_text = lista_text.replace(":::", "\n")
            lista_text = re.sub(r'[ \t]+', ' ', lista_text).strip()

            lista_text = split_string_by_newline(lista_text)

        return lista_text


if __name__ == "__main__":
    # print(check_del_add_lista())
    print(lista_in_text_beton(True))
