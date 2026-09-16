from aiogram import Dispatcher

from app.config import Settings
from app.main import build_dispatcher, help_text, home_text
from app.storage import Storage


def test_home_and_help_content():
    home = home_text()
    help_message = help_text()
    assert "3 functions" in home
    assert "Promotions" in home
    assert "Updates" in home
    assert "Submit Promotion" in home
    assert "Promotions" in help_message
    assert "Updates" in help_message
    assert "Submit Promotion" in help_message


def test_storage_initializes_and_saves_submission(tmp_path):
    database = tmp_path / "test.db"
    storage = Storage(str(database))
    submission_id = storage.add_submission(12345, "tester", "Test promotion")
    assert submission_id == 1
    assert database.exists()


def test_dispatcher_builds(tmp_path):
    storage = Storage(str(tmp_path / "test.db"))
    settings = Settings("token", None, str(tmp_path / "test.db"))
    dispatcher = build_dispatcher(storage, settings)
    assert isinstance(dispatcher, Dispatcher)
