import logging
import telebot
from telebot import types

from auth_data import token

def telegram_bot(token):
    bot = telebot.TeleBot(token)

    # Логирование ошибок
    logging.basicConfig(level=logging.INFO)

    # Переменные для хранения состояний пользователя
    user_state = {}

    # Список вопросов и сообщений
    questions = [
        "Где вы обо мне услышали и почему вас заинтересовала именно моя программа?",
        "Чего вы ждете от курса и какая проблема с речью у вас на данный момент?",
        "Где вы используете навык говорения? Это связано с вашей работой? Вы ведете блог или конференции, вы коуч или наставник?",
        "Что вы уже пробовали? Может быть, брали уроки по речи или вокалу, или занимались по моим роликам на YouTube?"
    ]

    text = 'Маша Ромаше дала сыворотку из-под простокваши. Маша \
    Ромаше дала сыворотку из-под простокваши. Маше дали кашу, а Саше простоквашу. Трудновыговариваемые слова назвали\
     трудновыговариваемыми потому, что их трудно выговаривать. У человека с плохо скоординированной координацией плохо\
      скоординированная походка. Трубач по улице идет, труба поет, труба ревет, труба трубит. Маланья-болтунья болтала,\
      болтала, что 33 корабля лавировали, лавировали, лавировали, лавировали, лавировали, да не вылавировали'

    audio_task_1 = f"Выполните первое задание: зачитайте как аудио сообщение следующий текст без репетиции: {text}"

    audio_task_2 = f"Прочтите еще раз текст как аудио сообщение: {text}"

    audio_task_3 = f"Зачитайте текст объемным низким голосом: {text}"

    final_message = "Переходите по ссылке и ознакомьтесь с условиями полной программы для качественного\
     изменения ГОЛОСА и РЕЧИ. https://elenaivankova.com/"

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
            user_state[call.message.chat.id] += 1
            bot.send_message(call.message.chat.id, "НАЖАТА КНОПКА 1")
            # как вызывать дочернюю функцию
            # next_question(call.message)

        elif call.data == "button2":
            user_state[call.message.chat.id] += 1

    # Приветствие
    @bot.message_handler(commands=['s'])
    def start_message(message):
        # bot.send_message(message.chat.id, " ")
        user_state[message.chat.id] = 0  # Устанавливаем начальное состояние пользователя
        markup = types.InlineKeyboardMarkup(row_width=1)  # Создаем разметку с кнопками
        btn1 = types.InlineKeyboardButton("Посмотреть расписание на сегодня", callback_data="button1")
        btn2 = types.InlineKeyboardButton("Посмотреть текущую погоду", callback_data="button2")
        btn3 = types.InlineKeyboardButton("Найти TОЧНЫЙ АДРЕС БУДОВЫ", callback_data="button3")
        btn4 = types.InlineKeyboardButton("ТЕЛЕФОНЫ КОЛЛЕГ", callback_data="button4")
        btn5 = types.InlineKeyboardButton("ГДЕ ПРОДАТЬ БЕТОН", callback_data="button5")
        btn6 = types.InlineKeyboardButton("Посмотреть где, кто сейчас находится", callback_data="button6")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6)  # Добавляем кнопки в разметку
        bot.send_message(message.chat.id, "ЧЕМ Я МОГУ ПОМОЧЬ:", reply_markup=markup)



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
