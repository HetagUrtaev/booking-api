from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepositories
from src.schemas.bookings import Booking



class BookingsRepositories(BaseRepositories):
    model = BookingsOrm
    schema = Booking
