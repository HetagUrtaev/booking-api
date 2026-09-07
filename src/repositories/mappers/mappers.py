from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.schemas.facilities import Facility, RoomFacility
from src.models.bookings import BookingsOrm
from src.models.rooms import RoomsOrm
from src.models.users import UsersOrm
from src.schemas.auth import User
from src.schemas.bookings import Booking
from src.schemas.rooms import Room, RoomWithRels
from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel
from src.repositories.mappers.base import DataMapper


class HotelDataMapper(DataMapper):
    db_model = HotelsOrm
    schema = Hotel


class RoomDataMapper(DataMapper):
    db_model = RoomsOrm
    schema = Room

class RoomWithRelsMapper(DataMapper):
    db_model = RoomsOrm
    schema = RoomWithRels

class UserDataMapper(DataMapper):
    db_model = UsersOrm
    schema = User

class BookingDataMapper(DataMapper):
    db_model = BookingsOrm
    schema = Booking

class FacilityDataMapper(DataMapper):
    db_model = FacilitiesOrm
    schema = Facility

class RoomFacilityDataMapper(DataMapper):
    db_model = RoomsFacilitiesOrm
    schema = RoomFacility