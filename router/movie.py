from fastapi import APIRouter
from fastapi import APIRouter
from fastapi import Depends, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from config.database import Session
#from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middleware.JWT import JWTBearer
from movie import *
from servicio.service import *
from schema.user import *


movie_router=APIRouter

@movie_router.get('/peliculas',tags=['peliculas'],response_model=list[Peliculas],dependencies=[Depends(JWTBearer)])
def get_peliculas() -> List[Peliculas]:
    db = Session()
    result = db.query(Movie_Model).filter(Movie_Model.category == category).all()
    if not result:
      return JSONResponse(status_code=404, content={"message": "Movie not found"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.get('/peliculas/{id}',tags=['peliculas'],response_model=Peliculas)
def get_pelicula(id: int=Path(ge=1,le=1500)) -> Peliculas:
    db=Session()
    result=Movie_service(database).get_movies(id)
    try:
        pelicula=list(filter(lambda x: x['id']==id,peliculas))
        return pelicula
    except IndexError:
        return {'error':' pelicula no encontrada'}
    
#@app.get('/movie/{id}')
#def get_movie(id:int):

    #for movie in peliculas:
        #if movie['id']==id
        #return movie
    #raise HTMLResponse(status_code=404,detail='movie no found')
@movie_router.get('/peliculas/',tags=['peliculas'],response_model=List[Peliculas])
def get_peliculas_por_categoria(category: str=Query(min_length=5,max_length=15)) -> Peliculas:
    
    try:
        category=list(filter(lambda w: w['category']==category,peliculas))
        return category
    except SyntaxError:
        return {'error':'categoria no encontrada'}

@movie_router.post('/peliculas', tags=['pelicuas'], response_model=dict, status_code=201)
def create_movie(movie: Movie_model) -> dict:
    db = Session()
    new_movie = Movie_model(**movie.dict())
    db.add(new_movie)
    db.commit()
    return JSONResponse(status_code=201, content={"message": "Se ha registrado la película"})


    
@movie_router.post('/peliculas',tags=['peliculas'],response_model=dict)
def create_movie(pelicula:Peliculas) -> dict:
    peliculas.append(pelicula)
    return peliculas
    

@movie_router.put(
    "/peliculas/{id}",
    status_code=status.HTTP_200_OK,
    summary="Update movie",
    tags=['peliculas'],
    response_model=dict
)
def update_movie(id: int,pelicula:Peliculas) -> dict:
    db = Session()
    result = Movie_service(database).get_movie(id)

    if not result: 
        return JSONResponse(status_code=201, content={"message": "Updated done"})
    #otra forma de hacer el filtrado

    Movie_service(database).update_movie(id,movie)
    return JSONResponse(status_code=201, content={"message": "Updated done"})
@movie_router.delete(
    "/pelicula/{id}",
    status_code=status.HTTP_200_OK,
    summary="Delete movie",
    tags=['peliculas'],
    response_model=dict) 
def delete_movie(id: int) -> dict:
    db = Session()
    result = db.query(Movie_model).where(Movie_model.id == id).first()

    if not  result:
        return JSONResponse(status_code=200, content={"message": "Record deleted"})
    Movie_service(database).delete_movie(id)
    return JSONResponse(status_code=200, content={"message": "se ha elimano la pelicula"})




    