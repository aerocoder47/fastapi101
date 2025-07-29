from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from random import randint  
import psycopg2 
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy import select
from . import models, schemas, utils
from . database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from app.routers import post, user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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



app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
async def root():
    return {"message": "Welcome to my api!!"}


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return {"status":"success"}
