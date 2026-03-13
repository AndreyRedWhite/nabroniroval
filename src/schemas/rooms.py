from pydantic import BaseModel


class GetAllRooms(BaseModel):
    hotel_id: int


class RoomAddSchema(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int


class RoomPatchSchema(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None


class RoomSchema(RoomAddSchema):
    room_id: int
    hotel_id: int