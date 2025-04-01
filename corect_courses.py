from datetime import datetime
import data_sql_list
import pandas as pd
import threading
import logging
from sqlalchemy import text as text_sql_request


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


def save_corect_course(number, name_user, new_time):

    if number == '001':
        delete_query = text_sql_request("DELETE FROM corrects")

        with db_lock:  
            with data_sql_list.engine.connect() as connection:
                connection.execute(delete_query)
                connection.commit()  

        return "я всё зачистил шеф!"

    query = f'SELECT * FROM actual_after WHERE "index" = {number}'

    try:
        with db_lock:
            df_restored_query = pd.read_sql_query(query, con=data_sql_list.engine)
    except Exception as error:
        inf(f"ошибка запроса из базы actual {error}")
        return "Курва чё-то ты намутил с базой данных при получении данных"

    if df_restored_query.empty:
        return "Курва чё-то ты тупишь, и впариваешь мне какую то дичь"
    
    else:
        df_restored_query[['new_time', 'user']] = new_time, name_user

        try:
            with db_lock:
                df_restored_query.to_sql('corrects', con=data_sql_list.engine, if_exists='append', index=False)
        
        except Exception as error:
            inf(f"ошибка записи из базы corrects {error}")
            return "Курва чё-то ты намутил с базой данных при записи данных"
        
        # region corrects actual_after
        query_try = f'SELECT * FROM actual_after'
        with db_lock:
            rozklad_curs = pd.read_sql_query(query_try, con=data_sql_list.engine)

        df_restored_query['new_time'] = pd.to_datetime(df_restored_query['new_time'])
        df_restored_query = df_restored_query[df_restored_query['new_time'].dt.date ==  datetime.today().date()]

        df_restored_query['id'] = df_restored_query['id'].astype(int)
        df_restored_query['m3'] = df_restored_query['m3'].astype(float).round(1)
        df_restored_query['k'] = df_restored_query['k'].astype(int)
        df_restored_query['budowa'] = df_restored_query['budowa'].astype(str)
        df_restored_query['res'] = df_restored_query['res'].astype(float)
        df_restored_query['wenz'] = df_restored_query['wenz'].astype(str)
        df_restored_query['mat'] = df_restored_query['mat'].astype(str)
        df_restored_query['p/d'] = df_restored_query['p/d'].astype(str)

        rozklad_curs['id'] = rozklad_curs['id'].astype(int)
        rozklad_curs['k'] = rozklad_curs['k'].astype(int)
        rozklad_curs['m3'] = rozklad_curs['m3'].astype(float).round(1)
        rozklad_curs['budowa'] = rozklad_curs['budowa'].astype(str)
        rozklad_curs['wenz'] = rozklad_curs['wenz'].astype(str)
        rozklad_curs['mat'] = rozklad_curs['mat'].astype(str)
        rozklad_curs['p/d'] = rozklad_curs['p/d'].astype(str)
        rozklad_curs['time'] = rozklad_curs['time'].apply(pd.to_datetime)

        merged_df = df_restored_query.merge(rozklad_curs[['m3', 'k', 'budowa', 'res', 'wenz', 'mat', 'p/d', 'time', 'id']],
                              on=['m3', 'k', 'budowa', 'res', 'wenz', 'mat', 'p/d'],
                              how='inner',
                              suffixes=('', '_from_rosklad'))
        
        merged_df.drop_duplicates(subset=['m3', 'k', 'budowa', 'res', 'wenz', 'mat', 'p/d'], keep='last', inplace=True)

        merged_df.reset_index(drop=True, inplace=True)    

        df_restored_query.reset_index(drop=True, inplace=True)
        df_restored_query.update(merged_df[['time_from_rosklad']].rename(columns={'time_from_rosklad': 'time'}))
        df_restored_query['id'] = merged_df['id_from_rosklad']

        df_restored_query[["time", "new_time"]] = df_restored_query[["time", "new_time"]].apply(pd.to_datetime)


        if not df_restored_query.empty:
            df_restored_query['delta'] = df_restored_query['new_time'] - df_restored_query['time']
            df_restored_query['delete'] = df_restored_query['new_time'].dt.time == pd.to_datetime('00:00:00').time()

        rozklad_curs["delete"] = False

        for _, row in df_restored_query.iterrows():
            rozklad_curs.loc[(rozklad_curs['id'] == row['id'])&(rozklad_curs['budowa'] == row['budowa']), 'time'] += row['delta']
            rozklad_curs.loc[(rozklad_curs['id'] == row['id'])&(rozklad_curs['budowa'] == row['budowa']), 'delete'] = row['delete']

        rozklad_curs = rozklad_curs[rozklad_curs['delete'] == False].reset_index(drop=True)
        rozklad_curs.drop(columns='delete', inplace=True)

        rozklad_curs.sort_values("time", inplace=True) # type: ignore
      
        with db_lock:
            rozklad_curs.to_sql(
                'actual_after', con=data_sql_list.engine, if_exists='replace', index=False)
        # endregion


        formatted_time_new = new_time.strftime("%H:%M")
        formatted_time_old = str(df_restored_query.loc[0,"time"])


        return  f"{name_user}\nИзмeнил {df_restored_query.loc[0,'budowa']}\nкурс№ - {df_restored_query.loc[0,'k']},\n"\
                f"Метров - {df_restored_query.loc[0,'m3']},\nВензель№ - {df_restored_query.loc[0,'wenz']},\n"\
                f"Остаток - {df_restored_query.loc[0,'res']},\nбыло время отгрузки - {formatted_time_old[10:16]}\nстало - {formatted_time_new}"



if __name__ == '__main__':

    query_try = f'SELECT * FROM actual_after '
    with db_lock:
        df_try = pd.read_sql_query(query_try, con=data_sql_list.engine)

