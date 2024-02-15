from fastapi import FastAPI, HTTPException
from schemas import GenreURLChoices, Band, Album


app = FastAPI()

# don't forget to add type hints




BANDS = [
    {'id':1, 'name': 'The kinks', 'genre': 'Rock'},
    {'id':2, 'name': 'Aphex Twin', 'genre': 'Electronic'},
    {'id':3, 'name': 'Slowdive', 'genre': 'Shoegaze', 'albums': [
        {'title': 'Master of Reality', 'release_date': '1971-07-21'}
    ]},
    {'id':4, 'name': 'Wu Tang Chan', 'genre': 'Hip-Hop'},
]


@app.get('/bands')
async def bands(
    genre: GenreURLChoices | None=None,
    has_albums: bool = False
    ) -> list[Band]:
    band_list = [Band(**b) for b in BANDS]
    if genre:
        band_list =  [
            b for b in band_list if b.genre.lower() == genre.value
        ]
    if has_albums:
        band_list = [b for b in band_list if len(b.albums) > 0]
    return band_list

@app.get('/bands/{band_id}')
async def bands(band_id: int) -> Band:
    band = next((Band(**b) for b in BANDS if b['id'] == band_id),None)
    if band is None:
        raise HTTPException(status_code=404, detail='Band not found')
    return band 

@app.get('/bands/genre/{genre}')
async def bands_for_genre(genre: GenreURLChoices) -> list[dict]:
    return [
        b for b in BANDS if b['genre'].lower() == genre.value
    ]


