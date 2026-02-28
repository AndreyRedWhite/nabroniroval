from fastapi import Query, APIRouter, Body, Depends

from sqlalchemy import insert, select, func

from src.api.dependencies import PaginationDep
from src.database import async_session_maker, engine
from src.models.hotels import HotelOrm
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import HotelSchema, HotelPatchSchema

router = APIRouter(prefix='/hotels', tags=['Отели'])


post_examples = {"1": {"summary": "Сочи", "value":
    {"title": "hotel sochi", "location": "Сочи, Ленина, 1"}},
                 "2": {"summary": "Дубай", "value":
    {"title": "hotel dubai", "location": "Дубай, шейха 1"}}}


@router.get(path="", summary='Get all the hotels')
async def get_hotels(
    pagination: PaginationDep,
    title: str | None = Query(default=None, description='Название отеля'),
    location: str | None = Query(default=None, description='Адрес отеля')
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            title=title, location=location, limit=per_page, offset=per_page * (pagination.page - 1))


@router.post(path="", summary='Add new wonderful hotel')
async def add_hotel(data: HotelSchema = Body(openapi_examples=post_examples)):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(data)
        await session.commit()
        return {'status': 'OK', 'hotel': hotel}



@router.put(path="/{hotel_id}", summary='Update all the info about particular hotel')
async def update_hotel(
    hotel_id: int, data: HotelSchema = Body(openapi_examples=post_examples)):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).edit(data, hotel_id=hotel_id)
        await session.commit()
        return {'status': 'OK', 'hotel': hotel}


@router.delete(path="/{hotel_id}", summary='Delete hotel')
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        delhotel = await HotelsRepository(session).delete(hotel_id=hotel_id)
        await session.commit()
        return {'status': 'OK', 'hotel': delhotel}




@router.patch(path="/{hotel_id}", summary='Partially update an info about particular hotel')
async def patch_hotel(
    hotel_id: int, data: HotelPatchSchema = Body(openapi_examples=post_examples)):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).edit(data, hotel_id=hotel_id, exclude_unset=True)
        await session.commit()
        return {'status': 'OK', 'hotel': hotel}
