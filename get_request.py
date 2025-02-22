import data_sql_list
import pandas as pd
import threading
import logging
import re

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

def answer_to_request():
    query_try = f'SELECT * FROM actual_after '
    with db_lock:
        df_try = pd.read_sql_query(query_try, con=data_sql_list.engine)

    df_try['time'] = pd.to_datetime(df_try['time'])

    # target_time = pd.Timestamp.now()- pd.Timedelta(hours=10) #for check
    target_time = pd.Timestamp.now()

    # todo remove minutes in setting
    start_time = target_time - pd.Timedelta(minutes=15)
    end_time = target_time + pd.Timedelta(minutes=30)

    df_now_loading = df_try[(df_try['time'] >= start_time) & (df_try['time'] <= end_time)]

    df_after_time = df_try[(df_try['time'] >= target_time)]
    reszta = df_after_time['m3'].sum()

    if df_now_loading.empty:
        return 'kolego, możesz być wolny jak wiatr kurwa'

    df_now_loading.set_index('index', inplace=True)
    df_now_loading = df_now_loading.drop(['id', 'mat'], axis=1)
    df_now_loading['time'] = df_now_loading['time'].dt.strftime("%H:%M")
    df_now_loading = df_now_loading.astype(str)

    df_now_loading['time'] = '<b>'+df_now_loading['time'].str.strip()+'</b>'
    df_now_loading['k'] = 'kurs - '+df_now_loading['k'].str.strip()
    df_now_loading['wenz'] = 'węnzeł - '+df_now_loading['wenz'].str.strip()+':::'
    df_now_loading['res'] = 'reszta - '+df_now_loading['res'].str.strip()
    df_now_loading['budowa'] = df_now_loading['budowa'].str.strip()+':::'
    df_now_loading['p/d'] = (df_now_loading['p/d'].str.strip()).replace({'d':'dzwig:::','p':'pompa:::'})
    df_now_loading['split'] = '----------------'

    df_now_loading = df_now_loading.reindex(['time', 'm3', 'k', 'wenz', 'budowa', 'res','p/d','split'], axis=1)

    text = df_now_loading.to_string(header=False)
    text = text.replace(":::", "\n")
    text = re.sub(r'[ \t]+', ' ', text).strip()
    text = f"<b>W ciągu najbliższych 45 minut to będą ładować:</b>\nDzisiaj pozostało do wysyłki <b><u>{reszta}"\
           f"</u></b>m3\n\n{text}\n\n <u>Eсли что не так, не поленись, кинь хуй с номером загрузки например: <b>'хуй10'</b></u>"

    return text




if __name__ == '__main__':

    query_try = f'SELECT * FROM actual_after '
    with db_lock:
        df_try = pd.read_sql_query(query_try, con=data_sql_list.engine)

