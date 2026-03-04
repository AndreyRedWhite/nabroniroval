from fastapi import APIRouter

from passlib.context import CryptContext

from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserRequestAddSchema, UserAddSchema

router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post('/register')
async def register_user(data: UserRequestAddSchema):
    hashed_password = pwd_context.hash(data.password)
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


