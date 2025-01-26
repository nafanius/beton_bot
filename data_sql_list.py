from datetime import time as time_from_datatime
import json
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from setting import Settings

# Создание базового класса
Base = declarative_base()


# Определение структуры таблицы через класс


class Beton(Base):
    __tablename__ = "beton"

    id_event_time = Column(Float, primary_key=True)
    date_text = Column(String)
    list_data = Column(String)
    day = Column(Integer)
    status = Column(Integer)

    def __repr__(self):
        return f"<User(user_id={self.id_event_time}, name ={self.list_data})>"


class Lista(Base):
    __tablename__ = "lista"

    id_event_time = Column(Float, primary_key=True)
    date_text = Column(String)
    list_data = Column(String)
    day = Column(Integer)
    status = Column(Integer)

    def __repr__(self):
        return f"<User(user_id={self.id_event_time}, name ={self.list_data})>"


# Создание базы данных SQLite в файле
engine = create_engine(Settings.data_base_lista)

# Создание всех таблиц, которые еще не существуют
Base.metadata.create_all(engine)

# Создание сессии для взаимодействия с базой данных
Session = sessionmaker(bind=engine)


def delete_records_below_threshold(threshold, base):
    """"Deletes all records from [base name] with id_event_time less than [threshold]

    Args:
        threshold (float): Time as a float from the beginning of the epoch
        base_name (str): base name
    """    
    base_name = Beton
    if base == "beton":
        base_name = Beton
    elif base == "lista":
        base_name = Lista

    session = Session()

    try:
        # Отберите записи с большим или меньшим значением первичного ключа
        records_to_delete = session.query(base_name).filter(base_name.id_event_time < threshold).order_by(base_name.id_event_time).all()

        # Удалите выбранные записи
        for record in records_to_delete:
            session.delete(record)
        
        # Подтвердите изменения
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")
    finally:
        session.close()


def get_oldest_list_beton_or_lista(base, date_of_lista):
    base_name = Beton
    if base == "beton":
        base_name = Beton
    elif base == "lista":
        base_name = Lista

    session = Session()

    try:
        result = session.query(base_name.list_data).filter(base_name.date_text == date_of_lista).order_by(base_name.id_event_time.asc()).first()
        
        if result:
            if base == "beton":
                deserialized_list = json.loads(result[0])
                result_list = [(item[0], time_from_datatime.fromisoformat(item[1]), *item[2:]) for item in deserialized_list]
                return result_list
            
            elif base == "lista":
                pass
           
        return []
    
    finally:
        session.close()
    


def get_newest_list_beton_or_lista(base, date_of_lista, step):
    base_name = Beton
    if base == "beton":
        base_name = Beton
    elif base == "lista":
        base_name = Lista

    session = Session()

    try:
        if step:
            result = session.query(base_name.list_data, base_name.id_event_time, base_name.status).filter(base_name.date_text == date_of_lista).order_by(base_name.id_event_time.desc()).offset(1).first()
        else:
            result = session.query(base_name.list_data, base_name.id_event_time, base_name.status).filter(base_name.date_text == date_of_lista).order_by(base_name.id_event_time.desc()).first()
        
        if result:
            if base == "beton":
                deserialized_list = json.loads(result[0])
                result_list = [[(item[0], time_from_datatime.fromisoformat(item[1]), *item[2:]) for item in deserialized_list], result[1], result[2]]
                return result_list
            
            elif base == "lista":
                deserialized_list = json.loads(result[0])
                result_list = [[(time_from_datatime.fromisoformat(item[0]), item[1]) for item in deserialized_list], result[1], result[2]]
                return result_list

        return [[], None, 1]
    
    finally:
        session.close()


def update_status(base, id_event_time):
    base_name = Beton
    if base == "beton":
        base_name = Beton
    elif base == "lista":
        base_name = Lista

    session = Session()
    
    try:
        record = session.query(base_name).get(id_event_time)
        
        # Проверяем, существует ли запись
        if record is not None:
            # Обновляем указанное поле
            record.status = 1
            
            # Фиксируем изменения в базе данных
            session.commit()
    except IntegrityError as e:
        print("Ошибка целостности данных: возможно, дубликат ключа")
        session.rollback()  # Отмена всех изменений в текущей транзакции

    except Exception as e:
        print("Ошибка при добавлении данных:", e)
        session.rollback()
    finally:
        session.close()
        
