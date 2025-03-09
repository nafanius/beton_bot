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

def answer_to_request(request, request_kurs):
    query_try = f'SELECT * FROM actual_after'
    with db_lock:
        df_try = pd.read_sql_query(query_try, con=data_sql_list.engine)

    df_source  = df_try[df_try['budowa'].str.contains(request, case=False, na=False)]

    if request_kurs:
        df_source = df_source[df_source['k'] == request_kurs]

    if df_source.empty:
        return "Курва чё-то ты тупишь, и впариваешь мне какую то дичь"
    
    df_source['time'] = pd.to_datetime(df_source['time'])
    df_source['time'] = df_source['time'].dt.strftime("%H:%M")
    
    df_source = df_source.astype(str)
    df_source.set_index('index', inplace=True)
    df_source = df_source.drop(['id', 'mat'], axis=1)

    df_source['time'] = '<b>'+df_source['time'].str.strip()+'</b>'
    df_source['k'] = 'k - '+df_source['k'].str.strip()
    df_source['res'] = 'res - '+df_source['res'].str.strip()+':::'
    df_source['budowa'] = df_source['budowa'].str.strip()+':::'
    df_source['p/d'] = (df_source['p/d'].str.strip()).replace({'d':'dzwig:::','p':'pompa:::'})
    df_source['split'] = '----------------'

    df_source = df_source.reindex(['time', 'm3', 'k', 'res', 'budowa', 'p/d','split'], axis=1)

    text = df_source.to_string(header=False, index_names=False)
    text = text.replace(":::", "\n")
    text = re.sub(r'[ \t]+', ' ', text).strip()

    text =  f"<b>КИДАЙ НОМЕР ХУЯ\nЕсли грузят сейчас - хуй2\nЕсли хуй бросаешь на время - хуй2 7:00 :</b>\n{text}"

    return text




if __name__ == '__main__':

    query_try = f'SELECT * FROM actual_after '
    with db_lock:
        df_try = pd.read_sql_query(query_try, con=data_sql_list.engine)

