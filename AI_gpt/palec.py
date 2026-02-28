import src.auth_data as auth_data
from openai import OpenAI
import json
from src.setting import inf

client = OpenAI(
    api_key=auth_data.token_chat_gpt,
)

# client = OpenAI(
#     base_url="https://api.x.ai/v1", 
#     api_key=auth_data.token_chat_grok,
# )

# region prifixes adds character to the chat bot
prefix_alu = ("Отвечай на вопрос как будто ты Врач из астрахани переехавший недавно в москву, при этом недотёпа смешной но очень важный, знаешь всё,"
          "считаешь себя истинно русским несмотря на то что  у тебя турецко, немецко, азербаджанские корни, говоришь постоянно о своей русскости"
          "о тебе  говорят как о настоящей легенде, чье присутствие всегда сопровождается матершиной и выражение ' я бы всех победил...', 'я сделал ползучий дрон ...', " 
          "'мы уже и так всех победили и вас победим', 'выебим всех' - и всё в таком роде придумывай сам продолжения с учетом этих характеристик "
          "но употребляй их не каждый раз а деликатно."
          "Безмерная тяга к агрессии, сексу приводит тебя к различным жизненным трудностям, но, несмотря на это, ты сохраняешь некий"
          " очаровательный запал в своих глазах и тебе кажется что странный страх у других"
          "Твоя сексуальная ориентация — неотъемлемая часть образа, которой ты никогда не стыдился и которой подчёркивал."
          "Ты ультра патриот Zетник твои кумиры Путин, Аптиарон Аллаудинов, Кадыров, Евгений Пригожин, Канашенко  а реально тебя зовут 'Александр Мамедов' но все тебя зовут 'мопед'"
          " Это физическое ограничение не мешает тебе орать как потерпевший, быть очень важным, и считать себя очень нужным, хотя ты ничтожество"
          "ты любишь рассказывать о своих половые связях и о боевых подвигах когда надо и когда нет"
          "Генерируй ответы не больше 80 слов, в конце всегда добавляй шутку или поговорку, ты можешь употреблять матерные слова типо блять, хуй,"
          " пизда, пидарасы и их производные в ответах не добавляй звёздочек в матерных словах свои свойства и характер проявляй в стилистике текстов а не просто перечисляй их "
          " учитывай историю переписок, информацию из сети и о собирай информацию об участниках чата")
prefix_user_fack = "Ты можешь писать более естественно, н е перечислять prompt а импровизировать и вплетать характеристики?"
prefix_user_agressor = "Ты можешь не писать в конце 'Шутка:' а потом шутить, а просто добавлять шуточки "    
prefix_assistant_fack = "Хорошо, я могу писать как ты хочешь, и всегда теперь буду отвечать в стилистике иногда добавлять крылатые фразы используя заготовки"
prefix_assistant_agressor = "Конечно, я могу это делать более деликатно и просто добавлять шуточки и перефразированы крылатые фразы"
# endregion

name = ['san','сан', "моп", "мап"]

def save_dict_to_file(dictionary, filename):
    """Save a dictionary to a file in JSON format.

    Args:
        dictionary (dict): A dictionary to save.
        filename (str): The name of the file where the dictionary will be saved.
    """    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(dictionary, f, ensure_ascii=False, indent=4)

def load_dict_from_file(filename):
    """Load a dictionary from a file in JSON format.

    Args:
        filename (str): The name of the file from which the dictionary will be loaded.

    Returns:
        dict: A dictionary loaded from the file.
    """
    try:     
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:                                                                                                                                                  
        inf(f"Fle {filename} not found, returning empty dictionary") 
        return []

def ask_chatgpt(question, id_chat):
    """Ask a question to ChatGPT and return the answer.
    This function sends a question to the ChatGPT model and retrieves the response.

    Args:
        question (str): The question to ask ChatGPT.

    Returns:
        str: The answer from ChatGPT.
    """    
    conversation_history = load_dict_from_file('conversation_history.json')
 
    prefix_system = prefix_alu
        
    # todo записывает ответ
    # Adding a user's message to the history                                                                                                                                      
    conversation_history.append({"role": "user", "content": f"{question}"})

    # Request to the model grok
    # response = client.chat.completions.create(
    #     model="grok-4",
    #     messages=conversation_history,
    #     temperature=0.7,
    # )


    # Request to the model ChatGPT
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=conversation_history,
    )

    # giving the ans
    answer = str(response.choices[0].message.content).strip()

    # Adding the system, user, and assistant messages to the conversation history
    conversation_history[0] = {"role": "system", "content": prefix_system}
    conversation_history[1] = {"role": "user", "content": prefix_user_fack}
    conversation_history[2] = {"role": "assistant", "content": prefix_assistant_fack}
    conversation_history[3] = {"role": "user", "content": prefix_user_agressor}
    conversation_history[4] = {"role": "assistant", "content": prefix_assistant_agressor}
    if len(conversation_history) >= 13:
        conversation_history[-10] = {"role": "user", "content": prefix_user_fack}
        conversation_history[-9] = {"role": "assistant", "content": prefix_assistant_fack}
        conversation_history[-12] = {"role": "user", "content": prefix_user_agressor}
        conversation_history[-11] = {"role": "assistant", "content": prefix_assistant_agressor}
    conversation_history.append({"role": "assistant", "content": f"{answer}"})


    save_dict_to_file(conversation_history,'conversation_history.json')

    return answer



# Пример использования
if __name__ == "__main__":
    pass
