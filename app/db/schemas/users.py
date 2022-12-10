from pydantic import BaseModel
import typing as t

from ..models.users import UserTypes


class UserBase(BaseModel):
    email: str
    is_active: bool = True
    is_superuser: bool = False
    first_name: str = None
    last_name: str = None
    instagram: str = None
    phone_number: str
    type: UserTypes = UserTypes.player


class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserShortInfoOut(BaseModel):
    email: str
    phone_number: str = None
    first_name: str
    last_name: str

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str

    class Config:
        orm_mode = True


class UserEdit(UserBase):
    password: t.Optional[str] = None

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str = None
    permissions: str = "player"
