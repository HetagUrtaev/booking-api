from repositories.mappers.mappers import BookingDataMapper
from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepositories




class BookingsRepositories(BaseRepositories):
    model = BookingsOrm
    mapper = BookingDataMapper
