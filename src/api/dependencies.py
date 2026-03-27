from typing import Annotated

from fastapi import Depends, Query, HTTPException, Request
from pydantic import BaseModel

from src.database import async_session_maker
from src.services.auth import AuthService
from src.utils.db_manager import DBManager


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(default=1, description='Цифра страницы', ge=1)]
    per_page: Annotated[int | None, Query(default=3, description='Количество отображаемых отелей', ge=1, le=30)]


PaginationDep = Annotated[PaginationParams, Depends()]

def get_token(request: Request) -> str:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail='Token has not been set')
    return token


def get_current_user_id(token: str = Depends(get_token)) -> int | None:
    data = AuthService().decode_token(token=token)
    user_id = data.get('user id', None)
    return user_id


UserIdDep = Annotated[int, Depends(get_current_user_id)]


async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


DBdeb = Annotated[DBManager, Depends(get_db)]
