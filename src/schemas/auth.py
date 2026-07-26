from pydantic import BaseModel, ConfigDict, EmailStr

class UserAdd(BaseModel):
    email: EmailStr
    password: str

class UserRequestAdd(BaseModel):
    email: EmailStr
    password: str

class User (BaseModel):
    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)

class UserWithHashedPassword(User):
    password: str

class UserWith (BaseModel):
    id: int
    email: EmailStr


