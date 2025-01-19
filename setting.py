"""настройки бота
"""


class Settings:
    data_base = 'sqlite:////home/user/.database_lista/web_lista.db'
    # id_group = "-4533287060"
    ADMIN_ID = ["-4533287060", ] # куда шлём
    message_without_bot = "Чёто ты меня притомил, давай ка помолчим kurwa"
    cod_wit = 'HZZJUIX7N6O7LJ2XNNSPN2ZTFGLWQCF6'
    time_of_compare = 4

    def __init__(self):
        pass