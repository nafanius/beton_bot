import db_driver.data_sql_list as data_sql_list
import pandas as pd
import threading
import re

db_lock = threading.Lock()

def answer_to_request():
    """Generate an answer to the current loading status.
    This function retrieves the current loading status from the database and formats it for display.

    Returns:
        str: A formatted string containing the current loading status, including remaining volume and number of courses.
    """    
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
    resz_courses = df_after_time.shape[0]

    if df_now_loading.empty and resz_courses == 0:
        return 'kolego, możesz być wolny jak wiatr <tg-spoiler>kurwa</tg-spoiler>'
    elif df_now_loading.empty and resz_courses != 0:
        return f"<b>W ciągu najbliższych 45 minut to będą ładować:</b>\nDzisiaj pozostało <b><u>{reszta}m3,\n kursów - {resz_courses}</u></b>"
    

    df_now_loading.set_index('index', inplace=True)
    df_now_loading = df_now_loading.drop(['id', 'mat'], axis=1)
    df_now_loading['time'] = df_now_loading['time'].dt.strftime("%H:%M")
    df_now_loading['m3'] = df_now_loading['m3'].round(1)
    df_now_loading['res'] = df_now_loading['res'].round(1)
    df_now_loading = df_now_loading.astype(str)
    df_now_loading['time'] = '<b>'+df_now_loading['time'].str.strip()+'</b>'
    df_now_loading['k'] = 'kurs-'+df_now_loading['k'].str.strip()
    df_now_loading['wenz'] = 'węnz-'+df_now_loading['wenz'].str.strip()+':::'
    df_now_loading['res'] = 'reszta - '+df_now_loading['res'].str.strip()
    df_now_loading['budowa'] = df_now_loading['budowa'].str.strip()+':::'
    df_now_loading['p/d'] = (df_now_loading['p/d'].str.strip()).replace({'d':'dzwig:::','p':'pompa:::'})
    df_now_loading['split'] = '----------------'

    df_now_loading = df_now_loading.reindex(['time', 'm3', 'k', 'wenz', 'budowa', 'res','p/d','split'], axis=1)

    text = df_now_loading.to_string(header=False)
    text = text.replace(":::", "\n")
    text = re.sub(r'[ \t]+', ' ', text).strip()
    text =  f"<b>W ciągu najbliższych 45 minut to będą ładować:</b>\nDzisiaj pozostało <b><u>{reszta}m3,\n kursów - {resz_courses}"\
            f"</u></b>\n\n{text}\n\n <u>Jeśli coś jest nie tak, nie len się, podaj <tg-spoiler>chuj/хуй</tg-spoiler> z numerem załadunku na przykład:"\
            f"<b>'<tg-spoiler>хуй10</tg-spoiler>'- jeśli w tym momencie ładuje, lub '<tg-spoiler>хуй10 9:20</tg-spoiler>'</b></u>"

    return text




if __name__ == '__main__':

    query_try = f'SELECT * FROM actual_after '
    with db_lock:
        df_try = pd.read_sql_query(query_try, con=data_sql_list.engine)

