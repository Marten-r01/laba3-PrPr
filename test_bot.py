import pytest
from unittest.mock import MagicMock
from handler import register_handlers

@pytest.fixture
def mock_bot():
    class DummyMessage:
        def __init__(self, text):
            self.text = text
            self.chat = type("chat", (), {"id": 42})

    bot = MagicMock()
    replies = []
    bot.reply_to.side_effect = lambda msg, text: replies.append(text)
    bot.message_handler = lambda commands: lambda func: func
    return bot, DummyMessage, replies

def test_start(mock_bot):
    bot, DummyMessage, replies = mock_bot
    register_handlers(bot)
    msg = DummyMessage("/start")
    bot.message_handler(commands=["start"])(lambda m: None)(msg)
    assert any("привет" in r.lower() for r in replies)

def test_track_missing_url(mock_bot):
    bot, DummyMessage, replies = mock_bot
    register_handlers(bot)
    msg = DummyMessage("/track")
    bot.message_handler(commands=["track"])(lambda m: None)(msg)
    assert any("ошибка" in r.lower() or "формат" in r.lower() for r in replies)

def test_list_empty(mock_bot):
    bot, DummyMessage, replies = mock_bot
    register_handlers(bot)
    msg = DummyMessage("/list")
    bot.message_handler(commands=["list"])(lambda m: None)(msg)
    assert any("нет" in r.lower() or "пуст" in r.lower() for r in replies)

def test_search_no_term(mock_bot):
    bot, DummyMessage, replies = mock_bot
    register_handlers(bot)
    msg = DummyMessage("/search")
    bot.message_handler(commands=["search"])(lambda m: None)(msg)
    assert any("введите" in r.lower() for r in replies)