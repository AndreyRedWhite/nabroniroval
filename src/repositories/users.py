from sqlalchemy import select, func

from src.models.users import UserOrm
from src.repositories.base import BaseRepository
from src.schemas.users import UserSchema


class UsersRepository(BaseRepository):
    model = UserOrm
    schema = UserSchema

    async def get_all(self, email: str):
        get_users_query = select(self.model)
        if email:
            get_users_query = get_users_query.filter(func.lower(self.model.email).ilike(f'%{email.strip().lower()}%'))
        result = await self.session.execute(get_users_query)
        return [self.schema.model_validate(item, from_attributes=True) for item in result.scalars()]
