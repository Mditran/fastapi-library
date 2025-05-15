from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from  ..database import get_db
from schemas.user import UserLogin
from models.users import User as UserModel
from ..utils import verify
from ..oauth2 import create_access_token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from schemas.token import Token

router = APIRouter(
    tags=['Authentication']
)

@router.post('/login', response_model=Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends() ,db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    if not verify(user_credentials.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    roles = [role.name for role in user.roles]

    access_token = create_access_token(data={"user_id": user.id, "roles": roles})
    #Create token
    return {"access_token": access_token, "token_type": "bearer"}


