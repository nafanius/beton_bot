"""настройки бота
"""


class Settings:
    data_base_lista = 'sqlite:////home/user/.database_lista/web_lista.db'
    data_base_bot = 'sqlite:////home/user/.database_bot/bot_database.db'
    ID_GROUPS = ["-4533287060", "-4768722432 "] # куда шлём
    message_without_bot = "Чёто ты меня притомил, давай ка помолчим kurwa"
    time_of_compare = 4

    def __init__(self):
        pass