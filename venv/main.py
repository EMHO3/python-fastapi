from fastapi import FastApi,Body,Path
from fastapi.responses import HTMLresponse,JSONResponse
from pydantic import BaseModel,Field
from typing import Optional,List

app= FastApi()

app=FastApi()
app.title="Mi aplicacion con fastapi"
app.version="0.0.1"
class Movie(BaseModel):
   id:Optional[int] = None
   title:str=Field( min_length=5, max_length=15)
   overview:str= Field( min_length=15, max_length=50)
   year:int = Field(le=2022)
   rating:float=Field(ge=1,le=10)
   category:str=Field( min_length=5, max_length=15)

   class config:
       schema_extra={
           "example":{
               "id":1,
               "title": "Mi pelicula",
               "overview":"descripcion de la pelicula",
               "year":2022,
               "rating":9.8,
               "category":"accion"
           }
       }

movies=[
     {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    } 
]



@app.get("/",tags=['home'])
def message():
    return HTMLresponse('<h1>Hello Wolrd</h1>')

app.get('/movies',tags=['movies'],response_model=List[Movie])
def get_movies() -> List[Movie]:
  return JSONResponse(content=movies)

@app.get('/movies/{id}',tags=['movies'],response_model=Movie)
def get_movie(id:int=Path(ge=1,le=2000))->Movie:
   for item in movies:
      if item["id"]==id:
         return JSONResponse(content=item)
   return JSONResponse(content=[])

@app.get('/movies',tags=['movies'],response_model=List[Movie])
def get_movies_by_category(category:str=Query(min_length=5,max_length=15))->List[Movie]:
   data= [item for item in movies if item['category']== category]
   return JSONResponse(content=[])

@app.post('/movies',tags=['movies'],response_model=dict)
def create_movie(movie:Movie)->dict:
   movies.append(movie)
   return JSONResponse(content={'message':'se registro la pelicula'})

@app.put('/movies/{id}', tags=['movies'],response_model=dict)
def update_movie(id: int, movie: Movie)->dict:
	for item in movies:
		if item["id"] == id:
			item['title'] = movie.title
			item['overview'] = movie.overview
			item['year'] = movie.year
			item['rating'] = movie.rating
			item['category'] = movie.category
			return JSONResponse(content={'message':'se ah modificado la pelicula'})
        


@app.delete('/movies/{id}', tags=['movies'], response_model=dict)
def delete_movie(id: int)-> dict:
     for item in movies:
         if item["id"] == id:
             movies.remove(item)
             return JSONResponse(content={"message": "Se ha eliminado la película"})        

   
   

