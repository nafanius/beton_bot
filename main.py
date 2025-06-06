import json
import time
import os
from datetime import datetime
import threading
import subprocess
import src.get_lista
import re
import src.corect_courses
import src.get_answer

from wit import Wit
import io
from pydub import AudioSegment
from gtts import gTTS

import telebot
from telebot import types

import src.weather as weather
from src.auth_data import token_bot
import src.auth_data as auth_data
from AI_gpt.palec import name, ask_chatgpt
from src.save_lista_bethon import lista_in_text_beton
from src.setting import Settings, inf, lg, timer
from src.get_request import answer_to_request


client_Wit = Wit(auth_data.cod_wit)
name_bud = ""
db_lock = threading.Lock()


def restart_service():
    """Restart the service using systemctl
    """    
    try:
        subprocess.run(['sudo','systemctl', 'restart', 'my_bot_bet.service'])
        lg("Service restarted successfully.")
    except subprocess.CalledProcessError as e:
        lg(f"Failed to restart service: {e}")


# region SAVE AND LOAD JSON
# todo region save and load json, rebuild it with db
def save_dict_to_file(dictionary, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(dictionary, f, ensure_ascii=False, indent=4)


def load_dict_from_file(filename):
    if os.path.isfile(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({}, f, ensure_ascii=False, indent=4)
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)


# endregion SAVE AND LOAD JSON


def telegram_bot(token):
    """main function for telegram bot

    Args:
        token (str): token for telegram bot
    """    
    bot = telebot.TeleBot(token)

    # todo make it as a database
    dict_contacts = {"Palcasty": "+48570315464",
                     "Ighor": "+48572989696",
                     "Maks": "+48536519415",
                     "Olech": "+48791192036",
                     "Ruslan": "+48513368948",
                     "Witalij": "+48576704688",
                     "Wojtek": "+48517457662",
                     "Gura Kalvaria węzeł": "+48502700711",
                     "Żerań węzeł": "+48502786525",
                     "HOLCIM węzeł 2": "+48502786916",
                     "HOLCIM węzeł 1": "+48519537060"}

    def send_scheduled_message():
        """function for sending scheduled messages
        """        
        
        try:
            while True:
                now = datetime.now()
                if now.weekday() > 5:
                    time.sleep(10800)  # check every 3 hours on weekends
                    continue

                # check if it's time to send the morning message
                if now.hour == 6 and now.minute == 30:
                    weather_3day = weather.weather_3day()
                    bot.send_message(Settings.ID_GROUPS[0], f"<b>Dzień dobry, panowie!</b>\n\n"
                                            f"<b>Harmonogram na dzisiaj</b>\n {src.get_lista.combination_of_some_days_list(True)}"
                                            f"<b>Dziś czeka nas taka pogoda:</b>\n"
                                            f"Temperatura minimalna <b><u>{weather_3day[0]['температура минимальная']}</u></b>\n"
                                            f"Maksymalna temperatura <b><u>{weather_3day[0]['температура максимальная']}</u></b>\n"
                                            f"Temperatura odczuwalna <b><u>{weather_3day[0]['temp']}</u></b>\n"
                                            f"zachmurzenie <b><u>{weather_3day[0]['облачность']}</u></b>\n"
                                            f"wiatr <b><u>{weather_3day[0]['ветер']}</u></b>\n", parse_mode='HTML')
                    time.sleep(90)  # check every 90 seconds to avoid multiple sends in the same minute

                # check if it's time to send the evening message
                # send infojrmation about changes in chromonogram 
                if now.minute in [7, 27, 47] :
                    text_list_beton = lista_in_text_beton()
                    text_lista = src.get_lista.combination_of_some_days_list()

                    if text_list_beton:
                        for id in Settings.ID_GROUPS:
                            bot.send_message(id, str(text_list_beton), parse_mode='HTML')
                            time.sleep(2) 

                    if text_lista:
                        for id in Settings.ID_GROUPS:
                            bot.send_message(id, text_lista, parse_mode='HTML')
                            time.sleep(2)

                    time.sleep(90)  # puse for 90 seconds to avoid multiple sends in the same minute
                time.sleep(20)  # check every 20 seconds
        except Exception as err:  # if error occurs, log it and restart the service
            inf(err)
            restart_service()
                

    # lounch thread for scheduled messages
    threading.Thread(target=send_scheduled_message).start()

    @bot.message_handler(content_types=['new_chat_members'])
    def welcome_new_member(message):
        """triggered when a new member joins the chat

        Args:
            message (object): passed from wrapper telebot, contains information about the new member
        """        
        for new_member in message.new_chat_members:
            bot.send_message(message.chat.id,
                             f"Witamy, <b>{new_member.first_name}!</b>\n"
                             f"Jesteś na czacie CONCRETnych facetów, "
                             f"lejących BETON :)\n"
                             f"/h - dla informacji, co można tu robić", parse_mode='HTML')

            bot.send_message(message.chat.id,
                             f"{new_member.first_name}\n:Wpisz:\n'/h' - a ja ci opowiem, co potrafię\n"
                             f"'/start' -  funkcje, które mogę wykonywać\n", parse_mode='HTML' )

    # region tap on Button
    @bot.callback_query_handler(func=lambda call: True)
    def handle_callback(call):
        """processing tap on button in inline keyboard
        """ 
        answer_text = []
              
        if call.data == "button1":  # shedule
            answer_text.append(src.get_lista.combination_of_some_days_list(True))

        elif call.data == "button2":  # weather
            try:
                weather_day = weather.weather_now()
                weather_3day = weather.weather_3day()
                answer_text.append((f"<b>Pogoda teraz:</b>\n"
                               f"Temperatura <b><u>{weather_day['температура']}</u></b>\n"
                               f"Zachmurzenie <b><u>{weather_day['облачность']}</u></b>\n"
                               f"Wiatr <b><u>{weather_day['ветер']}</u></b>\n"
                               f"Wschód <b><u>{weather_day['восход']}</u></b>\n"
                               f"Zachód <b><u>{weather_day['заход']}</u></b>\n\n"
                               f"<b>Pogoda na jutro:</b>\n"
                               f"Temperatura minimalna <b><u>{weather_3day[1]['температура минимальная']}</u></b>\n"
                               f"Temperatura maksymalna <b><u>{weather_3day[1]['температура максимальная']}</u></b>\n"
                               f"Temperatura odczuwalna <b><u>{weather_3day[1]['temp']}</u></b>\n"
                               f"Zachmurzenie <b><u>{weather_3day[1]['облачность']}</u></b>\n"
                               f"Wiatr <b><u>{weather_3day[1]['ветер']}</u></b>\n\n"
                               f"<b>Pogoda na pojutrze:</b>\n"
                               f"Temperatura minimalna <b><u>{weather_3day[2]['температура минимальная']}</u></b>\n"
                               f"Temperatura maksymalna <b><u>{weather_3day[2]['температура максимальная']}</u></b>\n"
                               f"Temperatura odczuwalna <b><u>{weather_3day[2]['temp']}</u></b>\n"
                               f"Zachmurzenie <b><u>{weather_3day[2]['облачность']}</u></b>\n"
                               f"Wiatr <b><u>{weather_3day[2]['ветер']}</u></b>\n\n"))

            except Exception as err:
                inf(err)
                return
        
        elif call.data == "button3":  # construction sites
            answer = []
            dic_bud = load_dict_from_file('dic_bud.json')
            for key in dic_bud.keys():
                answer.append(f'<a href="https://www.google.com/maps?q={dic_bud[key][0]},{dic_bud[key][1]}">'
                              f'*{key}*</a>')

            answer_text.append("Budowy:\npo kliknięciu otworzy się geolokalizacja\n" + "\n".join(answer))
        
        elif call.data == "button4": # contacts
            list_of_phone = []
            for key in dict_contacts.keys():
                list_of_phone.append(f'{key} <a href="tel:{dict_contacts[key]}">{dict_contacts[key]}</a>')
            answer_text.append('\n'.join(list_of_phone))
        
        elif call.data == "button5": # where to sell concrete
            answer_text.append((f'<a href="https://www.google.pl/maps/place/MD+Beton+Marek+D%C4%'
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
                           f'ТЕЛЕФОН: <a href="tel:+48505966026">+48505966026</a>\n\n'))
        
        elif call.data == "button6": # loading schedule
            answer_text = lista_in_text_beton(False)

        try:
            if len(answer_text) > 1:
                send_long_message(call.message.chat.id, answer_text, parse_mode='HTML')
            else:    
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=answer_text[0],
                                        reply_markup=call.message.reply_markup, parse_mode='HTML')
            
        except Exception as error:
            inf(error)

    # endregion tap on Button

    def send_long_message(chat_id, text, parse_mode='HTML'):
        for mes in text:
            bot.send_message(chat_id, text=mes, parse_mode=parse_mode)

    @bot.message_handler(commands=['start'])
    def start_message(message):
        """answering on command /start

        Args:
            message (object): passed from wrapper telebot, contains information about the message
        """        
        print(message.chat.id)
        markup = types.InlineKeyboardMarkup()  # markup for inline keyboard
        btn1 = types.InlineKeyboardButton("rozkład", callback_data="button1")
        btn2 = types.InlineKeyboardButton("pogodę", callback_data="button2")
        btn3 = types.InlineKeyboardButton("budowy", callback_data="button3")
        btn4 = types.InlineKeyboardButton("telefony", callback_data="button4")
        btn5 = types.InlineKeyboardButton("gdzie sprzedać beton", callback_data="button5")
        btn6 = types.InlineKeyboardButton("harmonogram załadunków", callback_data="button6")
        markup.row(btn1, btn2)
        markup.row(btn3, btn4)
        markup.add(btn5)  # Добавляем кнопки в разметку
        markup.add(btn6)  # Добавляем кнопки в разметку
        bot.send_message(message.chat.id, "*Czym mogę pomóc?*:", reply_markup=markup, parse_mode='HTML')

    # help
    @bot.message_handler(commands=['h'])
    def help_message(message):
        """answering on command /h

        Args:
            message (object): passed from wrapper telebot, contains information about the message
        """        
        bot.send_message(message.chat.id, f"{message.from_user.first_name}\n"
                                          f"Jestem botem, który pomaga dostarczyć wszystkie niezbędne informacje dla początkujących i"
                                          f" zaawansowanych operatorów betonomeszarek\n"
                                          f"Wpisz:\n'/h' - i opowiem ci, co potrafię\n"
                                          f"Wpisz:\n'/co' - i opowiem ci, co będą ładować w ciągu najbliższych 30 minut \n"
                                          f"Powiedz:\nPowiedz mi <code>PALEC</code> i swoje pytanie, a opowiem ci wszystko, co chcesz\n"
                                          f"Podaj:\nPodaj numer  - '<tg-spoiler>chuj/хуй12</tg-spoiler>' lub '<tg-spoiler>сhuj/хуй</tg-spoiler> 12:00' i, jeśli cię teraz ładują\n"
                                          f"Wpisz:\n<code>?'Nazwa budowy'</code> i/lub 'numer kursu' a ja ci powiem numer chuja\n"
                                          f"'/start' -  Funkcje, które mogę wykonywać\n"
                                          f"'/lista' - Wyświetlić rozkład\n", parse_mode='HTML')

    @bot.message_handler(commands=["lista"])
    def send_lista(message):
        """answering on command /lista

        Args:
            message (object): passed from wrapper telebot, contains information about the message
        """        
        bot.send_message(message.chat.id, "Oto ci, <tg-spoiler>kurwa</tg-spoiler>, rozkład: https://bit.ly/holcim_lista", parse_mode='HTML')

    @bot.message_handler(commands=["co"])
    def send_answer(message):
        bot.send_message(message.chat.id, answer_to_request(), parse_mode='HTML')

    # todo сделать стройки в виде базы данных
    # region ADD BUDOWA
    @bot.message_handler(commands=['add'])
    def add_budowa(message):
        """answering on command /add

        Args:
            message (object): passed from wrapper telebot, contains information about the message
        """        
        msg = bot.send_message(message.chat.id, "Wprowadź nazwę", reply_markup=types.ForceReply(), parse_mode='HTML')
        bot.register_next_step_handler(msg, ask_name_budowy)

    def ask_geolocation(message):
        """asking for geolocation

        Args:
            message (object): passed from wrapper telebot, contains information about the message
        """        
        if message.content_type == 'location':
            # answer correct, continue
            global name_bud
            lat = message.location.latitude
            lon = message.location.longitude
            dic_bud = load_dict_from_file("dic_bud.json")
            dic_bud[name_bud] = [lat, lon]
            with db_lock:
                save_dict_to_file(dic_bud, "dic_bud.json")
            bot.send_message(message.chat.id, "Przyjęto!", reply_markup=None, parse_mode='HTML')
        else:
            # answer incorrect, ask again
            msg = bot.send_message(message.chat.id, "Wyślij lokalizację", parse_mode='HTML')
            bot.register_next_step_handler(msg, ask_geolocation)

    def ask_name_budowy(message):
        """asking for name of budowa

        Args:
            message (object): passed from wrapper telebot, contains information about the message
        """        
        if message.content_type == 'text':
            global name_bud
            # answer correct, continue
            name_bud = message.text
            bot.send_message(message.chat.id, "Podaj swoją lokalizacjęУ", reply_markup=types.ForceReply(), parse_mode='HTML')
            bot.register_next_step_handler(message, ask_geolocation)
        else:
            # answer incorrect, ask again
            msg = bot.send_message(message.chat.id, "Wprowadź tekst - Nazwa budowy", parse_mode='HTML')
            bot.register_next_step_handler(msg, ask_name_budowy)

    # endregion ADD BUDOWA

    # text
    @bot.message_handler(content_types=['text'])
    def handle_text(message):
        """cathe all text messages and looking first worlds Palec, ?, <tg-spoiler>Chuj, хуй</tg-spoiler>, and if it looks for then send answer

        Args:
            message (object): passed from wrapper telebot, contains information about the message
        """        
        text_message = message.text
        # added message from user to conversation history for chatgpt bot
        if message.content_type == 'text':
            conversation_history = load_dict_from_file('conversation_history.json')
            if len(conversation_history) > 150:
                conversation_history = conversation_history[-75:]
            conversation_history.append({"role": "user", "content": f"{message.from_user.first_name}: {message.text}"})

            bot_name = text_message.split()[0].lower()[:3]

            request_corect_corse = text_message.lower()
            pattern_huy = Settings.pattern_huy
            pattern_question = Settings.pattern_question

            match_huy = re.search(pattern_huy, request_corect_corse)
            match_question = re.search(pattern_question, request_corect_corse)

            if bot_name in name and str(message.chat.id) in Settings.ID_SEND_BOT:
                conversation_history[-1] = {"role": "user",
                                            "content": f"{message.from_user.username} question: {message.text}"}

                with db_lock:
                    save_dict_to_file(conversation_history, 'conversation_history.json')

                split_text = text_message.split()
                text_message = ' '.join(split_text[1:])
                # try to get answer from chat bot
                try:
                    bot.reply_to(message, ask_chatgpt(text_message))
                except Exception as err:
                    inf(err)
                    bot.reply_to(message, Settings.message_without_bot)
            elif match_huy:
                number_course = match_huy.group(1)
                time_corse = match_huy.group(2)

                if not time_corse:
                    answer_from_lista = src.corect_courses.save_corect_course(number_course, message.from_user.username, datetime.now())
                else:
                    today = datetime.today()
                    time_parts = time_corse.split(':')
                    hours = int(time_parts[0])
                    minutes = int(time_parts[1])
                    date_time_course = datetime(today.year, today.month, today.day, hours, minutes)
                    answer_from_lista = src.corect_courses.save_corect_course(number_course, message.from_user.username, date_time_course)

                bot.reply_to(message, answer_from_lista)

            elif match_question:
                request = match_question.group(1)
                request_kurs = match_question.group(2)
                if request_kurs:
                    request_kurs = int(request_kurs)

                answer_from_request = src.get_answer.answer_to_request(request, request_kurs)
                bot.reply_to(message, answer_from_request, parse_mode='HTML')
                
            else:
                with db_lock:
                    save_dict_to_file(conversation_history, 'conversation_history.json')

    def palec_voice(message):
        """cathe all voice messages and looking first worlds Pal, if it looks for then send answer anather voice
        message saved in conversation history

        Args:
            message (_type_): _description_
        """        
        try:
            # getting voice message file
            file_info = bot.get_file(message.voice.file_id)
            # downloading the file
            downloaded_file = bot.download_file(file_info.file_path) # type: ignore
            ogg_audio = io.BytesIO(downloaded_file)
            audio = AudioSegment.from_file(ogg_audio, format="ogg")
            wav_audio_io = io.BytesIO()
            audio.export(wav_audio_io, format="wav")
            wav_audio_io.seek(0)
            wav_binary_data = wav_audio_io.read()

            # converting voice message to text using Wit.ai
            resp = client_Wit.speech(wav_binary_data, {'Content-Type': 'audio/wav'})

            text_message = resp['text']
        except Exception as err:
            inf(err)
            return
        pass

        conversation_history = load_dict_from_file('conversation_history.json')
        if len(conversation_history) > 300:
            conversation_history = conversation_history[-150:]

        try:
            bot_name = text_message.split()[0].lower()[:3]
        except IndexError:
            bot_name = ""


        if bot_name in name and str(message.chat.id) in Settings.ID_SEND_BOT:
            conversation_history[-1] = {"role": "user",
                                        "content": f"{message.from_user.username} question: {text_message}"}
            with db_lock:
                save_dict_to_file(conversation_history, 'conversation_history.json')

            split_text = text_message.split()
            text_message = ' '.join(split_text[1:])
            # try to get answer from chat bot
            try:
                # get answer from chatgpt
                tts = gTTS(ask_chatgpt(text_message), lang='ru')
                #  save answer to mp3 file
                mp3_fp = io.BytesIO()
                tts.write_to_fp(mp3_fp)
                mp3_fp.seek(0)

                # convert mp3 to ogg format
                audio = AudioSegment.from_file(mp3_fp, format="mp3")
                ogg_fp = io.BytesIO()
                audio.export(ogg_fp, format="ogg", codec="libopus")
                ogg_fp.seek(0)

                bot.send_voice(chat_id=message.chat.id, voice=ogg_fp, reply_to_message_id=message.message_id)

            except Exception as err:
                inf(err)
                bot.reply_to(message, Settings.message_without_bot)
        else:
            with db_lock:
                save_dict_to_file(conversation_history, 'conversation_history.json')

    @bot.message_handler(content_types=['voice'])
    def handle_voice(message):
        """cathe all voice messages and looking first worlds Palec, if it looks for then send voice answer 

        Args:
            message (object): passed from wrapper telebot, contains information about the message
        """        

        threading.Thread(target=palec_voice, args=(message,)).start()

    retries = 5
    for i in range(retries):
        try:
            bot.polling(none_stop=True)
        except Exception as err:
            inf(err)
            if i < retries - 1:
                time.sleep(8)
                continue
            else:
                restart_service()
                break


if __name__ == '__main__':
    telegram_bot(token_bot)
