import pickle
import logging
import os, re
from datetime import datetime

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


def save_dic_to_pickle(lists, directory ="save_old_lists"):
    """
    Сохраняет словарь в файл формата pickle.

    :param directory:
    :param lists: списков с текущим выводом del и add
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
    # Генерация имени нового файла
    new_filename = "last_lists.pkl"
    filename = os.path.join(directory, new_filename)

    with open(filename, 'wb') as f:
        pickle.dump(lists, f)




def load_dict_from_pickle(directory = "save_old_dict"):
    """
    Загружает список из файла формата pickle.

    :param filename: Имя файла, из которого нужно загрузить словарь.
    :return: Загруженный словарь.
    """

    files = [
        (file, os.path.getmtime(os.path.join(directory, file)))
        for file in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, file))
    ]

    # Если есть файлы, ищем самый старый
    if files:
        newest_file = max(files, key=lambda f: f[1])[0]
        filename = os.path.join(directory, newest_file)

    try:
        with open(filename, 'rb') as f:
            return pickle.load(f)
    except Exception as err:
        print(err)
        return {}

def get_list_of_beton(directory = "save_old_lists"):
    """
    Загружает список из файла формата pickle.

    :param filename: Имя файла, из которого нужно загрузить словарь.
    :return: списки
    """
    filename = os.path.join(directory, "last_lists.pkl")
    try:
        with open(filename, 'rb') as f:
            return pickle.load(f)
    except Exception as err:
        print(err)
        return {}



def check_del_add_lista():
    del_lista = []
    add_lista = []
    now = datetime.now()
    date_of_lista = now.strftime('%d.%m.%Y')
    currant_list_beton = load_dict_from_pickle('../weblista/save_old_dict').get(date_of_lista, [])
    old_stan_lista_beton = get_list_of_beton().get(date_of_lista, [])
    if not old_stan_lista_beton:
        old_stan_lista_beton = currant_list_beton

    for i in old_stan_lista_beton:
        if i not in currant_list_beton:
            del_lista.append(i)
    for i in currant_list_beton:
        if i not in old_stan_lista_beton:
            add_lista.append(i)

    # для контроля отображения
    # del_lista = del_lista + currant_list_beton[2:3]
    # add_lista = add_lista + currant_list_beton[0:2]

    save_dic_to_pickle({date_of_lista:currant_list_beton})


    del_lista = [tup + (1,) for tup in del_lista]
    add_lista = [tup + (2,) for tup in add_lista]
    return del_lista + add_lista


def lista_in_text_beton():
    """ "фотрмируем list в текстовый формат для высолки в бот"""
    lista_beton = check_del_add_lista()

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

    if not lista_beton:
        return ""
    lista_text = ''



    for metres, times, firm, name, uwagi, przebieg, tel, wenz, sort in lista_beton:
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
                f'*To kurwa dyspozytor usunął:*\n'
                f'~~{times} {metres} węzeł {wenz}~~\n'
                f'~~{firm}~~\n'
                f'~~{name} {uwagi + " " + przebieg}~~\n'
                f'~~{tel}~~\n'
                f'--------------------\n')

        elif sort == 2:
            lista_text += (
                f'*To kurwa dyspozytor dodał:*\n'
                f'{times} {metres} węzeł {wenz}\n'
                f'{firm}\n'
                f'{name} {uwagi + " " + przebieg}\n'
                f'{tel}\n'
                f'--------------------\n')
        else:
            lista_text =  ''

    return lista_text


if __name__ == '__main__':
    print(check_del_add_lista())
    print(lista_in_text_beton())
