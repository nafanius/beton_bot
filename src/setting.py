"""настройки бота
"""
import datetime
from pprint import pformat
import logging
import traceback
import time

class Settings:
    data_base_lista = 'sqlite:////home/user/.database_lista/web_lista.db'
    data_base_bot = 'sqlite:////home/user/.database_bot/bot_database.db'
    ID_GROUPS = ["-4533287060", "-4768722432"] # куда шлём
    ID_SEND_BOT = ["-4533287060", "-4768722432", "1276025555"] #куда отвечает бот голосом и текстом
    message_without_bot = "Чёто ты меня притомил, давай ка помолчим kurwa"
    time_of_compare = 4
    start_time_co = 15 # min before request CO
    finish_time_co = 15 # min after request CO
    pattern_huy = r'^(?:хуй|chuj)\s*(\d{1,3})\s*(?:((?:[01]?\d|2[0-3]):[0-5]\d))?$'
    pattern_question = r'^\?\s*([a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ]*)\s*(\d*)'
    def __init__(self):
        pass



# region logging
class PrettyFormatter(logging.Formatter):
       def format(self, record):
           # if message is a structured data, format it
           if isinstance(record.msg, (dict, list, tuple)):
               record.msg = pformat(record.msg)
           return super().format(record)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setFormatter(PrettyFormatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

lg = logger.debug
cr = logger.critical
inf = logger.info
exp = logger.exception
logging.disable(logging.DEBUG)
# logging.disable(logging.INFO)
# logging.disable(logging.CRITICAL)
# logging.disable(logging.EXCEPTION)
# endregion


def formating_error_message(error, name):
    """Format the error message for logging

    Args:
        error (Exception): error message

    Returns:
        str: formatted error message
    """
    err_type = type(error).__name__
    tb_str = traceback.format_exc()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    current_frame = traceback.extract_tb(error.__traceback__)[-1]
    function_name = current_frame.name

    explain_mistake = f"""
        Mistake mame: {name}
        Time: {timestamp}
        Type of error: {err_type}
        Message: {error}
        Function name: {function_name}
        Traceback:
        {tb_str}
        """

    return explain_mistake

def timer(func):
    """
    A decorator that measures and logs the execution time of the wrapped function.

    Args:
        func (callable): The function to be wrapped and timed.

    Returns:
        callable: The wrapped function with execution time logging.

    Logs:
            Logs the execution time of the function in seconds using the `inf` logger
    """
    def wrapper(*args, **kwargs):
        """
        A decorator function that measures the execution time of the wrapped function.

        Args:
            *args: Positional arguments to be passed to the wrapped function.
            **kwargs: Keyword arguments to be passed to the wrapped function.

        Returns:
            The result of the wrapped function.

        Logs:
            Logs the execution time of the wrapped function in seconds.
        """
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        inf(f"Function {func.__name__} executed for {end_time - start_time} seconds") 
        return result
    return wrapper