from typing import Union
from fastapi import FastAPI
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi import FastAPI,HTTPException
from fastapi import Depends
from fastapi import FastAPI,Query,Path,Body
from fastapi import status
from fastapi.security.http import HTTPAuthorizationCredentials
from pydantic import BaseModel,Field
from typing import Optional,List
import datetime
from starlette.requests import Request
from utils.jwt_api import*
from fastapi.security import HTTPBearer
from config.database import Session, engine, Base
from middleware.error import *
from model import *
from middleware.JWT import *
from router.movie import *
from router.user import *


peliculas= [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    }, 
    {
        'id': 2,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    },
     {
        'id': 3,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    } 
]
app=FastAPI()
app.title='aplicacion con FastAPI'
app.version='0.0.1'

app.middleware(Manejo_de_erro)
app.include_router(movie_router)
app.include_router(user_router)

Base.metadata.create_all(bind=engine)

class JWTBearer(HTTPBearer):
   async def __call__(self, request: Request):
        auth=await super().__call__(request)
        validar_token(auth.credentials)
        if data ['email'] != "juangmail.com":
            raise HTTPException(status_code=403, detail=" credenciales no validas")
class client(BaseModel):
    email:str
    password:str


class Peliculas(BaseModel):
    id:Optional[int]=None
    title: str=Field(min_length=8,max_length=15)
    overview:str =Field(min_length=5,max_length=16)
    year:int =Field(le=2019)
    rating:float=Field(ge=1,le=10)
    category:str=Field(min_length=5,max_length=12)
    class Config:
        schema={
            'example':{
                'id':1,
                'title':"Mi pelicula",
                'overview':"Descripcion de la pelicula",
                'year':2019,
                'rating':9.8,
                'category':"category"
            }
        }
@app.get("/", tags=['Home'])
def message():
    return HTMLResponse('<h1>Hello world<h1>')

@app.post('/login',tags=['autenticacion'])
def loging_user(user:client):
    if user.email == "juan@gmail.com" and user.password == "juan123" :
        token: str =create_token(user.dict())
        return HTMLResponse(status_code=200, content=token)
    else:
        return HTMLResponse(status_code=401, content={"message": "Credenciales inválidas, intente de nuevo"})
       


@app.get('/peliculas',tags=['peliculas'],response_model=list[Peliculas],dependencies=[Depends(JWTBearer)])
def get_peliculas() -> List[Peliculas]:
    db = Session()
    result = db.query(Movie_Model).filter(Movie_Model.category == category).all()
    if not result:
      return JSONResponse(status_code=404, content={"message": "Movie not found"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@app.get('/peliculas/{id}',tags=['peliculas'],response_model=Peliculas)
def get_pelicula(id: int=Path(ge=1,le=1500)) -> Peliculas:
    db=Session()
    result=db.query(Movie_model).filter(Movie_model.id==id).first()
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
@app.get('/peliculas/',tags=['peliculas'],response_model=List[Peliculas])
def get_peliculas_por_categoria(category: str=Query(min_length=5,max_length=15)) -> Peliculas:
    try:
        category=list(filter(lambda w: w['category']==category,peliculas))
        return category
    except SyntaxError:
        return {'error':'categoria no encontrada'}

@app.post('/peliculas', tags=['pelicuas'], response_model=dict, status_code=201)
def create_movie(movie: Movie_model) -> dict:
    db = Session()
    new_movie = Movie_model(**movie.dict())
    db.add(new_movie)
    db.commit()
    return JSONResponse(status_code=201, content={"message": "Se ha registrado la película"})


    
@app.post('/peliculas',tags=['peliculas'],response_model=dict)
def create_movie(pelicula:Peliculas) -> dict:
    peliculas.append(pelicula)
    return peliculas
    

@app.put(
    "/peliculas/{id}",
    status_code=status.HTTP_200_OK,
    summary="Update movie",
    tags=['peliculas'],
    response_model=dict
)
def update_movie(id: int,pelicula:Peliculas) -> dict:
    db = Session()
    result = db.query(Movie_Model).where(Movie_Model.id == id).first()

    if result: 
        result.title = movie.title
        result.category = movie.overview
        result.overview = movie.overview
        result.rating = movie.rating
        result.year = movie.year  
        db.commit()
        return JSONResponse(status_code=201, content={"message": "Updated done"})
    #otra forma de hacer el filtrado
    filtered_list_movies = list(filter(lambda x: id == x["id"], Peliculas))
    list_movies = list(filtered_list_movies)
    if not list_movies:
        raise HTTPException(status_code=404, detail="Movie not found! t(-_-t)")
    else:
        print("DEBUGGER")

        peliculas[0].update({
            "id": id,
            "title": Peliculas["title"],
            "overview": Peliculas["overview"],
            "year": Peliculas["year"],
            "rating": Peliculas["rating"],
            "category": Peliculas["category"],
        })

    return peliculas


@app.delete(
    "/pelicula/{id}",
    status_code=status.HTTP_200_OK,
    summary="Delete movie",
    tags=['peliculas'],
    response_model=dict) 
def delete_movie(id: int) -> dict:
    db = Session()
    result = db.query(Movie_Model).where(Movie_Model.id == id).first()

    if result: 
        db.delete(result)
        db.commit()
        return JSONResponse(status_code=200, content={"message": "Record deleted"})

    if not result:
        return JSONResponse(status_code=404, content={'message': 'ID No found'})

    
    filtered_list_movies = list(filter(lambda x: id == x["id"], peliculas))
    list_movies = list(filtered_list_movies)
    if not list_movies:
        raise HTTPException(status_code=404, detail="Movie not found! t(-_-t)")
    else:
        print("DEBUGGER")

        peliculas.pop(0)

    return peliculas