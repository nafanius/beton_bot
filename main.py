import json
import logging
from threading import Thread
import time
from datetime import datetime

import weather
import telebot
from telebot import types
from auth_data import token
from palec import name, ask_chatgpt


id_group = "-4533287060"
request_name_of_building = 1
request_location_of_building = 2
request_how_much_m = 3
request_lista = 4
name_bud = ""
user_state = {}
message_without_bot = "Чёто ты меня притомил, давай ка помолчим kurwa"
how_much_m = 860
lista = ""

def telegram_bot(token):
    """основной цикл следящий за состоянием"""
    bot = telebot.TeleBot(token)

    # Логирование ошибок
    logging.basicConfig(level=logging.INFO)

    # Переменные для хранения состояний пользователя
    dict_contacts = {"Пальцастый":"+48570315464",
                     "Игорь":"+48572989696",
                     "Макс":"+48536519415",
                     "Олег":"+48791192036",
                     "Руслан":"+48513368948",
                     "Виталил":"+48576704688",
                     "Войтек":"+48517457662",
                     "HOLCIM":"+48519537060"}

    # Функция для записи словаря в файл
    def save_dict_to_file(dictionary, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(dictionary, f, ensure_ascii=False, indent=4)

    # Функция для загрузки словаря из файла
    def load_dict_from_file(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)

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
                weather_3day = weather.weather_3day()
                bot.send_message(id_group, f"*Добрейшее утро господа!*\n\n"
                                           f"*Сегодня запланировано отгрузить*  - _{how_much_m}m3_\n\n"
                                           f"*Расписание на сегодня* - _{lista}_\n\n"
                                           f"*Cегодня нас ждёт такая погода:*\n"
                                           f"Tемпература минимальная- {weather_3day[0]['температура минимальная']}\n"
                                           f"Tемпература максимальная - {weather_3day[0]['температура максимальная']}\n"
                                           f"Tемпература ощущение - {weather_3day[0]['temp']}\n"
                                           f"Oблачность  - {weather_3day[0]['облачность']}\n"
                                           f"Ветер  - {weather_3day[0]['ветер']}\n\n", parse_mode='Markdown')
                time.sleep(90)  # Пауза, чтобы избежать многократной отправки в течение той же минуты
            time.sleep(10)  # Проверка каждые 10 секунд

    # Запускаем поток для выполнения запланированного задания
    Thread(target=send_scheduled_message).start()



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
        answer_text = ""
        """"оброботка сробатывания кнопок"""
        if call.data == "button1":
            answer_text = f"Cегодня запланировано отгрузить - {how_much_m}m3\n{lista}"

        elif call.data == "button2":
            try:
                weather_day = weather.weather_now()
                weather_3day = weather.weather_3day()
                answer_text =  (f"*Погода сейчас:*\n"
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
            except:
                return

        elif call.data == "button3":
            dic_bud = load_dict_from_file('dic_bud.json')
            for key in dic_bud.keys():


                 answer_text = (f'<a href="https://www.google.com/maps?q={dic_bud[key][0]},{dic_bud[key][1]}">'
                               f'*{key}*</a>')

        elif call.data == "button4":
            list_of_phone =[]
            for key in dict_contacts.keys():
                list_of_phone.append(f'{key} <a href="tel:{dict_contacts[key]}">{dict_contacts[key]}</a>')
            answer_text  = '\n'.join(list_of_phone)
        elif call.data == "button5":
            answer_text = (f'<a href="https://www.google.pl/maps/place/MD+Beton+Marek+D%C4%'
                           f'85browski/@52.1922286,20.7767505,17z/data=!3m1!4b1!4m6!3m5!1s0x4719'
                           f'352a34873e2b:0xc1fcd68e6bb8d915!8m2!3d52.1922253!4d20.7793254!16s%2'
                           f'Fg%2F1tf9l_k3?entry=ttu&g_ep=EgoyMDI0MTAyMy4wIKXMDSoASAFQAw%3D%3D">'
                           f'*MD BETON:*</a>\n'
                           f'ТЕЛЕФОН: <a href="tel:+48602593954">+48602593954</a>')
            # bot.send_message(call.message.chat.id, f'ТЕЛЕФОН: <a href="tel:+48602593954">+48602593954</a>',
            #                  parse_mode='HTML')

        elif call.data == "button6":
            answer_text = "ФУНКЦИЯ В РАЗРАБОТКЕ, НЕМНОГО ТЕРПЕНИЯ!"

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=answer_text,
                              reply_markup=call.message.reply_markup, parse_mode='HTML')



    # Приветствие
    @bot.message_handler(commands=['s'])
    def start_message(message):
        """сробатывание на команду слэш с"""
        user_state[message.chat.id] = 0  # Устанавливаем начальное состояние пользователя
        markup = types.InlineKeyboardMarkup(row_width=1)  # Создаем разметку с кнопками
        btn1 = types.InlineKeyboardButton("посмотреть расписание", callback_data="button1")
        btn2 = types.InlineKeyboardButton("посмотреть погоду", callback_data="button2")
        btn3 = types.InlineKeyboardButton("найти адрес будовы", callback_data="button3")
        btn4 = types.InlineKeyboardButton("телефоны", callback_data="button4")
        btn5 = types.InlineKeyboardButton("ГДЕ ПРОДАТЬ БЕТОН", callback_data="button5")
        btn6 = types.InlineKeyboardButton("посмотреть что сейчас на заводе", callback_data="button6")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6)  # Добавляем кнопки в разметку
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
        user_state[message.chat.id] = 0  # Устанавливаем начальное состояние пользователя

    @bot.message_handler(commands=['add'])
    def add_budowa(message):
        """записываем адрес и локализацию будовы"""
        bot.send_message(message.chat.id, "Введите название")
        user_state[message.chat.id] = request_name_of_building

    @bot.message_handler(commands=['m'])
    def how_much_m_message(message):
        bot.send_message(message.chat.id, "введите метры")
        user_state[message.chat.id] = request_how_much_m

    @bot.message_handler(commands=['l'])
    def lista_message(message):
        bot.send_message(message.chat.id, "введите listu")
        user_state[message.chat.id] = request_lista


    # Обработчик текста и геолакации
    @bot.message_handler(content_types=['text', 'location'])
    def handle_text(message):
        global name_bud
        global how_much_m
        global lista
        user_id = message.chat.id
        text_message = message.text
        # Игнорируем сообщения от пользователей, которые не находятся в состоянии ожидания ответа
        if message.content_type == 'text':
            print(message)

            conversation_history = load_dict_from_file('conversation_history.json')
            if len(conversation_history) > 1000:
                conversation_history = conversation_history[-1000:]

            conversation_history.append({"role": "user", "content": f"{message.from_user.first_name}: {message.text}"})

            bot_name = text_message.split()[0].lower()[:5]
            if bot_name in name:
                conversation_history[-1] = {"role": "user", "content": f"{message.from_user.username} question: {message.text}"}
                save_dict_to_file(conversation_history,'conversation_history.json')

                split_text = text_message.split()
                text_message = ' '.join(split_text[1:])
                # пробуем получить ответ от чат бота
                try:
                    bot.reply_to(message, ask_chatgpt(text_message))
                except:
                    bot.reply_to(message, message_without_bot)
            else:
                save_dict_to_file(conversation_history,'conversation_history.json')


            if user_id not in user_state:
                return
            # Обработка первого ответа
            if user_state[user_id] == request_name_of_building:
                bot.send_message(user_id, "Укажите свою геолокацию")
                name_bud = message.text
                user_state[user_id] = request_location_of_building
            elif user_state[user_id] == request_how_much_m:
                if message.text.isdigit():
                    how_much_m = message.text
                    del user_state[user_id]
                else:
                    bot.send_message(user_id, "ВВЕДИТЕ ЧИСЛО")

            elif user_state[user_id] == request_lista:
                lista = message.text
                del user_state[user_id]


        elif message.content_type == 'location':
            """обрабатывает получение геолокации для команды add"""
            user_id = message.chat.id
            if user_id not in user_state:
                return

            if user_state[user_id] == request_location_of_building:
                lat = message.location.latitude
                lon = message.location.longitude
                # После получения второго ответа можем очистить состояние.
                del user_state[user_id]
                dic_bud = load_dict_from_file("dic_bud.json")
                dic_bud[name_bud] = [lat, lon]
                print(dic_bud)
                save_dict_to_file(dic_bud, "dic_bud.json")


    bot.polling(none_stop=True)


if __name__ == '__main__':
    telegram_bot(token)
