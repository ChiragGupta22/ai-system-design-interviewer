from pydantic import BaseModel

class UserSchema(BaseModel):
    name: str
    email: str
    password:str
    role: str = "user"

class UserResponseSchema(BaseModel):
    name: str
    email: str
    id:int
    role: str
    
   


class LoginSchema(BaseModel):
    email: str
    password:str