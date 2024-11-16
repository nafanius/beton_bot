import json
import logging
import time
import os
from datetime import datetime
import threading
import subprocess


import telebot
from telebot import types

import weather
from auth_data import token
from palec import name, ask_chatgpt

# logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
lg = logging.debug
cr = logging.critical
inf = logging.info
exp = logging.exception
# logging.disable(logging.DEBUG)
# logging.disable(logging.INFO)
# logging.disable(logging.CRITICAL)
# logging_end


id_group = "-4533287060"
name_bud = ""
message_without_bot = "Чёто ты меня притомил, давай ка помолчим kurwa"
lista = {}
db_lock = threading.Lock()

def restart_service():
    subprocess.run(['systemctl', 'restart', 'my_bot_bet.service'])


#region  SAVE AND LOAD JSON
# Функция для записи словаря в файл
def save_dict_to_file(dictionary, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(dictionary, f, ensure_ascii=False, indent=4)

# Функция для загрузки словаря из файла
def load_dict_from_file(filename):
    if os.path.isfile(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({}, f, ensure_ascii=False, indent=4)
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
#endregion SAVE AND LOAD JSON


def telegram_bot(token):
    """основной цикл следящий за состоянием"""
    bot = telebot.TeleBot(token)

    # Логирование ошибок
    logging.basicConfig(level=logging.INFO)

    # Переменные для хранения состояний пользователя
    dict_contacts = {"Пальцастый": "+48570315464",
                     "Игорь": "+48572989696",
                     "Макс": "+48536519415",
                     "Олег": "+48791192036",
                     "Руслан": "+48513368948",
                     "Виталий": "+48576704688",
                     "Войтек": "+48517457662",
                     "Гура кальвария вензел": "+48502700711",
                     "Жерань вензел": "+48502786525",
                     "HOLCIM вензел 2": "+48502786916",
                     "HOLCIM вензел 1": "+48519537060"}

    # todo отремонтипровать приветствие каждого дня из за неё зависает ресберн
    def send_scheduled_message():
        """функция отсыла сообщений по утрам"""
        while True:
            now = datetime.now()
            if now.weekday() >= 5:
                time.sleep(500)  # Подождите 60 секунд перед следующей проверкой, если это выходной день
                continue

            # Проверьте если текущее время совпадает с запланированным (например, 9:00)
            if now.hour == 6 and now.minute == 30:
                global lista
                lista = load_dict_from_file('lista.json')
                weather_3day = weather.weather_3day()
                bot.send_message(id_group, f"*Добрейшее утро господа!*\n\n"
                                           f"*Сегодня запланировано отгрузить*  - _{lista['m']}m3_\n\n"
                                           f"*Расписание на сегодня* - _{lista['lista']}_\n\n"
                                           f"*Cегодня нас ждёт такая погода:*\n"
                                           f"Tемпература минимальная- {weather_3day[0]['температура минимальная']}\n"
                                           f"Tемпература максимальная - {weather_3day[0]['температура максимальная']}\n"
                                           f"Tемпература ощущение - {weather_3day[0]['temp']}\n"
                                           f"Oблачность  - {weather_3day[0]['облачность']}\n"
                                           f"Ветер  - {weather_3day[0]['ветер']}\n\n", parse_mode='Markdown')
                time.sleep(90)  # Пауза, чтобы избежать многократной отправки в течение той же минуты
            time.sleep(10)  # Проверка каждые 10 секунд

    # Запускаем поток для выполнения запланированного задания
    threading.Thread(target=send_scheduled_message).start()

    @bot.message_handler(content_types=['new_chat_members'])
    def welcome_new_member(message):
        """запуск при входе нового пользователя"""
        for new_member in message.new_chat_members:
            bot.send_message(message.chat.id,
                             f"Добро пожаловать, *{new_member.first_name}!*\n"
                             f"Ты находишся в чатике CONCRETных мужиков, "
                             f"льющих БЕТОН :)\n"
                             f"/h - для справки что тут можно делать", parse_mode='Markdown')

            bot.send_message(message.chat.id,
                             f"{new_member.first_name}\n:Набери:\n'/h' - и я тебе расскажу что я умею\n"
                             f"'/s' -  функции которые я могу выполнять \n")

    @bot.callback_query_handler(func=lambda call: True)
    def handle_callback(call):
        global lista
        answer_text = ""
        """"оброботка сробатывания кнопок"""
        if call.data == "button1": # расписание
            lista = load_dict_from_file('lista.json')
            answer_text = f"Cегодня запланировано отгрузить - {lista["m"]}m3\n{lista['lista']}"

        elif call.data == "button2": # погода
            try:
                weather_day = weather.weather_now()
                weather_3day = weather.weather_3day()
                answer_text = (f"*Погода сейчас:*\n"
                               f"Tемпература - {weather_day['температура']}\n"
                               f"Oблачность  - {weather_day['облачность']}\n"
                               f"Ветер  - {weather_day['ветер']}\n"
                               f"Восход  - {weather_day['восход']}\n"
                               f"Заход  - {weather_day['заход']}\n\n"
                               f"*Погода завтра:*\n"
                               f"Tемпература минимальная- {weather_3day[1]['температура минимальная']}\n"
                               f"Tемпература максимальная - {weather_3day[1]['температура максимальная']}\n"
                               f"Tемпература ощущение - {weather_3day[1]['temp']}\n"
                               f"Oблачность  - {weather_3day[1]['облачность']}\n"
                               f"Ветер  - {weather_3day[1]['ветер']}\n\n"
                               f"*Погода послезавтра:*\n"
                               f"Tемпература минимальная- {weather_3day[2]['температура минимальная']}\n"
                               f"Tемпература максимальная - {weather_3day[2]['температура максимальная']}\n"
                               f"Tемпература ощущения - {weather_3day[2]['temp']}\n"
                               f"Oблачность  - {weather_3day[2]['облачность']}\n"
                               f"Ветер  - {weather_3day[2]['ветер']}\n\n")
            except Exception:
                return
        elif call.data == "button3": # будовы
            answer = []
            dic_bud = load_dict_from_file('dic_bud.json')
            for key in dic_bud.keys():

                answer.append(f'<a href="https://www.google.com/maps?q={dic_bud[key][0]},{dic_bud[key][1]}">'
                               f'*{key}*</a>')

            answer_text = "Будовы:\nпо щелчку откроется геолокация\n" + "\n".join(answer)
        elif call.data == "button4":
            list_of_phone = []
            for key in dict_contacts.keys():
                list_of_phone.append(f'{key} <a href="tel:{dict_contacts[key]}">{dict_contacts[key]}</a>')
            answer_text = '\n'.join(list_of_phone)
        elif call.data == "button5":
            answer_text = (f'<a href="https://www.google.pl/maps/place/MD+Beton+Marek+D%C4%'
                           f'85browski/@52.1922286,20.7767505,17z/data=!3m1!4b1!4m6!3m5!1s0x4719'
                           f'352a34873e2b:0xc1fcd68e6bb8d915!8m2!3d52.1922253!4d20.7793254!16s%2'
                           f'Fg%2F1tf9l_k3?entry=ttu&g_ep=EgoyMDI0MTAyMy4wIKXMDSoASAFQAw%3D%3D">'
                           f'*MD BETON:*</a>\n'
                           f'ТЕЛЕФОН: <a href="tel:+48602593954">+48602593954</a>\n\n'
                           f'<a href="https://www.google.com/maps/place/Korzenna+3,+02-981+Warszawa'
                           f'/@52.1946406,21.0970687,17z/data=!3m1!4b1!4m6!3m5!1s0x471ed2a36aa060c7:'
                           f'0x714094a9a28101a0!8m2!3d52.1946406!4d21.099649!16s%2Fg%2F11c251zhvh?entry'
                           f'=ttu&g_ep=EgoyMDI0MTAyOS4wIKXMDSoASAFQAw%3D%3D">'
                           f'*Pawel:*</a>\n'
                           f'ТЕЛЕФОН: <a href="tel:+48505966026">+48505966026</a>')


        elif call.data == "button6":
            answer_text = "ФУНКЦИЯ В РАЗРАБОТКЕ, НЕМНОГО ТЕРПЕНИЯ!"
        try:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=answer_text,
                                  reply_markup=call.message.reply_markup, parse_mode='HTML')
        except Exception as error:
            inf(error)



    @bot.message_handler(commands=['s'])
    def start_message(message):
        """сробатывание на команду слэш с"""
        markup = types.InlineKeyboardMarkup()  # Создаем разметку с кнопками
        btn1 = types.InlineKeyboardButton("расписание", callback_data="button1")
        btn2 = types.InlineKeyboardButton("погоду", callback_data="button2")
        btn3 = types.InlineKeyboardButton("будовы", callback_data="button3")
        btn4 = types.InlineKeyboardButton("телефоны", callback_data="button4")
        btn5 = types.InlineKeyboardButton("ГДЕ ПРОДАТЬ БЕТОН", callback_data="button5")
        btn6 = types.InlineKeyboardButton("посмотреть что сейчас на заводе", callback_data="button6")
        markup.row(btn1 ,btn2)
        markup.row(btn3 ,btn4)
        markup.add(btn5)  # Добавляем кнопки в разметку
        markup.add(btn6)  # Добавляем кнопки в разметку
        bot.send_message(message.chat.id, "*ЧЕМ Я МОГУ ПОМОЧЬ*:", reply_markup=markup, parse_mode='Markdown')

    # help
    @bot.message_handler(commands=['h'])
    def help_message(message):
        """сробатывание на команду слэш аш"""""
        bot.send_message(message.chat.id, f"{message.from_user.first_name}\n"
                                          f"Я бот помогающий дать всю необходимую информацию для начинающих и"
                                          f" продвинутых бетономешальщиков\n"
                                          f"Hабери:\n'/h' - и я тебе расскажу что я умею\n"
                                          f"'/s' -  функции которые я могу выполнять \n")

#region ADD BUDOWA
    @bot.message_handler(commands=['add'])
    def add_budowa(message):
        """записываем адрес и локализацию будовы"""
        msg = bot.send_message(message.chat.id, "Введите название", reply_markup=types.ForceReply())
        bot.register_next_step_handler(msg, ask_name_budowy)

    def ask_geolocation(message): # Ответ корректен, продолжаем
        if message.content_type == 'location':
            # Ответ корректен, продолжаем
            global name_bud
            lat = message.location.latitude
            lon = message.location.longitude
            dic_bud = load_dict_from_file("dic_bud.json")
            dic_bud[name_bud] = [lat, lon]
            with db_lock:
                save_dict_to_file(dic_bud, "dic_bud.json")
            bot.send_message(message.chat.id, "ПРИНЯТО!")
        else:
            # Ответ некорректен, просим ввести снова
            msg = bot.send_message(message.chat.id, "Вышлите геолокацию")
            bot.register_next_step_handler(msg, ask_geolocation)

    def ask_name_budowy(message) :# Ответ корректен, продолжаем
        if message.content_type == 'text':
            global name_bud
            # Ответ корректен, продолжаем
            name_bud = message.text
            bot.send_message(message.chat.id, "Укажите свою геолокацию", reply_markup=types.ForceReply() )
            bot.register_next_step_handler(message, ask_geolocation)
        else:
            # Ответ некорректен, просим ввести снова
            msg = bot.send_message(message.chat.id, "ВВЕДИТЕ ТЕКСТ - Название будовы")
            bot.register_next_step_handler(msg, ask_name_budowy)
#endregion ADD BUDOWA

# region add plan meters
    @bot.message_handler(commands=['m'])
    def how_much_m_message(message):
        msg = bot.send_message(message.chat.id, "введите метры", reply_markup=types.ForceReply())
        bot.register_next_step_handler(msg, ask_how_much)

    def ask_how_much(message):
        if message.content_type == 'text':
            global how_much_m
            # Ответ корректен, продолжаем
            lista["m"] = message.text
            with db_lock:
                save_dict_to_file(lista, 'lista.json')
            bot.send_message(message.chat.id, "ПРИНЯТО")
        else:
            # Ответ некорректен, просим ввести снова
            msg = bot.send_message(message.chat.id, "ВВЕДИТЕ ТЕКСТ - СКОЛЬКО МЕТРОВ ЗАПЛАНИРОВАНО")
            bot.register_next_step_handler(msg, ask_how_much)
# endregion add plan meters

# region add list
    @bot.message_handler(commands=['l'])
    def lista_message(message):
        msg = bot.send_message(message.chat.id, "введите listu", reply_markup=types.ForceReply())
        bot.register_next_step_handler(msg, ask_listu)

    def ask_listu(message):
        if message.content_type == 'text':
            global lista
            # Ответ корректен, продолжаем
            lista["lista"] = message.text
            with db_lock:
                save_dict_to_file(lista, 'lista.json')
            bot.send_message(message.chat.id, "ПРИНЯТО")
        else:
            # Ответ некорректен, просим ввести снова
            msg = bot.send_message(message.chat.id, "ВВЕДИТЕ ТЕКСТ - СКОЛЬКО МЕТРОВ ЗАПЛАНИРОВАНО")
            bot.register_next_step_handler(msg, ask_how_much)
# endregion add list

    # text
    @bot.message_handler(content_types=['text'])
    def handle_text(message):
        global name_bud
        global how_much_m
        global lista
        text_message = message.text
        # Игнорируем сообщения от пользователей, которые не находятся в состоянии ожидания ответа
        if message.content_type == 'text':
            conversation_history = load_dict_from_file('conversation_history.json')
            if len(conversation_history) > 1000:
                conversation_history = conversation_history[-1000:]

            conversation_history.append({"role": "user", "content": f"{message.from_user.first_name}: {message.text}"})

            bot_name = text_message.split()[0].lower()[:5]
            if bot_name in name:
                conversation_history[-1] = {"role": "user",
                                            "content": f"{message.from_user.username} question: {message.text}"}
                with db_lock:
                    save_dict_to_file(conversation_history, 'conversation_history.json')

                split_text = text_message.split()
                text_message = ' '.join(split_text[1:])
                # пробуем получить ответ от чат бота
                try:
                    bot.reply_to(message, ask_chatgpt(text_message))
                except:
                    bot.reply_to(message, message_without_bot)
            else:
                with db_lock:
                    save_dict_to_file(conversation_history, 'conversation_history.json')

    retries = 5
    for i in range(retries):
        try:
            bot.polling(none_stop=True)
        except Exception as err:
            inf(err)
            if i < retries -1:
                time.sleep(8)
                continue
            else:
                restart_service()
                break


if __name__ == '__main__':
    telegram_bot(token)
