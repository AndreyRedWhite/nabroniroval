from sqlalchemy import select, insert, update, delete
from pydantic import BaseModel


class BaseRepository:
    model = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):

        query = select(self.model)
        result = await self.session.execute(query)
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]


    async def get_one_or_none(self, **filter_by):

        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model =  result.scalars().one_or_none()
        if model is None:
            return None
        return self.schema.model_validate(model, from_attributes=True)

    async def add(self, data: BaseModel):

        stmt = (insert(self.model)
                .values(**data.model_dump())
                .returning(self.model))
        result = await self.session.execute(stmt)
        model = result.scalar_one()
        return self.schema.model_validate(model, from_attributes=True)

    async def edit(self, data: BaseModel, filter_by, exclude_unset: bool = False):
        stmt = (
            update(self.model)
            .values(**data.model_dump(exclude_unset=exclude_unset))
            .filter_by(**filter_by)
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one()
        return self.schema.model_validate(model, from_attributes=True)

    async def delete(self, **filter_by):
        stmt = delete(self.model).filter_by(**filter_by).returning(self.model)
        del_stmt = await self.session.execute(stmt)
        model = del_stmt.scalar_one()
        return self.schema.model_validate(model, from_attributes=True)


