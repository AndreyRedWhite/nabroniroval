from sqlalchemy import insert, select

from src.models.bookings import BookingOrm
from src.repositories.base import BaseRepository
from src.schemas.bookings import BookingSchema, BookingAddSchema


class BookingsRepository(BaseRepository):
    model = BookingOrm
    schema = BookingSchema

    async def add_booking(self, booking: BookingAddSchema):
        add_room_stmt = insert(self.model).values(**booking.model_dump()).returning(self.model)
        result = await self.session.execute(add_room_stmt)
        return self.schema.model_validate(result.scalar_one(), from_attributes=True)


    async def get_my_bookings(self, user_id: int):
        get_bookings_query = (
            select(self.model).where(BookingOrm.user_id == user_id)
        )
        result = await self.session.execute(get_bookings_query)
        return [self.schema.model_validate(row, from_attributes=True) for row in result.scalars().all()]
