from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Text, Table
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime, UTC

Base = declarative_base()

# Tabla intermedia para favoritos
user_favorites = Table(
    "user_favorites", Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("movie_id", Integer, ForeignKey("movies.id"))
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)

    reviews = relationship("Review", back_populates="user")
    favorites = relationship("Movie", secondary=user_favorites, back_populates="favorited_by")


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    overview = Column(Text)
    release_date = Column(String)
    poster_path = Column(String)

    reviews = relationship("Review", back_populates="movie")
    favorited_by = relationship("User", secondary=user_favorites, back_populates="favorites")


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    movie_id = Column(Integer, ForeignKey("movies.id"))
    rating = Column(Float)
    comment = Column(Text)
    date = Column(DateTime, default=datetime.now(UTC))

    user = relationship("User", back_populates="reviews")
    movie = relationship("Movie", back_populates="reviews")
