import pickle
import logging
import os
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
    return del_lista, add_lista


if __name__ == '__main__':
    print(check_del_add_lista())