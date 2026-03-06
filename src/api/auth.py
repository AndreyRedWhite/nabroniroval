"""
Endpoints for authentification and authorization.
"""

from fastapi import APIRouter, HTTPException, Response, Request

from src.api.dependencies import UserIdDep
from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserRequestAddSchema, UserAddSchema, UserLoginSchema
from src.services.auth import AuthService


router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])


@router.post('/register')
async def register_user(data: UserRequestAddSchema):
    hashed_password = AuthService().hash_password(data.password)
    user_dict = data.model_dump(exclude={"password"})
    user_dict['hashed_password'] = hashed_password
    new_user_data = UserAddSchema(**user_dict)
    async with async_session_maker() as session:
        user_exist = await UsersRepository(session).get_all(str(data.email))
        if user_exist:
            return {'status': 'User already exists'}
        await UsersRepository(session).add(new_user_data)
        await session.commit()
        return {'status': 'OK'}


@router.post('/login')
async def login_user(data: UserLoginSchema, response: Response):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(email=data.email)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        password = AuthService().verify_password(data.password, user.hashed_password)
        if not password:
            raise HTTPException(status_code=401, detail="Incorrect password")
        access_token = AuthService().create_access_token(data={"user id": user.id})
        response.set_cookie(key="access_token", value=access_token)
        return {"access_token": access_token, "token_type": "bearer"}


@router.get('/me')
async def get_me(user_id: UserIdDep):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(id=user_id)
        return user


@router.post('/logout')
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"status": "OK"}









