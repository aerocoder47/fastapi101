from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randint  
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

# title str, content str
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None  

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
    cursor.execute("SELECT * FROM posts")
    rows = cursor.fetchall()
    result = [dict(row) for row in rows]
    return {"data": result}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    # print(new_post.model_dump()) 
    new_post = post.model_dump()
    new_post["id"] = randint(0,100000)
    my_posts.append(new_post)
    return {"new_post":  f"{new_post}"}

@app.get("/posts/latest")
def get_post():
    post = my_posts[len(my_posts) - 1]
    return {"post_details": f"Here is the post {post}"}

@app.get("/posts/{id}")
def get_post(id: int, response: Response): 
    post = find_post(int(id))
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found"}
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return {"post_details": f"Here is the post {post}"}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # delete post
    # find the index of the post
    #delete the post my_post.pop(index)
    index = find_index_post(id)
    if index == -1:
            #return {"message": f"post doesn't exist"}
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                         detail=f"Post with id: {id} does not exist")
    my_posts.pop(index)
    # return {"message": "post was successfully deleted"}
    return Response(status_code=status.HTTP_204_NO_CONTENT)
        
    


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index == -1:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                         detail=f"Post with id: {id} not found")
    
    post_dict = post.model_dump()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": post_dict}
    

    