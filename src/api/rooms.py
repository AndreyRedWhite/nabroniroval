from fastapi import APIRouter, Body

from src.schemas.rooms import RoomAddSchema, RoomPatchSchema
from src.api.dependencies import DBdeb

router = APIRouter(prefix='/hotels', tags=['Номера'])

post_examples = {"1": {"summary": "King", "value":
    {"title": "King suite", "description": "Room for essentials kings", "price": 100, "quantity": 1}}}


@router.get('/{hotel_id}/rooms', summary='Get all rooms for the hotel')
async def get_rooms(hotel_id: int, db: DBdeb):
    return await db.rooms.get_all_rooms(hotel_id=hotel_id)


@router.get('/{hotel_id}/rooms/{room_id}', summary='Get specific room')
async def get_room(hotel_id: int, room_id: int, db: DBdeb):
    return await db.rooms.get_one_or_none(hotel_id=hotel_id, room_id=room_id)


@router.post('/{hotel_id}/rooms', summary='Create new room')
async def create_room(hotel_id: int, db: DBdeb, data: RoomAddSchema = Body(openapi_examples=post_examples)):
    room = await db.rooms.add_room(data, hotel_id)
    await db.commit()
    return {'status': 'OK', 'room': room}


@router.put('/{hotel_id}/rooms/{room_id}', summary='Update room')
async def update_room(
    hotel_id: int, room_id: int, db: DBdeb, data: RoomAddSchema = Body(openapi_examples=post_examples)):
    room = await db.rooms.edit_room(data, hotel_id, room_id)
    if not room:
        return {'status': 'Error', 'message': 'Room not found'}
    await db.commit()
    return {'status': 'OK', 'room': room}


@router.patch('/{hotel_id}/rooms/{room_id}', summary='Update room')
async def update_room(
    hotel_id: int, room_id: int, db: DBdeb, data: RoomPatchSchema = Body(openapi_examples=post_examples)):
    room = await db.rooms.edit_room(data, hotel_id, room_id, exclude_unset=True)
    await db.commit()
    return {'status': 'OK', 'room': room}


@router.delete('/{hotel_id}/rooms/{room_id}', summary='Delete room')
async def delete_room(hotel_id: int, room_id: int, db: DBdeb):
    await db.rooms.delete(hotel_id=hotel_id, room_id=room_id)
    await db.commit()
    return {'status': 'OK'}