from typing import Annotated

from fastapi import Depends, Query
from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(default=1, description='Цифра страницы', ge=1)]
    per_page: Annotated[int | None, Query(default=3, description='Количество отображаемых отелей', ge=1, le=30)]


PaginationDep = Annotated[PaginationParams, Depends()]
