from sqlalchemy import select, insert, update

from src.models.rooms import RoomOrm
from src.repositories.base import BaseRepository
from src.schemas.rooms import GetAllRooms, RoomSchema, RoomAddSchema


class RoomsRepository(BaseRepository):
    model = RoomOrm
    schema = RoomSchema

    async def get_all_rooms(self, hotel_id: int):
        get_rooms_query = select(self.model).where(self.model.hotel_id==hotel_id).order_by(self.model.room_id)
        result = await self.session.execute(get_rooms_query)
        return [self.schema.model_validate(item, from_attributes=True) for item in result.scalars().all()]

    async def add_room(self, room: RoomAddSchema, hotel_id: int):
        add_room_stmt = (
            insert(self.model)
            .values(**room.model_dump(), hotel_id=hotel_id).
            returning(self.model))
        result = await self.session.execute(add_room_stmt)
        return self.schema.model_validate(result.scalar_one(), from_attributes=True)

    async def edit_room(self, room: RoomAddSchema, hotel_id: int, room_id: int, exclude_unset: bool = False):
        edit_room_stmt = (
            update(self.model)
            .where(self.model.hotel_id==hotel_id, self.model.room_id==room_id)
            .values(**room.model_dump(exclude_unset=exclude_unset))
            .returning(self.model)
        )
        result = await self.session.execute(edit_room_stmt)
        if not result:
            return {'status': 'Error', 'message': 'Room not found'}
        return self.schema.model_validate(result.scalar_one(), from_attributes=True)

