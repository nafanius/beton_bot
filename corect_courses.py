from datetime import datetime
import time
import data_sql_list
import pandas as pd
import threading
import logging


# region logging

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s")
lg = logging.debug
cr = logging.critical
inf = logging.info
exp = logging.exception
# logging.disable(logging.DEBUG)
# logging.disable(logging.INFO)
# logging.disable(logging.CRITICAL)
# logging_end
# endregion





db_lock = threading.Lock()


def save_corect_course(number, name_user, new_time=time.time()):
    query = f'SELECT * FROM actual WHERE "index" = {number}'

    try:
        with db_lock:
            df_restored_query = pd.read_sql_query(query, con=data_sql_list.engine)
    except Exception as error:
        inf(f"ошибка запроса из базы actual {error}")
        return True

    if df_restored_query.empty:
        return True
    
    else:
        df_restored_query[['new_time', 'user']] = new_time, name_user

        try:
            with db_lock:
                df_restored_query.to_sql('corrects', con=data_sql_list.engine, if_exists='append', index=False)
        
        except Exception as error:
            inf(f"ошибка запроса из базы actual {error}")
            return True
        
        return False

