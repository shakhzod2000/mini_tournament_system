from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Base


class Tournament(Base):
    __tablename__ = 'tournaments'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    max_players: Mapped[int]
    start_at: Mapped[datetime] = mapped_column(DateTime)
    players: Mapped[list['Player']] = relationship(back_populates='tournament')


class Player(Base):
    __tablename__ = 'players'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100))
    tournament_id: Mapped[int] = mapped_column(ForeignKey('tournaments.id'))
    tournament: Mapped['Tournament'] = relationship(back_populates='players')
