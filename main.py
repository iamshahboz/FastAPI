from fastapi import FastAPI, Depends, HTTPException, Query
from models import GenreURLChoices, GenreChoices, Band, Album, BandCreate
# from contextlib import asynccontextmanager
from db import init_db, get_session
from sqlmodel import Session, select
from typing import Annotated
import uvicorn


# @asynccontextmanager
# async def lifespan(app:FastAPI):
#     init_db()
#     yield


app = FastAPI() #lifespan=lifespan



@app.get('/bands', description= 'Get all bands')
async def get_all_bands(
    genre: GenreURLChoices | None=None,
    q: Annotated[str | None, Query(max_length=10)] = None,
    session: Session = Depends(get_session)
    ) -> list[Band]:

    band_list = session.exec(select(Band)).all()

    if genre:
        band_list = [
            b for b in band_list if b.genre.value.lower() == genre.value
        ]
    if q:
        band_list = [
            b for b in band_list if q.lower() in b.name.lower()
        ]
    return band_list
    

@app.get('/bands/{band_id}', description="Get band by id")
async def get_band_by_id(band_id: int,
                session: Session = Depends(get_session)
) -> Band:
    band = session.get(Band, band_id)
    if band is None:
        raise HTTPException(status_code=404, detail="Band not found")
    
    return band
    

@app.post('/bands', description="Create a new band filling required fields")
async def create_a_band(band_data:BandCreate,
                      session: Session = Depends(get_session)
                      ) -> Band:
    band = Band(name = band_data.name, genre=band_data.genre)
    session.add(band)
    
    if band_data.albums:
        for album in band_data.albums:
            album_obj = Album(
                title=album.title, release_date=album.release_date,
                band = band
            )
            session.add(album_obj)
    session.commit()
    session.refresh(band)
    return band 





if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)









