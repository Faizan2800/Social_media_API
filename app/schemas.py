from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional

# Base schema for common fields
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    



# Used for incoming POST requests
class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime  # ✅ Fix is here

    class Config:
        from_attributes = True  # ✅ Replaces orm_mode


# Used for responses
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner : UserOut

    class Config:
        from_attributes = True  # ✅ Replaces orm_mode in Pydantic v2

class PostOut(BaseModel):
    Post: Post
    votes: int
    
    
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True




class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id : Optional[int] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)