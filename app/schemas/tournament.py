from pydantic import BaseModel, EmailStr
from datetime import datetime


class TournamentCreate(BaseModel):
    """creates tournament when client sends data"""
    name: str
    max_players: int
    start_at: datetime


class TournamentOut(BaseModel):
    """used when API returns tournament info"""
    id: int
    name: str
    max_players: int
    start_at: datetime
    registered_players: int

    class Config:
        """This model receives SQLAlchemy ORM objects, not just plain dicts"""
        orm_mode: True


class PlayerCreate(BaseModel):
    name: str
    email: EmailStr


class PlayerOut(BaseModel):
    """used when API returns player info"""
    name: str
    email: EmailStr

    class Config:
        orm_mode: True
