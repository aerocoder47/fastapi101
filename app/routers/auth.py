from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import database, schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(user_cred: OAuth2PasswordRequestForm = Depends() , db: Session = Depends(database.get_db)):
    #{username:"" , password:""} : user_cred
    
    user = db.query(models.User).filter(models.User.email == user_cred.username.lower()).first()
  
    hash_user_pwd = utils.hash(user_cred.password)

    if (user) and (utils.verify(user_cred.password, user.password)):
       access_token = oauth2.create_access_token(data={"user_id": user.id })
       return {"access_token":access_token, "token_type":"bearer"}

    raise HTTPException(status_code=status.HTTP_403_NOT_FOUND, detail="Invalid Credentials")

 