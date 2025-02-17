from datetime import datetime
import time
import data_sql_list
import pandas as pd
import threading

db_lock = threading.Lock()


def save_corect_course(number, name_user, new_time=time.time()):
    query = f'SELECT * FROM actual WHERE "index" = {number}'


    with db_lock:
        df_restored_query = pd.read_sql_query(query, con=data_sql_list.engine)

    df_restored_query[['new_time', 'user']] = new_time, name_user

    with db_lock:
        df_restored_query.to_sql('corects', con=data_sql_list.engine, if_exists='append', index=False)

