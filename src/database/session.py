from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine, Engine

import os
from functools import lru_cache

@lru_cache(maxsize=None)
def get_engine(url: str):
    return create_engine(url, echo=False, pool_size=5, max_overflow=10)

def get_connection(url: str = None) -> Engine:
    if url:
        return create_engine(url, echo=True)

    load_dotenv()
    user = os.getenv("DATABASE_USER")
    password = os.getenv("DATABASE_PASSWORD")
    host = os.getenv("DATABASE_HOST")
    port = os.getenv("DATABASE_PORT")
    database = os.getenv("DATABASE_NAME")
    sslmode = os.getenv("DATABASE_SSLMODE", "require")

    assert all([user, password, host, port, database]), "One of the parameters is absent"
    url = f"postgresql://{user}:{password}@{host}:{port}/{database}?sslmode={sslmode}"

    return get_engine(url)

@lru_cache(maxsize=None)
def get_session_maker(url: str = None):
    engine = get_connection(url)
    return sessionmaker(bind=engine)

def get_session(url: str = None) -> Session:
    """Returns a new session from the existing engine pool"""
    SessionLocal = get_session_maker(url)
    return SessionLocal()