from model.movie import *
from schema.movie import *
class Movie_service():
    def __init__(self,database) -> None:
        self.database=database

    def get_movies(self):
        result=self.database.query(Movie_model).all
        return result
    
    def get_movie(self):
        result=self.database.query(Movie_model).all
        return result
    
    def get_movie_by_category(self):
        result=self.database.query(Movie_model).filter(Movie_model.catagory=='catagory').all
        return result
    
    def create_movie(self, movie: Movie):
        data = movie.dict(exclude_unset=True)

        exclude_fields = ["id"]
        if all(field in list(data.keys()) for field in exclude_fields):
            raise Exception("Ha agregado campos no editables")

        new_movie =Movie_model(**data)
        self.database.add(new_movie)
        self.database.commit()

    def update_movie(self, movie_id: int, movie: Movie):
        result = self.database.query(Movie_model).filter(Movie_model.id == movie_id)

        data = movie.dict(exclude_unset=True)

        exclude_fields = ["id"]
        if all(field in list(data.keys()) for field in exclude_fields):
            raise Exception("Ha agregado campos no editables")

        result.update(data)
        self.database.commit()

    def delete_movie(self, movie_id: int):
        result = self.get_movie(movie_id)
        self.database.delete(result)
        self.database.commit()