import pytest
from unittest.mock import patch, MagicMock
from db_driver import data_sql_bot
from sqlalchemy.exc import IntegrityError

@pytest.fixture(autouse=True)
def mock_session(monkeypatch):
    # Patch Session to return a mock session
    mock_session = MagicMock()
    monkeypatch.setattr(data_sql_bot, "Session", MagicMock(return_value=mock_session))
    yield mock_session

def test_add_all_acive_chat_id_returns_active_chat_ids(mock_session):
    # Arrange
    mock_record1 = MagicMock(chat_id="123")
    mock_record2 = MagicMock(chat_id="456")
    mock_session.query.return_value.filter_by.return_value.all.return_value = [mock_record1, mock_record2]

    # Act
    result = data_sql_bot.add_all_acive_chat_id()

    # Assert
    assert result == ["123", "456"]
    mock_session.close.assert_called_once()

def test_add_all_acive_chat_id_returns_empty_list_when_no_active_chats(mock_session):
    # Arrange
    mock_session.query.return_value.filter_by.return_value.all.return_value = []

    # Act
    result = data_sql_bot.add_all_acive_chat_id()

    # Assert
    assert result == []
    mock_session.close.assert_called_once()

def test_add_all_acive_chat_id_handles_integrity_error(mock_session):
    # Arrange
    mock_session.query.return_value.filter_by.return_value.all.side_effect = IntegrityError("msg", "params", Exception("orig"))
    with patch.object(data_sql_bot, "inf") as mock_inf:
        # Act
        result = data_sql_bot.add_all_acive_chat_id()
        # Assert
        mock_inf.assert_called_with("Data integrity error: possible duplicate key")
        mock_session.rollback.assert_called_once()
        mock_session.close.assert_called_once()
        assert result is None

def test_add_all_acive_chat_id_handles_general_exception(mock_session):
    # Arrange
    mock_session.query.return_value.filter_by.return_value.all.side_effect = Exception("Some error")
    with patch.object(data_sql_bot, "inf") as mock_inf:
        # Act
        result = data_sql_bot.add_all_acive_chat_id()
        # Assert
        mock_inf.assert_called()
        mock_session.rollback.assert_called_once()
        mock_session.close.assert_called_once()
        assert result is None