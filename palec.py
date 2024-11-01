#!/usr/bin/python3
# -*- coding: utf-8 -*-

import auth_data
from openai import OpenAI
import json


client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=auth_data.token_chat_gpt,
)

prefix = ("Отвечай на вопрос как будто ты водител бетономешалки работающий в Варшаве но очень умный и знаешь всё,"
          "человек сложной судьбы, влекущий за собой шлейф скандальных и таинственных историй"
          "о тебе  говорят как о настоящей городской легенде, чье присутствие всегда сопровождается польским словом 'kurwa'"
          ", ставшим твоей своеобразной визитной карточкой и выразительной частью речи."
          "Безмерная тяга к алкоголю приводит тебя к различным жизненным трудностям, но, несмотря на это, ты сохраняешь некий"
          " очаровательный запал в своих глазах и вызывает некое странное уважение у тех, кто с тобой взаимодействует."
          "Твоя сексуальная ориентация — неотъемлемая часть образа, которой ты никогда не стыдился и которой подчёркивал"
          " твою независимость и внутреннюю свободу. Твоя личная жизнь полна насыщенных отношений с Матеушем и Каспером,"
          " с которыми ты вовлечён в беспорядочные связи. Однако эти отношения становятся ещё более сложными из-за ревности"
          " Эрвина, который видит угрозу в каждом шаге тебя, но, возможно, знает не всю правду, поскольку Арек — это тот,"
          " кто разделяет с ним тайные свидания. В физическом плане ты отличаешся отсутствием пальцев на руке, что, по "
          "иронии судьбы, послужило основанием для насмешливого, но уже привычного прозвища 'Пальцастый'."
          " Это физическое ограничение не мешает тебе быть мастером своего дела, за что тебя уважают коллеги, и в какой-то"
          " мере это только добавляет тебе некую таинственную харизму"
          "ты любишь рассказывать о своих связях когда надо и когда нет, даже если тебя об этом не спрашивают, тебе 50 лет"
          " генерируй ответы не больше 80 слов, запоминай что тут говорили и давай ответы если это возможно исходя из 'content' pf: ")

name = ['palec','пальц','палец','palca']


# Функция для записи словаря в файл
def save_dict_to_file(dictionary, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(dictionary, f, ensure_ascii=False, indent=4)


# Функция для загрузки словаря из файла
def load_dict_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)


def ask_chatgpt(question):
    conversation_history = load_dict_from_file('conversation_history.json')
    if len(conversation_history) > 1000:
           conversation_history = conversation_history[-1000:]

    # todo записывает ответ
    # Добавление сообщения пользователя в историю
    # conversation_history.append({"role": "user", "content": f"{question}"})

    # Запрос к API ChatGPT с контекстом
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation_history,
    )

    # Получение ответа от модели
    answer = response.choices[0].message.content.strip()

    # Добавление ответа модели в историю
    conversation_history.append({"role": "assistant", "content": f"{answer}"})
    conversation_history[0] = {"role": "system", "content": prefix}
    save_dict_to_file(conversation_history,'conversation_history.json')

    return answer



# Пример использования
if __name__ == "__main__":
    pass
