from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr
from pydantic.v1 import ConfigDict, conint, ConstrainedInt


# ####Extiende de BaseModel
# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    vote_dir: int

    @classmethod
    def __get_pydantic_json_schema__(cls, *, by_alias: bool = False):
        schema = super().__get_pydantic_json_schema__(by_alias=by_alias)
        schema['properties']['vote_dir']['maximum'] = 1
        schema['properties']['vote_dir']['minimum'] = -1
        schema['properties']['vote_dir']['type'] = ['integer', 'string']
        return schema
