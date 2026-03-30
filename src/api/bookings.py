from fastapi import APIRouter, Body

from src.api.dependencies import DBdeb, UserIdDep
from src.schemas.bookings import BookingAddRequestSchema, BookingAddSchema

router = APIRouter(prefix='/bookings', tags=['Бронирования'])


@router.get('')
async def get_bookings(db: DBdeb):
    all_bookings = await db.bookings.get_all()
    return {'all_bookings': all_bookings}


@router.get('/me')
async def get_me(db: DBdeb, user_id: UserIdDep):
    my_bookings = await db.bookings.get_my_bookings(user_id=user_id)
    return {'my_bookings': my_bookings}


@router.post('')
async def create_booking(db: DBdeb, user_id: UserIdDep, data: BookingAddRequestSchema = Body(...)):
    room = await db.rooms.get_one_or_none(hotel_id=data.hotel_id, room_id=data.room_id)
    room_price: int = room.price
    _data = BookingAddSchema(
        user_id=user_id,
        price=room_price,
        **data.model_dump()
    )
    result = await db.bookings.add_booking(_data)
    await db.commit()
    return {'message': 'OK', 'booking': result}

