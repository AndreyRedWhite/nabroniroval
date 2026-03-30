from fastapi import Query, APIRouter, Body

from src.api.dependencies import PaginationDep, DBdeb
from src.schemas.hotels import HotelPatchSchema, HotelAddSchema

router = APIRouter(prefix='/hotels', tags=['Отели'])


post_examples = {"1": {"summary": "Сочи", "value":
    {"title": "hotel sochi", "location": "Сочи, Ленина, 1"}},
                 "2": {"summary": "Дубай", "value":
    {"title": "hotel dubai", "location": "Дубай, шейха 1"}}}


@router.get(path="", summary='Get all hotels')
async def get_hotels(
    pagination: PaginationDep,
    db: DBdeb,
    title: str | None = Query(default=None, description='Название отеля'),
    location: str | None = Query(default=None, description='Адрес отеля')
):
    per_page = pagination.per_page or 5
    return await db.hotels.get_all(
        title=title, location=location, limit=per_page, offset=per_page * (pagination.page - 1))


@router.get(path="/{id}", summary='Get a specific hotel')
async def get_hotel(hotel_id: int, db: DBdeb):
    return await db.hotels.get_one_or_none(hotel_id)


@router.post(path="", summary='Add new wonderful hotel')
async def add_hotel(db: DBdeb, data: HotelAddSchema = Body(openapi_examples=post_examples)):
    hotel = await db.hotels.add(data)
    await db.commit()
    return {'status': 'OK', 'hotel': hotel}


@router.put(path="/{hotel_id}", summary='Update all the info about particular hotel')
async def update_hotel(
    hotel_id: int, db: DBdeb ,data: HotelAddSchema = Body(openapi_examples=post_examples)):
    hotel = await db.hotels.edit(data, hotel_id=hotel_id)
    await db.commit()
    return {'status': 'OK', 'hotel': hotel}


@router.delete(path="/{hotel_id}", summary='Delete hotel')
async def delete_hotel(hotel_id: int, db: DBdeb):
    delhotel = await db.hotels.delete(hotel_id=hotel_id)
    await db.commit()
    return {'status': 'OK', 'hotel': delhotel}


@router.patch(path="/{hotel_id}", summary='Partially update an info about particular hotel')
async def patch_hotel(
    hotel_id: int, db: DBdeb, data: HotelPatchSchema = Body(openapi_examples=post_examples)):
    hotel = await db.hotels.edit(data, hotel_id=hotel_id, exclude_unset=True)
    await db.commit()
    return {'status': 'OK', 'hotel': hotel}
