from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randint  
import psycopg2 
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

# title str, content str
class Post(BaseModel):
    title: str
    content: str

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




my_posts = [
    {"title": "title of post 1",
             "content": "content of post 1",
             "id": 1},
    {"title": "title of post 2",
             "content": "content of post 2",
             "id": 2},
            ]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
    return None

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i
    return -1


@app.get("/")
async def root():
    return {"message": "Welcome to my api!!"}

@app.get("/posts")
def get_post():
    table_name = "posts"
    query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(table_name))
    cursor.execute(query)
    rows = cursor.fetchall()
    result = [dict(row) for row in rows]
    return {"data": result}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    # print(new_post.model_dump()) 
    data = post.model_dump()
    query = sql.SQL("INSERT INTO {table} ({fields}) VALUES ({placeholders}) RETURNING *").format(
        table=sql.Identifier("posts"),
        fields=sql.SQL(", ").join(map(sql.Identifier, data.keys())),
        placeholders= sql.SQL(",").join(sql.Placeholder() * len(data))
    )
    cursor.execute(query, tuple(data.values()))
    conn.commit()
    inserted_post = cursor.fetchone()
    # result = [dict(row) for row in inserted_post]

    return {"new_post":  f"{dict(inserted_post)}"}

@app.get("/posts/latest")
def get_post():
    table_name="posts"
    query = sql.SQL("SELECT * FROM {table} ORDER BY {field} DESC LIMIT 1").format(
        table = sql.Identifier(table_name),
        field= sql.Identifier("created_at")
    )
    cursor.execute(query)
    result =  cursor.fetchone()
    print(result)
    return {"data": f"{dict(result)}"}

@app.get("/posts/{id}")
def get_post(id: int, response: Response): 
    table_name = "posts"
    query = sql.SQL("SELECT * FROM {table} WHERE {field}={value}").format(
        table = sql.Identifier(table_name),
        field = sql.Identifier("id"),
        value = sql.Placeholder()
    )
    cursor.execute(query, (id,))
    result = cursor.fetchone()
    if not result:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found"}
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return {"post_details": f"Here is the post {dict(result)}"}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # delete post
    # find the index of the post
    #delete the post my_post.pop(index)
    query = sql.SQL("DELETE FROM {table} WHERE {field} = {value};").format(
        table=sql.Identifier("posts"),
        field=sql.Identifier("id"),
        value=sql.Placeholder()
    )
    cursor.execute(query, (id,))
    conn.commit()
    print("Deleted rows:", cursor.rowcount)

    if cursor.rowcount == 0:
        #return {"message": f"post doesn't exist"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Post with id: {id} does not exist")
   
    return Response(status_code=status.HTTP_204_NO_CONTENT)
        
    


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    data = post.model_dump()
    set_clause = sql.SQL(",").join(
        sql.SQL("{} = {}").format(
            sql.Identifier(k), sql.Placeholder()
        ) for k in data.keys()
    )

    query = sql.SQL("UPDATE {table} SET {set_clause}  WHERE {id_field}={value} RETURNING *").format(
        table=sql.Identifier("posts"),
        set_clause= set_clause,
        id_field=sql.Identifier("id"),
        value=sql.Placeholder()
    )
    values = list(data.values()) + [id]
    cursor.execute(query, values)
    conn.commit()
    result = cursor.fetchone()
    if not result :
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                         detail=f"Post with id: {id} not found")
       
    return {"data": f"{dict(result)}"}
    

    