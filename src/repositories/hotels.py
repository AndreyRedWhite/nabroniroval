from sqlalchemy import select, func, update, delete

from src.models.hotels import HotelOrm
from src.repositories.base import BaseRepository
from src.schemas.hotels import HotelSchema


class HotelsRepository(BaseRepository):
    model = HotelOrm

    async def get_all(self, title: str, location: str, limit: int, offset: int):
        get_hotels_query = select(self.model)
        if title:
            get_hotels_query = get_hotels_query.filter(func.lower(self.model.title).ilike(f'%{title.strip().lower()}%'))
        if location:
            get_hotels_query = get_hotels_query.filter(func.lower(self.model.location).ilike(f"%{location.strip().lower()}%"))
        get_hotels_query = (
            get_hotels_query
            .limit(limit)
            .offset(offset).
            order_by(HotelOrm.id)
        )
        result = await self.session.execute(get_hotels_query)
        return result.scalars().all()

    async def get_by_id(self, hotel_id: int):
        get_hotels_query = select(self.model).where(func.lower(self.model.id).ilike(f'%{hotel_id}%'))
        result = await self.session.execute(get_hotels_query)
        return result.scalars().first()

    async def edit(self, data: HotelSchema, hotel_id: int, exclude_unset: bool = False):
        update_hotel_stmt = (
            update(self.model)
            .values(**data.model_dump(exclude_unset=exclude_unset))
            .where(self.model.id == hotel_id).returning(self.model)
        )
        result = await self.session.execute(update_hotel_stmt)
        return result.scalar_one()

    async def delete(self, hotel_id: int):
        delete_hotel_stmt = delete(self.model).where(self.model.id == hotel_id).returning(self.model)
        result = await self.session.execute(delete_hotel_stmt)
        return result.scalar_one()

