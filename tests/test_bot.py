from aiogram import Dispatcher

from app.config import Settings
from app.content import PROMOTIONS, UPDATES
from app.main import _safe_index, build_dispatcher, help_text, home_text
from app.storage import Storage


def test_home_and_help_describe_exactly_three_functions():
    home = home_text()
    help_message = help_text()
    assert "3 functions" in home
    assert "Promotions" in home
    assert "Updates" in home
    assert "Submit Promotion" in home
    assert "exactly three user functions" in help_message


def test_content_is_present():
    assert PROMOTIONS and UPDATES
    assert all(item.title and item.body for item in (*PROMOTIONS, *UPDATES))


def test_callback_index_validation():
    assert _safe_index("promotion:0", "promotion", 3) == 0
    assert _safe_index("promotion:2", "promotion", 3) == 2
    assert _safe_index("promotion:3", "promotion", 3) is None
    assert _safe_index("promotion:-1", "promotion", 3) is None
    assert _safe_index("promotion:x", "promotion", 3) is None
    assert _safe_index("update:0", "promotion", 3) is None


def test_storage_initializes_and_saves_submission(tmp_path):
    database = tmp_path / "test.db"
    storage = Storage(str(database))
    submission_id = storage.add_submission(12345, "tester", "Test promotion")
    assert submission_id == 1
    assert database.exists()


def test_dispatcher_builds(tmp_path):
    database = tmp_path / "test.db"
    storage = Storage(str(database))
    settings = Settings("token", None, str(database))
    dispatcher = build_dispatcher(storage, settings)
    assert isinstance(dispatcher, Dispatcher)