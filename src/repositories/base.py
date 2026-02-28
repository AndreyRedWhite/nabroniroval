from sqlalchemy import select, insert, update, delete
from pydantic import BaseModel

class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):

        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, filter_by):

        query = select(self.model)
        result = await self.session.execute(query).filter(**filter_by)
        return result.scalars().one_or_none()

    async def add(self, data: BaseModel):

        stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def edit(self, data: BaseModel, filter_by, exclude_unset: bool = False) -> None:
        stmt = (
            update(self.model)
            .values(**data.model_dump(exclude_unset=exclude_unset))
            .filter(**filter_by)
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def delete(self, **filter_by) -> None:
        stmt = delete(self.model)
        deleted_hotel = await self.session.execute(stmt).filter(**filter_by).returning(self.model)
        return deleted_hotel.scalar_one()


