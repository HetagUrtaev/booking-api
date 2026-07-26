from typing import Annotated
from fastapi import Depends, Query
from pydantic import BaseModel
from fastapi import Request, HTTPException

from service.auth import AuthServise


# Данный документ нужен для создания схем, параметр которого лягут в URL запроса

class PaginationParams(BaseModel): # данная схема касается пагинации

    page: Annotated[int | None, Query(default=1, ge=1)]
    per_page: Annotated[int | None, Query(default=None, ge=1, lt=30)]


PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request) -> str:
    token = request.cookies.get("access_token", None)
    if not token:
        raise HTTPException(status_code=401, detail= 'Вы не аутентифицированы')
    return token

def get_current_user_id(token: str = Depends(get_token)) ->int:

    data = AuthServise().decode_token(token)
    return data['user_id']


UserIdDep = Annotated[int, Depends(get_current_user_id)]

