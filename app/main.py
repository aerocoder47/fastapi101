from fastapi import FastAPI, Depends
from app import models
from app.database import engine, get_db
from sqlalchemy.orm import Session
from app.routers import post, user, auth, vote
from app.config import settings

from fastapi.middleware.cors import CORSMiddleware

# alchmey db filler
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
async def root():
    return {"message": "Welcome to my api!!"}


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return {"status":"success"}
