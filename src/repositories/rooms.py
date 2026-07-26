from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepositories


class RoomsRepositories(BaseRepositories):
    model = RoomsOrm