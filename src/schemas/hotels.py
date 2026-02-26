from pydantic import BaseModel


class HotelSchema(BaseModel):
    title: str
    location: str


class HotelPatchSchema(BaseModel):
    title: str | None = None
    location: str | None = None