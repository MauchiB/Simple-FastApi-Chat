from ..schemas.auth_schemas import Reg
from sqlalchemy.orm import Session
from ..models.user import User
from app.security.oauth2 import pwd_context
import jwt
from datetime import datetime, timedelta
from app.security.oauth2 import pwd_context
from app.config import ALGORITHM, SECRET_KEY

def register_user(data: Reg, db: Session) -> User:
    user = db.query(User).filter_by(username=data.username).first()
    if user:
        return False
    user = User(**data.model_dump())
    user.hash_password = pwd_context.hash(data.hash_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def create_access_token(data: dict, expire: timedelta | None = timedelta(minutes=30)):
    to_encode = data.copy()
    exp = datetime.now() + expire
    to_encode.update({'exp':exp})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


def is_authenticated(username: str, password: str, db: Session):
    user = db.query(User).filter_by(username=username).first()
    if user and pwd_context.verify(password, user.hash_password):
        return user
    return None

def get_user(username: str, db: Session):
    return db.query(User).filter_by(username=username).first()
    
    