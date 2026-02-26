from fastapi import Query, APIRouter, Body, Depends

from sqlalchemy import insert, select, func

from src.api.dependencies import PaginationDep
from src.database import async_session_maker, engine
from src.models.hotels import HotelOrm
from src.schemas.hotels import HotelSchema

router = APIRouter(prefix='/hotels', tags=['Отели'])


post_examples = {"1": {"summary": "Сочи", "value":
    {"title": "hotel sochi", "location": "Сочи, Ленина, 1"}},
                 "2": {"summary": "Дубай", "value":
    {"title": "hotel dubai", "location": "Дубай, шейха 1"}}}


@router.get(path="", summary='Get all the hotels')
async def get_hotels(
    pagination: PaginationDep,
    title: str | None = Query(default=None, description='Название отеля'),
    location: str | None = Query(default=None, description='Адрес отеля')):
    async with async_session_maker() as session:
        get_hotels_query = select(HotelOrm)
        if title:
            get_hotels_query = get_hotels_query.filter(func.lower(HotelOrm.title).ilike(f'%{title.strip().lower()}%'))
        if location:
            get_hotels_query = get_hotels_query.filter(func.lower(HotelOrm.location).ilike(f"%{location.strip().lower()}%"))
        get_hotels_query = (
            get_hotels_query
            .limit(pagination.per_page)
            .offset(pagination.page * (pagination.page - 1))
        )
        result = await session.execute(get_hotels_query)
        hotels = result.scalars().all()
        return hotels


@router.post(path="", summary='Add new wonderful hotel')
async def add_hotel(data: HotelSchema = Body(openapi_examples=post_examples)):
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelOrm).values(**data.model_dump())
        # раскомментировать для отладки - будут видны все запросы в базу:
        # print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await session.execute(add_hotel_stmt)
        await session.commit()
        return {'status': 'OK'}



# @router.put(path="/{hotel_id}", summary='Update all the info about particular hotel')
# def update_hotel(
#     hotel_id: int, data: HotelSchema):
#     global hotels
#     for hotel in hotels:
#         if hotel['id'] == hotel_id:
#             hotel['title'] = data.title
#             hotel['name'] = data.name
#             return {"status": "OK"}
#         else:
#             return {'status': 'bad parameter'}


# @router.patch(path="/{hotel_id}", summary='Partially update an info about particular hotel')
# def patch_hotel(
#     hotel_id: int, data: HotelSchemaPatch):
#     global hotels
#     for hotel in hotels:
#         if hotel["id"] == hotel_id:
#             if data.title:
#                 hotel['title'] = data.title
#             if data.name:
#                 hotel['name'] = data.name
#             return {"status": "OK"}
#         else:
#             return {'status': 'bad parameter'}
