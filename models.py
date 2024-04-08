from enum import Enum 
from datetime import date
from pydantic import BaseModel, validator
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional


class GenreURLChoices(Enum):
    ROCK = 'rock'
    ELECTRONIC = 'electronic'
    METAL = 'metal'
    HIP_HOP = 'hip-hop'


class GenreChoices(Enum):
    ROCK = 'Rock'
    ELECTRONIC = 'Electronic'
    METAL = 'Metal'
    HIP_HOP = 'Hip-hop'
    

class AlbumBase(SQLModel):
    title: str
    release_date: date
    band_id: int | None = Field(default=None, foreign_key="band.id")


class Album(AlbumBase, table=True):
    id: int = Field(default=None, primary_key=True)
    band: "Band" = Relationship(back_populates='albums')


class BandBase(SQLModel):
    name: str 
    genre: GenreChoices 
    

class BandCreate(BandBase):
    albums: list[AlbumBase] | None = None
    @validator('genre',pre=True)
    def title_case_genre(cls,value):
        return value.title()
    

class Band(BandBase, table=True):
    id: int = Field(default=None, primary_key=True)
    albums: list[Album] = Relationship(back_populates='band')
    date_formed : date | None 


    



