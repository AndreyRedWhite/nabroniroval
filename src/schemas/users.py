from pydantic import BaseModel, EmailStr


class UserRequestAddSchema(BaseModel):
    email: EmailStr
    password: str
    first_name: str | None = None
    last_name: str | None = None
    age: int | None = None
    gender: str | None = None


class UserAddSchema(BaseModel):
    email: EmailStr
    hashed_password: str
    first_name: str | None = None
    last_name: str | None = None
    age: int | None = None
    gender: str | None = None


class UserSchema(BaseModel):
    id: int
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None
    age: int | None = None
    gender: str | None = None
