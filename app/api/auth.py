from fastapi import APIRouter, Depends, HTTPException, Response, responses
from ..schemas.auth_schemas import Reg, UserOut, Token, Login
from ..services.auth_services import register_user
from sqlalchemy.orm import Session
from typing import Annotated, List
from ..models.user import User
from ..dependencies import get_db
from app.security.oauth2 import get_token
from app.services.auth_services import is_authenticated, create_access_token
from app.dependencies import get_current_user

auth_router = APIRouter(prefix='/auth', tags=['auth'])


@auth_router.post('/reg', summary='Register unique user', description='Accepts the pydantic model in the post request and registers if there is no such user.')
def regestration(data: Reg, db: Annotated[Session, Depends(get_db)]):
    user = register_user(data=data, db=db)
    if not user:
        raise HTTPException(status_code=409, detail={'error':'User is already exists'})
    return UserOut.model_validate(user, from_attributes=True)

@auth_router.post('/login', summary='Login user', description='If the data in the body is correct, a jwt token will be assigned in cookies.')
def login(form: Login, db: Annotated[Session, Depends(get_db)], response: Response):
    '''form is dict with attr: username and password'''
    user = is_authenticated(username=form.username, password=form.password, db=db)
    if user is not None:
        token = create_access_token(data={'username':user.username})
        '''token_type default Bearer'''
        response.set_cookie(key='token', value=token, max_age=60 * 30)
        return Token(access_token=token)
    raise HTTPException(status_code=404, detail='User is not defind', headers={'WWW-Authenticated':'Bearer'})
 

@auth_router.get('/users', summary='Return list users', description='Retrieves the list of all users. Not for production, just for testing purposes.')
def all_users(db: Annotated[Session, Depends(get_db)], token: Annotated[str, Depends(get_token)]) -> List[UserOut]:
    users = db.query(User).all()
    return [UserOut.model_validate(user, from_attributes=True) for user in users]

@auth_router.get('/me', summary='Return user', description='Returns the user by the cookie token, if available')
def me(user: Annotated[get_current_user, Depends(get_current_user)]) -> UserOut:
    return UserOut.model_validate(user, from_attributes=True)

@auth_router.get('/logout', summary='Logout user', description='Logs out of the account, deletes the token in cookies')
def logout(token: Annotated[str, Depends(get_token)], response: Response):
    response.delete_cookie('token')
    responses.RedirectResponse('/login')


