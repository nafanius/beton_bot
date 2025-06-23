from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Boolean
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from src.setting import Settings, inf

# Creating a base class
Base = declarative_base()


# Defining the table structure through a class
class Chats(Base):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    block = Column(Boolean, default=False)


# Creating an SQLite database in a file
engine = create_engine(Settings.data_base_bot)

# Creating all tables that do not exist yet
Base.metadata.create_all(engine)

# Creating a session for interacting with the database
Session = sessionmaker(bind=engine)


def add_id_chat_or_turn_on(chat_id):

    base_name = Chats

    session = Session()

    try:
        record = session.query(base_name).filter_by(chat_id=chat_id).first()
        if record is None:
            # record does not exist, create a new one
            new_record = base_name(
                chat_id=chat_id, is_active=True, block=False)
            session.add(new_record)
            session.commit()
            return "save record is_active true"
        else:
            if record.is_active is False:
                setattr(record, "is_active", True)
                session.commit()
                return "record exist is_active turn true "
            else:
                return "record exist is_active true"

    except IntegrityError as e:
        inf("Data integrity error: possible duplicate key")
        session.rollback()  # Rolling back all changes in the current transaction

    except Exception as e:
        inf("Error adding data:", e)
        session.rollback()
    finally:
        session.close()


def add_id_chat_or_turn_off(chat_id):

    base_name = Chats

    session = Session()

    try:
        record = session.query(base_name).filter_by(chat_id=chat_id).first()
        if record is None:
            # record not found, adding a new one
            new_record = base_name(
                chat_id=chat_id, is_active=False, block=False)
            session.add(new_record)
            session.commit()
            return "save record is_active False"
        else:
            if record.is_active is True:
                setattr(record, "is_active", False)
                session.commit()
                return "record exist is_active turn false "
            else:
                return "record exist is_active false"

    except IntegrityError as e:
        inf("Data integrity error: possible duplicate key")
        session.rollback()  # Rolling back all changes in the current transaction

    except Exception as e:
        inf("Error adding data:", e)
        session.rollback()
    finally:
        session.close()


def add_all_acive_chat_id():

    base_name = Chats

    session = Session()

    try:
        # doing a query to get all active records
        records = session.query(base_name).filter_by(
            is_active=True, block=False).all()
        #   extracting chat_id from the records
        active_chat_id = [record.chat_id for record in records]
        return active_chat_id

    except IntegrityError as e:
        inf("Data integrity error: possible duplicate key")
        session.rollback()  # Rolling back all changes in the current transaction

    except Exception as e:
        inf("Error adding data:", e)
        session.rollback()
    finally:
        session.close()
