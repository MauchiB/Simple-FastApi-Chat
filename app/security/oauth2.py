from fastapi.security import OAuth2PasswordBearer
from fastapi import Request, HTTPException
from passlib.context import CryptContext

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='/auth/login'
)

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_token(request: Request):
    token = request.cookies.get('token')
    if token:
        return token
    raise HTTPException(status_code=401, detail='User not have auth token')




