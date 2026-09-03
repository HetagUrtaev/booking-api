from sqlalchemy import  select
from pydantic import EmailStr

from src.models.users import UsersOrm
from src.repositories.base import BaseRepositories
from src.schemas.auth import User, UserWithHashedPassword



class UsersRepositories(BaseRepositories):
    model = UsersOrm
    schema = User

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        res = result.scalars().one_or_none()
        if res is None:
            return None
        return UserWithHashedPassword.model_validate(res, from_attributes=True)
