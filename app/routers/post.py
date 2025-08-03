from typing import Optional, List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from app import models, schemas, oauth2
from app.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/", response_model=List[schemas.PostJoinVote])
def get_post(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
              limit: int = 3, skip: int = 0, search: Optional[str]=""):
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
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    result = db.query(models.Post, func.count(models.Vote.post_id).label("votes")
                      ).filter(models.Post.title.contains(search)).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True
                             ).group_by(models.Post.id
                                        ).order_by(models.Post.id.desc()).limit(limit).offset(skip).all()
     
    return result

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user),
                ):
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
   
    new_post = models.Post(owner_id=current_user.id,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/latest", response_model=schemas.Post)
def get_post( db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # table_name="posts"
    # query = sql.SQL("SELECT * FROM {table} ORDER BY {field} DESC LIMIT 1").format(
    #     table = sql.Identifier(table_name),
    #     field= sql.Identifier("created_at")
    # )
    # cursor.execute(query)
    # result =  cursor.fetchone()
    # print(result)
    # return {"data": f"{dict(result)}"}
    # print(current_user.email)

    post = db.query(models.Post).order_by(models.Post.id.desc()).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No post found")
    return post


@router.get("/{id}", response_model=schemas.PostJoinVote)
def get_post(id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): 
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
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).filter(models.Post.id == id
                                        ).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True
                                               ).group_by(models.Post.id)

    post = post.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Post not found")
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
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
    
    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
        
    


@router.put("/{id}")
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), response_model=schemas.Post, current_user: int = Depends(oauth2.get_current_user)):
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
    
    if existing_post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    existing_post.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return existing_post.first()
