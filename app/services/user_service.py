from sqlalchemy.orm import Session
from ..models.users import User as UserModel
from ..models.roles import Role as RoleModel
from fastapi import HTTPException, status
from ..utils import get_password_hash
from ..utils import verify
from ..oauth2 import create_access_token

def create_user(db: Session, user_data: dict) -> UserModel:
    # Validar si existe usuario
    existing_user = db.query(UserModel).filter(UserModel.email == user_data['email']).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )
    
    # Buscar rol por defecto
    role_user = db.query(RoleModel).filter(RoleModel.name == "ROLE_USER").first()
    if not role_user:
        raise HTTPException(status_code=500, detail="Default role ROLE_USER not found")

    # Hashear contraseña
    password_hash = get_password_hash(user_data.pop('password_hash'))

    # Crear usuario
    new_user = UserModel(
        **user_data,
        password_hash=password_hash,
        roles=[role_user]
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def authenticate_user(db: Session, username: str, password: str) -> str:
    user = db.query(UserModel).filter(UserModel.email == username).first()
    if not user or not verify(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )

    roles = [role.name for role in user.roles]
    return create_access_token(data={"user_id": user.id, "roles": roles})