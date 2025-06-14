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
from src.setting import Settings, inf

# Creating a base class
Base = declarative_base()


class Beton_zawod(Base):
    __tablename__ = "beton_zawod"

    id_event_time = Column(Float, primary_key=True)
    date_text = Column(String)
    list_data = Column(String)
    day = Column(Integer)
    status = Column(Integer)

    def __repr__(self):
        return f"<User(user_id={self.id_event_time}, name ={self.list_data})>"


class Lista_zawod(Base):
    __tablename__ = "lista_zawod"

    id_event_time = Column(Float, primary_key=True)
    date_text = Column(String)
    list_data = Column(String)
    day = Column(Integer)
    status = Column(Integer)

    def __repr__(self):
        return f"<User(user_id={self.id_event_time}, name ={self.list_data})>"


# Creating an SQLite database in a file
engine = create_engine(Settings.data_base_lista)

# Creating all tables that do not exist yet
Base.metadata.create_all(engine)

# Создание сессии для взаимодействия с базой данных
Session = sessionmaker(bind=engine)


def delete_records_below_threshold(threshold, base):
    """"Deletes all records from [base name] with id_event_time less than [threshold]

    Args:
        threshold (float): Time as a float from the beginning of the epoch
        base_name (str): base name
    """
    base_name = Beton_zawod
    if base == "beton":
        base_name = Beton_zawod
    elif base == "lista":
        base_name = Lista_zawod

    session = Session()

    try:
        # Select records with a  lesser primary key value
        records_to_delete = session.query(base_name).filter(
            base_name.id_event_time < threshold).order_by(base_name.id_event_time).all()

        # Delete the selected records
        for record in records_to_delete:
            session.delete(record)

        # Confirm the changes
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")
    finally:
        session.close()


def get_oldest_list_beton_or_lista(base, date_of_lista):
    """Get the oldest list from Beton_zawod or Lista_zawod for a given date.

    Args:
        base (str): "beton" or "lista" to specify the table to query.
        date_of_lista (str): The date for which to retrieve the list, formatted as "dd.mm.yyyy".

    Returns:
        list: A list of tuples containing the data from the oldest list for the specified date.
    """
    base_name = Beton_zawod
    if base == "beton":
        base_name = Beton_zawod
    elif base == "lista":
        base_name = Lista_zawod

    session = Session()

    try:
        result = session.query(base_name.list_data).filter(
            base_name.date_text == date_of_lista).order_by(base_name.id_event_time.asc()).first()

        if result:
            if base == "beton":
                deserialized_list = json.loads(result[0])
                result_list = [(item[0], time_from_datatime.fromisoformat(
                    item[1]), *item[2:]) for item in deserialized_list]
                return result_list

            elif base == "lista":
                pass

        return []

    finally:
        session.close()


def get_newest_list_beton_or_lista(base, date_of_lista, step):
    """Get the newest list from Beton_zawod or Lista_zawod for a given date.

    Args:
        base (str): "beton" or "lista" to specify the table to query.
        date_of_lista (str): The date for which to retrieve the list, formatted as "dd.mm.yyyy".
        step (int): If 1, returns the second newest list; if 0, returns the newest list.

    Returns:
        list: A list containing the data from the newest list for the specified date,
    """
    base_name = Beton_zawod
    if base == "beton":
        base_name = Beton_zawod
    elif base == "lista":
        base_name = Lista_zawod

    session = Session()

    try:
        if step:
            result = session.query(base_name.list_data, base_name.id_event_time, base_name.status).filter(
                base_name.date_text == date_of_lista).order_by(base_name.id_event_time.desc()).offset(1).first()
        else:
            result = session.query(base_name.list_data, base_name.id_event_time, base_name.status).filter(
                base_name.date_text == date_of_lista).order_by(base_name.id_event_time.desc()).first()

        if result:
            if base == "beton":
                deserialized_list = json.loads(result[0])
                # list of [[list of tuple data], id_event_time, status]
                result_list = [[(item[0], time_from_datatime.fromisoformat(
                    item[1]), *item[2:]) for item in deserialized_list], result[1], result[2]]
                return result_list

            elif base == "lista":
                deserialized_list = json.loads(result[0])
                # list of [[list of tuple data], id_event_time, status]
                result_list = [[(time_from_datatime.fromisoformat(item[0]), item[1])
                                for item in deserialized_list], result[1], result[2]]
                return result_list

        return [[], None, 1]

    finally:
        session.close()


def update_status(base, id_event_time):
    """Update the status of a record in Beton_zawod or Lista_zawod.
    This function sets the status of a record with the given id_event_time to 1.
    This is typically used to mark a record as processed or completed.

    Args:
        base (str): "beton" or "lista" to specify the table to update.
        id_event_time (int): The id_event_time of the record to update.
    """
    base_name = Beton_zawod
    if base == "beton":
        base_name = Beton_zawod
    elif base == "lista":
        base_name = Lista_zawod

    session = Session()

    try:
        record = session.query(base_name).get(id_event_time)

        # Checking if the record exists
        if record is not None:
            #  Updating the specified field
            record.status = 1

            # Committing changes to the database
            session.commit()
    except IntegrityError as e:
        inf("Data integrity error: possible duplicate key")
        session.rollback()  # Rolling back all changes in the current transaction

    except Exception as e:
        inf("Error adding data:", e)
        session.rollback()
    finally:
        session.close()
