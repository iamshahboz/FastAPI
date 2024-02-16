from enum import Enum 
from datetime import date
from pydantic import BaseModel


class GenreURLChoices(Enum):
    ROCK = 'rock'
    ELECTRONIC = 'electronic'
    METAL = 'metal'
    HIP_HOP = 'hip-hop'
    


class Album(BaseModel):
    title: str
    release_date: date

class BandBase(BaseModel):
    name: str 
    genre: str 
    albums: list[Album] = []

class BandCreate(BandBase):
    pass 

class BandwithID(BandBase):
    id: int 
    



