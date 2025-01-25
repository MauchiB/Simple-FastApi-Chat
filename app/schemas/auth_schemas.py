from pydantic import BaseModel, Field, EmailStr, ConfigDict


class Reg(BaseModel):
    username: str = Field(examples=['oleg'], max_length=20, min_length=4)
    hash_password: str = Field(min_length=5, examples=['12345'])
    email: EmailStr

class Login(BaseModel):
    username: str
    password: str



class UserOut(BaseModel):
    id: int
    username: str
    email: str


class Token(BaseModel):
    access_token: str
    token_type: str = Field(default='Bearer')

