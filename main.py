import json
import logging
from time import daylight

import weather
import telebot
from telebot import types
from auth_data import token


def telegram_bot(token):
    bot = telebot.TeleBot(token)

    # Логирование ошибок
    logging.basicConfig(level=logging.INFO)

    # Переменные для хранения состояний пользователя
    user_state = {}

    @bot.message_handler(content_types=['new_chat_members'])
    def welcome_new_member(message):
        for new_member in message.new_chat_members:
            bot.send_message(message.chat.id,
                             f"Добро пожаловать, {new_member.first_name}! Ты находишся в чатике CONCRETных мужиков,"
                             f"льющих БЕТОН")

            bot.send_message(message.chat.id,
                             f"{new_member.first_name}\n:набери '/h' - и я тебе расскажу что я умею\n"
                             f"'/s' -  функции которые я могу выполнять \n")

    @bot.callback_query_handler(func=lambda call: True)
    def handle_callback(call):
        if call.data == "button1":
            bot.send_message(call.message.chat.id, "ФУНКЦИЯ В РАЗРАБОТКЕ, НЕМНОГО ТЕРПЕНИЯ!")

        elif call.data == "button2":
            weather_day = weather.weather_now()
            weather_2day = weather.weather_3day()
            bot.send_message(call.message.chat.id, f"*Погода сейчас:*\n"
                                                   f"Tемпература - {weather_day['температура']}\n"
                                                   f"Oблачность  - {weather_day['облачность']}\n"
                                                   f"Ветер  - {weather_day['ветер']}\n"
                                                   f"Восход  - {weather_day['восход']}\n"
                                                   f"Заход  - {weather_day['заход']}\n\n"
                                                   f"*Погода завтра:*\n"
                                                   f"Tемпература минимальная- {weather_2day[0]['температура минимальная']}\n"
                                                   f"Tемпература максимальная - {weather_2day[0]['температура максимальная']}\n"
                                                   f"Tемпература ощущение - {weather_2day[0]['temp']}\n"
                                                   f"Oблачность  - {weather_2day[0]['облачность']}\n"
                                                   f"Ветер  - {weather_2day[0]['ветер']}\n\n"
                                                   f"*Погода послезавтра:*\n"
                                                   f"Tемпература минимальная- {weather_2day[1]['температура минимальная']}\n"
                                                   f"Tемпература максимальная - {weather_2day[1]['температура максимальная']}\n"
                                                   f"Tемпература ощущения - {weather_2day[1]['temp']}\n"
                                                   f"Oблачность  - {weather_2day[1]['облачность']}\n"
                                                   f"Ветер  - {weather_2day[1]['ветер']}\n\n",
                             parse_mode='Markdown')
        elif call.data == "button3":
            bot.send_message(call.message.chat.id, "ФУНКЦИЯ В РАЗРАБОТКЕ, НЕМНОГО ТЕРПЕНИЯ!")
        elif call.data == "button4":
            bot.send_message(call.message.chat.id, "ФУНКЦИЯ В РАЗРАБОТКЕ, НЕМНОГО ТЕРПЕНИЯ!")
        elif call.data == "button5":
            bot.send_message(call.message.chat.id, "*MD BETON:*\n", parse_mode='Markdown')
            bot.send_message(call.message.chat.id, f'<a href="tel:+48602593954">+48602593954</a>', parse_mode='HTML')
            bot.send_location(call.message.chat.id, 52.192, 20.779)

        elif call.data == "button6":
            bot.send_message(call.message.chat.id, "ФУНКЦИЯ В РАЗРАБОТКЕ, НЕМНОГО ТЕРПЕНИЯ!")



    # Приветствие
    @bot.message_handler(commands=['s'])
    def start_message(message):
        # bot.send_message(message.chat.id, " ")
        user_state[message.chat.id] = 0  # Устанавливаем начальное состояние пользователя
        markup = types.InlineKeyboardMarkup(row_width=1)  # Создаем разметку с кнопками
        btn1 = types.InlineKeyboardButton("ПОСМОТРЕТЬ РАСПИСАНИЕ НА СЕГОДНЯ", callback_data="button1")
        btn2 = types.InlineKeyboardButton("ПОСМОТРЕТЬ ТЕКУЩУЮ ПОГОДУ", callback_data="button2")
        btn3 = types.InlineKeyboardButton("НАЙТИ ТОЧНЫЙ АДРЕС БУДОВЫ", callback_data="button3")
        btn4 = types.InlineKeyboardButton("ТЕЛЕФОНЫ КОЛЛЕГ", callback_data="button4")
        btn5 = types.InlineKeyboardButton("ГДЕ ПРОДАТЬ БЕТОН", callback_data="button5")
        btn6 = types.InlineKeyboardButton("ПОСМОТРЕТЬ ГДЕ, КТО СЕЙЧАС НАХОДИТЬСЯ", callback_data="button6")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6)  # Добавляем кнопки в разметку
        bot.send_message(message.chat.id, "*ЧЕМ Я МОГУ ПОМОЧЬ*:", reply_markup=markup, parse_mode='Markdown')

    # help
    @bot.message_handler(commands=['h'])
    def help_message(message):
        bot.send_message(message.chat.id, f"{message.from_user.first_name}\n"
                                          f"Я бот помогающий дать всю необходимую информацию для начинающих и продвинутых бетономешальщиков\n"
                                          f"Hабери '/h' - и я тебе расскажу что я умею\n"
                                          f"'/s' -  функции которые я могу выполнять \n")
        user_state[message.chat.id] = 0  # Устанавливаем начальное состояние пользователя

    @bot.message_handler(commands=['add'])
    def add_message(message):

        # Функция для записи словаря в файл
        def save_dict_to_file(dictionary, filename):
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(dictionary, f, ensure_ascii=False, indent=4)

        # Функция для загрузки словаря из файла
        def load_dict_from_file(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)

        dic_bud = load_dict_from_file("dic_bud.json")

        """добавляем будову"""
        bot.send_message(message.chat.id, f"{message.from_user.first_name}\n"
                                          f"Я бот помогающий дать всю необходимую информацию для начинающих и продвинутых бетономешальщиков\n"
                                          f"Hабери '/h' - и я тебе расскажу что я умею\n"
                                          f"'/s' -  функции которые я могу выполнять \n")
        user_state[message.chat.id] = 0  # Устанавливаем начальное состояние пользователя

    #
    # # Обработка текстовых ответов
    # @bot.message_handler(content_types=['text'])
    # def handle_text(message):
    #     state = user_state.get(message.chat.id, 0)
    #     logging.info(f" state handle_text {state}")
    #
    #     # if state == 0:
    #     #     return
    #     if message.chat.id not in user_state:
    #         return
    #
    #     if state == len(questions) or state == len(questions) + 2 or state == len(questions) + 5:
    #         bot.send_message(message.chat.id, "Пожалуйста, отправьте аудиосообщение, как указано в задании.")
    #         return
    #
    #     if state < len(questions):
    #         user_state[message.chat.id] += 1
    #         next_question(message)
    #
    #     elif state == len(questions):
    #         user_state[message.chat.id] += 1
    #         next_question(message)
    #
    #     elif state == len(questions) + 1:
    #         user_state[message.chat.id] += 1
    #         next_question(message)
    #
    #     elif state == len(questions) + 2:
    #         user_state[message.chat.id] += 1
    #         next_question(message)
    #
    #     elif state == len(questions) + 3:
    #         user_state[message.chat.id] += 1
    #         next_question(message)
    #
    #     elif state == len(questions) + 4:
    #         user_state[message.chat.id] += 1
    #         next_question(message)
    #
    #     elif state == len(questions) + 6:
    #         user_state[message.chat.id] += 1
    #         next_question(message)
    #
    #     elif state == len(questions) + 7:
    #         user_state[message.chat.id] += 1
    #         next_question(message)
    #
    #     elif state == len(questions) + 8:
    #         user_state[message.chat.id] += 1
    #         next_question(message)
    #
    #     elif state == len(questions) + 9:
    #         user_state[message.chat.id] +=
    #         next_question(message)
    #
    #     elif state == len(questions) + 10:
    #         user_state[message.chat.id] += 1
    #         next_question(message)
    #
    # @bot.message_handler(content_types=['voice'])
    # def handle_audio(message):
    #     bot.send_message(message.chat.id, "Спасибо за ваше аудиосообщение!")
    #     user_state[message.chat.id] += 1
    #     next_question(message)
    #
    # # Функция для перехода к следующему вопросу
    # def next_question(message):
    #
    #     state = user_state.get(message.chat.id, 0)
    #     logging.info(state)
    #     if state < len(questions):
    #         bot.send_message(message.chat.id, questions[state])
    #     elif state == len(questions):
    #         bot.send_message(message.chat.id, audio_task_1)
    #
    #     elif state == len(questions) + 1:
    #         bot.send_message(message.chat.id,
    #                          "Прямо сейчас выполните все упражнения по этому видео\n https://youtu.be/BaSK40u4Kq4")
    #
    #         markup = types.InlineKeyboardMarkup()  # Создаем разметку с кнопками
    #         btn1 = types.InlineKeyboardButton("Проверочное задание 1", callback_data="button1")
    #         markup.add(btn1)  # Добавляем кнопки в разметку
    #         bot.send_message(message.chat.id, "После выполнения нажмите на кнопку", reply_markup=markup)
    #
    #         # handle_text(message)
    #     elif state == len(questions) + 2:
    #         bot.send_message(message.chat.id, audio_task_2)
    #     elif state == len(questions) + 3:
    #         bot.send_message(message.chat.id,
    #                          "Послушайте предыдущее аудио. Напишите, есть ли изменения в вашей дикции.")
    #
    #     elif state == len(questions) + 4:
    #         bot.send_message(message.chat.id, "Выполните все упражнения по этому видео https://youtu.be/VlbLHjPnQ3w")
    #         markup = types.InlineKeyboardMarkup()  # Создаем разметку с кнопками
    #         btn2 = types.InlineKeyboardButton("Проверочное задание 2", callback_data="button2")
    #         markup.add(btn2)  # Добавляем кнопки в разметку
    #         bot.send_message(message.chat.id, "После выполнения нажмите на кнопку", reply_markup=markup)
    #
    #     elif state == len(questions) + 5:
    #         bot.send_message(message.chat.id, audio_task_3)
    #     elif state == len(questions) + 6:
    #         bot.send_message(message.chat.id, "Есть ли изменения в вашей дикции и голосе после двух уроков?")
    #
    #     elif state == len(questions) + 7:
    #         bot.send_message(message.chat.id, final_message)

    bot.polling(none_stop=True)


if __name__ == '__main__':
    telegram_bot(token)
