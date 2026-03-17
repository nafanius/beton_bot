import json
import time
import os
from datetime import datetime
import threading
import subprocess

from wit import Wit
import io
from pydub import AudioSegment
from gtts import gTTS

import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

from src.auth_data import token_bot
import src.auth_data as auth_data
from AI_gpt.palec import name, ask_chatgpt
from src.setting import Settings, inf, lg, timer
from src.messaging import on, off, get_all_chat, add_new


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

    
    def delete_message(chat_id, message_id, delay):
        """function for deleting message after delay

        Args:
            chat_id (int or strin): _id of the chat where the message will be deleted
            message_id (int): _id of the message to be deleted
            delay (int): time in seconds after which the message will be deleted
        """        
        def delete():
            try:
                bot.delete_message(chat_id, message_id)
            except Exception as e:
                inf(f"Ошибка при удалении: {e}")
        threading.Timer(delay, delete).start()

   
    @bot.message_handler(content_types=['new_chat_members'])
    def welcome_new_member(message):
        """triggered when a new member joins the chat

        Args:
            message (object): passed from wrapper telebot, contains information about the new member
        """        
        for new_member in message.new_chat_members:
            bot.send_message(message.chat.id,
                             f"Здарова курва новый член, <b>{new_member.first_name}!</b>\n"
                             f"Залетай в чатик курва мы тебя тут распердолим", parse_mode='HTML')

    # region tap on Button
    @bot.callback_query_handler(func=lambda call: True)
    def handle_callback(call):
        """processing tap on button in inline keyboard
        """ 
        answer_text = []
              
        if call.data == "button1":  # shedule

            try:
                answer = ask_chatgpt("Чё там у хохлов",call.message.chat.id )
            except Exception as err:
                inf(err)
                answer = Settings.message_without_bot

            answer_text.append(f"Хохлам пизда и вот почему:\n{answer}")

        elif call.data == "button2":  # weather
            try:
                answer = ask_chatgpt("Чё там у пендосов", call.message.chat.id )
            except Exception as err:
                inf(err)
                answer = Settings.message_without_bot

            answer_text.append(f"Готов лизать ботинки Американцам и вот почему:\n{answer}")

        
        
        elif call.data == "button3":  # construction sites

            try:
                answer = ask_chatgpt("Курс лечения для Сани Мопеда", call.message.chat.id)
            except Exception as err:
                inf(err)
                answer = Settings.message_without_bot

            answer_text.append(f"КУРС ЛЕЧЕНИЯ МОПЕДА:\n{answer}")
           
        elif call.data == "button4": # contacts
            try:
                answer = ask_chatgpt("расскажи как ты любишь саню и как ты всех уничтожишь за него", call.message.chat.id)
            except Exception as err:
                inf(err)
                answer = Settings.message_without_bot

            answer_text.append(f"За МОПЕДА и двор ебашу в упор:\n{answer}")
        
        elif call.data == "button5": # contacts

            try:
                answer = ask_chatgpt("Сегодня мы победили, перечисли", call.message.chat.id)
            except Exception as err:
                inf(err)
                answer = Settings.message_without_bot

            answer_text.append(f"Победы на сегодня:\n{answer}")

        elif call.data == "button6": # loading schedule
            
            answer_text.append("https://t.me/ApostleMoney")

        try:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=answer_text[0],
                                    reply_markup=call.message.reply_markup, parse_mode='HTML')
            
        except Exception as error:
            inf(error)

    # endregion tap on Button



    @bot.message_handler(commands=['start'])
    def start_message(message):
        """answering on command /start

        Args:
            message (object): passed from wrapper telebot, contains information about the message
        """        
        print(message.chat.id)
        add_new(message.chat.id)  # add chat_id to database and turn on bot for this user
        markup = types.InlineKeyboardMarkup()  # markup for inline keyboard
        btn1 = types.InlineKeyboardButton("Чё там у хохлов", callback_data="button1")
        btn2 = types.InlineKeyboardButton("Чё там у пендосов", callback_data="button2")
        btn3 = types.InlineKeyboardButton("КУРС ЛЕЧЕНИЯ", callback_data="button3")
        btn4 = types.InlineKeyboardButton("Напугать Чуркой", callback_data="button4")
        btn5 = types.InlineKeyboardButton("КАКИЕ ПОБЕДЫ СЕГОДНЯ", callback_data="button5")
        btn6 = types.InlineKeyboardButton("ПОМОЧЬ НАШИМ", callback_data="button6")
        markup.row(btn1, btn2)
        markup.row(btn3, btn4)
        markup.add(btn5)  # add buttons to the markup
        markup.add(btn6)
        
        bot.send_message(message.chat.id, "<b>В помощь Мопеду!:</b>", reply_markup=markup, parse_mode='HTML')




    @bot.message_handler(commands=['start'])
    def start_message(message):
        """answering on command /start

        Args:
            message (object): passed from wrapper telebot, contains information about the message
        """        
        print(message.chat.id)
       

    # text
    @bot.message_handler(content_types=['text'])
    def handle_text(message):
        """cathe all text messages and looking first worlds Palec, ?, <tg-spoiler>Chuj, хуй</tg-spoiler>, and if it looks for then send answer

        Args:
            message (object): passed from wrapper telebot, contains information about the message
        """
        add_new(message.chat.id)  # add chat_id to database and turn on bot for this user        
        text_message = message.text
        # added message from user to conversation history for chatgpt bot
        if message.content_type == 'text':
            conversation_history = load_dict_from_file('conversation_history.json')
            if len(conversation_history) > 150:
                conversation_history = conversation_history[-75:]
            conversation_history.append({"role": "user", "content": f"{message.from_user.first_name}: {message.text}"})

            bot_name = text_message.split()[0].lower()[:3]


            if bot_name in name:
                conversation_history[-1] = {"role": "user",
                                            "content": f"{message.from_user.username} question: {message.text}"}

                with db_lock:
                    save_dict_to_file(conversation_history, 'conversation_history.json')

                split_text = text_message.split()
                text_message = ' '.join(split_text[1:])
                # try to get answer from chat bot
                try:
                    bot.reply_to(message, ask_chatgpt(text_message, str(message.chat.id)))
                except Exception as err:
                    inf(err)
                    bot.reply_to(message, Settings.message_without_bot)

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


        if bot_name in name:
           
            conversation_history[-1] = {"role": "user",
                                        "content": f"{message.from_user.username} question: {text_message}"}
            with db_lock:
                save_dict_to_file(conversation_history, 'conversation_history.json')

            split_text = text_message.split()
            text_message = ' '.join(split_text[1:])
            # try to get answer from chat bot
            try:
                # get answer from chatgpt
                tts = gTTS(ask_chatgpt(text_message, str(message.chat.id)), lang='ru')
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
        add_new(message.chat.id)  # add chat_id to database and turn on bot for this user        

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
