import importlib
import os
import sys
import types

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text


os.environ.setdefault("DATABASE_URL", "sqlite:///./tests/bootstrap.db")

fake_model_module = types.ModuleType("backend.models.efficientnet_model")


class FakeModel:
    def predict(self, img):
        return "construction-waste"


fake_model_module.Model = FakeModel
sys.modules["backend.models.efficientnet_model"] = fake_model_module

db_module = importlib.import_module("backend.db.db")
main_module = importlib.import_module("backend.main")


@pytest.fixture
def client(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    engine = create_engine(
        f"sqlite:///{db_path}",
        connect_args={"check_same_thread": False},
    )

    def init_test_db(retries=10, delay=2):
        with engine.begin() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    city TEXT,
                    waste_type TEXT,
                    severity INT,
                    lat FLOAT,
                    lng FLOAT,
                    status TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """))

    monkeypatch.setattr(db_module, "engine", engine)
    monkeypatch.setattr(main_module, "engine", engine)
    monkeypatch.setattr(main_module, "init_db", init_test_db)
    monkeypatch.setattr(main_module, "Model", FakeModel)

    with TestClient(main_module.app) as test_client:
        yield test_client, engine

    engine.dispose()
