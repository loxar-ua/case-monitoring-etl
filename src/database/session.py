from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine, Engine

import os

from sqlalchemy.orm import sessionmaker


def get_connection(url: str = None) -> Engine:
    """Connects to the PostgreSQL database and returns the engine"""
    if url:
        engine = create_engine(url, echo=True)

        return engine

    load_dotenv()
    user = os.getenv("DATABASE_USER")
    password = os.getenv("DATABASE_PASSWORD")
    host = os.getenv("DATABASE_HOST")
    port = os.getenv("DATABASE_PORT")
    database = os.getenv("DATABASE_NAME")

    assert all([user, password, host, port, database]), "One of the parameters is absent"

    url = f"postgresql://{user}:{password}@{host}:{port}/{database}"
    engine = create_engine(url, echo=False) # TODO: change echo to false in production
    return engine

def get_session(url: str = None) -> Session:
    """Creates a new database session per request"""
    engine = get_connection(url)
    Session = sessionmaker(bind=engine)

    return Session()



