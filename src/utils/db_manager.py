from repositories.auth import UsersRepositories
from repositories.hotels import HotelsRepositories
from repositories.rooms import RoomsRepositories
from repositories.bookings import BookingsRepositories
from repositories.facilities import FacilitiesRepositories, RoomsFacilitiesRepositories

class DBMamager:

    def __init__(self, session_factory):
        self.session_factory = session_factory


    async def  __aenter__(self):
        self.session = self.session_factory()
        self.bookings = BookingsRepositories(self.session)
        self.hotels = HotelsRepositories(self.session)
        self.rooms = RoomsRepositories(self.session)
        self.facilities = FacilitiesRepositories(self.session)
        self.rooms_facilities = RoomsFacilitiesRepositories(self.session)
        self.users = UsersRepositories(self.session)


        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()