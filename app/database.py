import time
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from psycopg2.extras import RealDictCursor
from app.config import settings



# SQLALCHEMY_DATABASE_URL= 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL= f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def conntect_to_db():
    while True:
        try:
            conn = psycopg2.connect(
                host='127.0.0.1', database='fastapi',  user='postgres', password='4747', cursor_factory=RealDictCursor
            )

            cursor = conn.cursor()
            print("Database connection was successful")
            break

        except Exception as e:
            print("Connecting to database failed")
            print("Error", e)
            time.sleep(2)