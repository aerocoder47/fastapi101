from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from random import randint  
import psycopg2 
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy import select
from app import models, schemas, utils
from app.database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session


router = APIRouter(
   prefix="/users",
   tags=['Users']
)

 # Users   


@router.get("/", status_code=status.HTTP_200_OK, response_model= List[schemas.UserGet])
def get_users( db: Session = Depends(get_db)):
    
    users = db.query(models.User).all()

    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wrong email or password"
        ) 
    
    return users

@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return user
    

@router.post("/create", status_code=status.HTTP_201_CREATED, response_model= schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    #hash the password - user.password
    email = user.email.lower()
   
    user_exists = db.query(models.User).filter(models.User.email == email).first()

    if user_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already taken")

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
 
    return new_user

@router.post("/login", status_code=status.HTTP_200_OK, response_model= schemas.UserOut)
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    auth_user =  db.query(models.User).filter(models.User.email == user.email).first()

    if(auth_user and auth_user.password == user.password):
        return auth_user
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Wrong email or password"
    )

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    email = user.email.lower()
    user_exists = db.query(models.User).filter(models.User.email == email)

    if(user_exists.first() and  user_exists.first().password == user.password):
        user_exists.delete()
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wrong email or password")
    
    
@router.put("/", status_code=status.HTTP_202_ACCEPTED, response_model= schemas.UserOut)
def update_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    email = user.email.lower()
    user_exists = db.query(models.User).filter(models.User.email == email)

    if not user_exists.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wrong email or password")
    
    if user_exists.first().password == user.password:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Old password used, please provide new password")

    
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    # new_user = models.User(**user.model_dump())

    user_exists.update(user.model_dump(), synchronize_session=False)
    db.commit()
 
    return user_exists.first()
