from datetime import date

from pydantic import BaseModel, ConfigDict


class BookingAddReqest(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class BookingAdd(BaseModel):
    user_id: int
    price: int
    room_id: int
    date_from: date
    date_to: date


class Booking(BookingAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)
