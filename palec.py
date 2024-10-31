#!/usr/bin/python3
# -*- coding: utf-8 -*-

import readline
import auth_data
from openai import OpenAI


client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=auth_data.token_chat_gpt,
)

conversation_history = []
prefix = ("Отвечай на вопрос как будто ты водител бетономешалки работающий в Варшаве но очень умный и знаешь всё,"
          "тебя зовут 'пальцастый' но так же могут называть 'палец' "
          "у тебя любовь и половые отношения с Мартиным и иногда с Каспером, но вас ревнует Эрвин, об этих отношениях "
          "ты всем рассказываешь когда надо и когда нет, даже если тебя об этом не спрашивают, тебе 50 лет ты любишь выпить,"
          " и через каждое слово добавляешь слово 'курва'"
          " отвечай на вопрос котрый находится после сочитания символов - '%%:'  %%: ")
name = ['palec','пальцастый','палец','palcasty']

def ask_chatgpt(question):
    global conversation_history
    if len(conversation_history) > 50:
           conversation_history = conversation_history[-50:]
    # Добавление сообщения пользователя в историю
    conversation_history.append({"role": "user", "content": f"{prefix} {question}"})

    # Запрос к API ChatGPT с контекстом
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=conversation_history
    )

    # Получение ответа от модели
    answer = response.choices[0].message.content.strip()

    # Добавление ответа модели в историю
    conversation_history.append({"role": "assistant", "content": answer})

    return answer



# Пример использования
if __name__ == "__main__":
    pass
