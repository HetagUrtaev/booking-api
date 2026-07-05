from typing import Annotated
from fastapi import Depends, Query
from pydantic import BaseModel

# Данный документ нужен дя создания схем, параметр которого лягут в URL запроса


class PaginationParams(BaseModel): # данная схема касается пагинации

    page: Annotated[int | None, Query(default=None, ge=1)]
    per_page: Annotated[int | None, Query(default=None, ge=1, lt=30)]


PaginationDep = Annotated[PaginationParams, Depends()]
