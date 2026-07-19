"""
Task 2.1 — Veritabanı bağlantısını ve session yönetimini sağlayan katman.

DoD: "backend/app/db/database.py dosyası yazılmış olmalı."
"""

import os
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.db.models import Base

# backend/app/db/departments.db — Task 2.1'de belirtilen sabit konum
DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DB_DIR, "departments.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    """Tabloları (yoksa) oluşturur. Idempotent — var olan tabloyu bozmaz."""
    Base.metadata.create_all(bind=engine)


@contextmanager
def get_session() -> Session:
    """`with get_session() as session:` şeklinde kullanılacak session context manager'ı."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
