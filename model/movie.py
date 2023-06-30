from config.database import Base
from sqlalchemy import Integer,FLOAT,Column,String

class Movie_model(Base):
    __tablename__= "movies"

    id=Column(Integer,primary_key=True)
    title=Column(String)
    overview=Column(String)
    year=Column(Integer)
    rating=Column(FLOAT)
    catagory=Column(String)
