from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from .Settings import settings

from .schemas.token import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = f"{settings.secret_key}"
ALGORITHM = f"{settings.algorithm}"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

        user_id  = payload.get("user_id")
        roles = payload.get("roles", [])
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(id=str(user_id), roles=roles)

    except InvalidTokenError:
        raise credentials_exception
    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception= HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_access_token(token, credentials_exception)

def require_roles(required_roles: list[str]):
    def role_checker(token_data: TokenData = Depends(get_current_user)):
        if not any(role in token_data.roles for role in required_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action"
            )
        return token_data
    return role_checker