import os
import time
from sqlalchemy import create_engine, text

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)


def init_db(retries: int = 10, delay: int = 2):
    last_error = None

    for _ in range(retries):
        try:
            with engine.begin() as conn:
                conn.execute(text("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    city TEXT,
                    waste_type TEXT,
                    severity INT,
                    lat FLOAT,
                    lng FLOAT,
                    status TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """))
            return
        except Exception as exc:
            last_error = exc
            time.sleep(delay)

    raise last_error
