"""настройки бота
"""


class Settings:
    data_base_lista = 'sqlite:////home/user/.database_lista/web_lista.db'
    data_base_bot = 'sqlite:////home/user/.database_bot/bot_database.db'
    ID_GROUPS = ["-4533287060", "-4768722432"] # куда шлём
    ID_SEND_BOT = ["-4533287060", "-4768722432", "1276025555"] #куда отвечает бот голосом и текстом
    message_without_bot = "Чёто ты меня притомил, давай ка помолчим kurwa"
    time_of_compare = 4
    start_time_co = 15 # min before request CO
    finish_time_co = 15 # min after request CO

    def __init__(self):
        pass