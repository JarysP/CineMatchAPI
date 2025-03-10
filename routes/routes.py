from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.models import Movie, User, Review
from config.dependence import get_db
import httpx

router = APIRouter()

TMDB_API_KEY = "tu_api_key"

# Búsqueda de películas
@router.get("/movies")
def search_movies(query: str, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.title.ilike(f"%{query}%")).first()
    if movie:
        return movie

    # Si no está en la BD, buscar en TMDB
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={query}"
    response = httpx.get(url).json()

    if "results" in response and response["results"]:
        movie_data = response["results"][0]
        new_movie = Movie(
            id=movie_data["id"],
            title=movie_data["title"],
            overview=movie_data["overview"],
            release_date=movie_data["release_date"],
            poster_path=movie_data.get("poster_path", "")
        )
        db.add(new_movie)
        db.commit()
        return new_movie

    raise HTTPException(status_code=404, detail="Película no encontrada")

# Detalle de película
@router.get("/movies/{id}")
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(movie_id == Movie.id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    return movie

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