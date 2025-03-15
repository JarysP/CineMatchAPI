from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models.models
import schemas.schema
from models.models import Movie, User, Review
from config.dependence import get_db
import httpx

router = APIRouter()

TMDB_API_KEY = "4f5f43495afcc67e9553f6c684a82f84"


# Búsqueda de películas
@router.get("/movie_by_name", response_model=List[schemas.schema.MovieSchema])
def search_movies(query: str, db: Session = Depends(get_db)):
    movies = db.query(Movie).filter(Movie.title.ilike(f"%{query.strip()}%")).all()
    if movies:
        return movies

    # Si no está en la BD, buscar en TMDB
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={query}"
    response = httpx.get(url).json()

    if "results" in response and response["results"]:
        new_movies = []

        for movie_data in response["results"]:
            # Verificar si la película ya existe en la BD para evitar duplicados
            existing_movie = db.query(Movie).filter(Movie.id == movie_data["id"]).first()
            if not existing_movie:
                new_movie = Movie(
                    id=movie_data["id"],
                    title=movie_data["title"],
                    overview=movie_data["overview"],
                    release_date=movie_data["release_date"],
                    poster_path=movie_data.get("poster_path", "")
                )
                db.add(new_movie)
                new_movies.append(new_movie)

        db.commit()
        movies = db.query(Movie).filter(Movie.title.ilike(f"%{query.strip()}%")).all()

        return movies

    raise HTTPException(status_code=404, detail="Película no encontrada")

# Consultar peliculas
@router.get("/movies/", response_model=List[schemas.schema.MovieSchema])
def get_movies(db: Session = Depends(get_db)):
    movies = db.query(models.models.Movie).limit(20).all()
    return movies

# Agregar reseña
@router.post("/reviews")
def add_review(user_id: int, movie_id: int, rating: float, comment: str, db: Session = Depends(get_db)):
    review = Review(user_id=user_id, movie_id=movie_id, rating=rating, comment=comment)
    db.add(review)
    db.commit()
    return {"message": "Reseña agregada"}

# Favoritos de usuario
@router.get("/users/{id}/favorites")
def get_favorites(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(user_id == User.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user.favorites