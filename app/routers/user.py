from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..schemas.user import UserCreate, UserResponse
from ..database import get_db
from ..services.user_service import create_user
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..schemas.token import Token
from ..services.user_service import authenticate_user

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def api_create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_dict = user.model_dump(exclude_unset=True, exclude={"roles"})
    new_user = create_user(db, user_dict)
    return new_user

@router.post('/login', response_model=Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    access_token = authenticate_user(db, user_credentials.username, user_credentials.password)
    return {"access_token": access_token, "token_type": "bearer"}