from pydantic import BaseModel

class MovieSchema(BaseModel):
    id: int
    title: str
    overview: str
    release_date: str
    poster_path: str

    class Config:
        orm_mode = True