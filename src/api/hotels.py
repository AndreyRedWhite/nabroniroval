from fastapi import Query, APIRouter, Body

from src.api.dependencies import PaginationDep


router = APIRouter(prefix='/hotels', tags=['Отели'])

hotels = [
    {"id": 1, "title": "sochi", "name": "Sochi_Star"},
    {"id": 2, "title": "dubai", "name": "Dubai_parus"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]

post_examples = {"1": {"summary": "Сочи", "value":
    {"title": "hotel sochi", "location": "Сочи, Ленина, 1"}},
                 "2": {"summary": "Дубай", "value":
    {"title": "hotel dubai", "location": "Дубай, шейха 1"}}}


@router.get(path="", summary='Get all the hotels',
            # response_model=list[HotelSchema]
            )
def get_hotels(
    params: PaginationDep,
    id: int | None = Query(default=None, description='ID отеля'),
    title: str | None = Query(default=None, description='Название отеля'),
    ):
    filtered_hotels = []
    for hotel in hotels:
        if id is not None and hotel['id'] != id:
            continue
        if title is not None and hotel['title'] != title:
            continue
        filtered_hotels.append(hotel)

    # Пагинация
    start_idx = (params.page - 1) * params.per_page
    end_idx = start_idx + params.per_page

    # Проверка выхода за границы списка
    if start_idx >= len(filtered_hotels):
        return []

    return filtered_hotels[start_idx:end_idx]


@router.delete(path='/{hotel_id}', summary='Delete a particular hotel')
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {'status': 'OK'}


# @router.post(path="", summary='Add new wonderful hotel')
# async def add_hotel(data: HotelSchema = Body(openapi_examples=post_examples)):
#     async with async_session_maker() as session:
#         add_hotel_stmt = insert(HotelsOrm).values(**data.model_dump())
#         print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
#         await session.execute(add_hotel_stmt)
#         await session.commit()
#     return {'status': 'OK'}


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
