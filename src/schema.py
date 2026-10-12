from pydantic import BaseModel

class UserSchema(BaseModel):
    name: str
    email: str
    password:str

class UserResponseSchema(BaseModel):
    name: str
    email: str
    id:int


class LoginSchema(BaseModel):
    email: str
    password:str