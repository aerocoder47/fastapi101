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
    prefix="/posts"
)


@router.get("/", response_model=List[schemas.Post])
def get_post(db: Session = Depends(get_db)):
    # table_name = "posts"
    #1
    # query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(table_name))
    # cursor.execute(query)
    # rows = cursor.fetchall()
    # result = [dict(row) for row in rows]
    # return {"data": result}
    #2
    # stmt = select(models.Post)
    # posts = db.execute(stmt).scalars().all()
    # return posts
    posts = db.query(models.Post).all()
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # print(new_post.model_dump()) 
    # data = post.model_dump()
    # query = sql.SQL("INSERT INTO {table} ({fields}) VALUES ({placeholders}) RETURNING *").format(
    #     table=sql.Identifier("posts"),
    #     fields=sql.SQL(", ").join(map(sql.Identifier, data.keys())),
    #     placeholders= sql.SQL(",").join(sql.Placeholder() * len(data))
    # )
    # cursor.execute(query, tuple(data.values()))
    # conn.commit()
    # inserted_post = cursor.fetchone()
    # # result = [dict(row) for row in inserted_post]

    # return {"new_post":  f"{dict(inserted_post)}"}
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/latest", response_model=schemas.Post)
def get_post( db: Session = Depends(get_db)):
    # table_name="posts"
    # query = sql.SQL("SELECT * FROM {table} ORDER BY {field} DESC LIMIT 1").format(
    #     table = sql.Identifier(table_name),
    #     field= sql.Identifier("created_at")
    # )
    # cursor.execute(query)
    # result =  cursor.fetchone()
    # print(result)
    # return {"data": f"{dict(result)}"}
    post = db.query(models.Post).order_by(models.Post.id.desc()).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No post found")
    return post


@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, response: Response, db: Session = Depends(get_db)): 
    # table_name = "posts"
    # query = sql.SQL("SELECT * FROM {table} WHERE {field}={value}").format(
    #     table = sql.Identifier(table_name),
    #     field = sql.Identifier("id"),
    #     value = sql.Placeholder()
    # )
    # cursor.execute(query, (id,))
    # result = cursor.fetchone()
    # if not result:
    #     # response.status_code = status.HTTP_404_NOT_FOUND
    #     # return {"message": f"post with id: {id} was not found"}
    #     raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
    #                         detail=f"post with id: {id} was not found")
    # return {"post_details": f"Here is the post {dict(result)}"}
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Post not found")
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # delete post
    # find the index of the post
    #delete the post my_post.pop(index)
    # query = sql.SQL("DELETE FROM {table} WHERE {field} = {value};").format(
    #     table=sql.Identifier("posts"),
    #     field=sql.Identifier("id"),
    #     value=sql.Placeholder()
    # )
    # cursor.execute(query, (id,))
    # conn.commit()
    # print("Deleted rows:", cursor.rowcount)

    # if cursor.rowcount == 0:
    #     #return {"message": f"post doesn't exist"}
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                     detail=f"Post with id: {id} does not exist")
   
    # return Response(status_code=status.HTTP_204_NO_CONTENT)
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post not found")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
        
    


@router.put("/{id}")
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), response_model=schemas.Post):
    # data = post.model_dump()
    # set_clause = sql.SQL(",").join(
    #     sql.SQL("{} = {}").format(
    #         sql.Identifier(k), sql.Placeholder()
    #     ) for k in data.keys()
    # )

    # query = sql.SQL("UPDATE {table} SET {set_clause}  WHERE {id_field}={value} RETURNING *").format(
    #     table=sql.Identifier("posts"),
    #     set_clause= set_clause,
    #     id_field=sql.Identifier("id"),
    #     value=sql.Placeholder()
    # )
    # values = list(data.values()) + [id]
    # cursor.execute(query, values)
    # conn.commit()
    # result = cursor.fetchone()
    # if not result :
    #     return HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
    #                      detail=f"Post with id: {id} not found")
       
    # return {"data": f"{dict(result)}"}
    existing_post = db.query(models.Post).filter(models.Post.id == id)
    if not existing_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    existing_post.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return existing_post.first()
