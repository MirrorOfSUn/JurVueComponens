from fastapi import FastAPI
from sqlmodel import create_engine, Session
from config import DB_LOCATION

# Create the database
# Base.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


engine = create_engine(
    DB_LOCATION,
    connect_args={"check_same_thread": False},
    echo=True
)

api_app = FastAPI(title="api app", debug=True)

import app.UsersAPI
