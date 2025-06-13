from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.tournament import Tournament, Player


class TournamentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_tournament(self, name, max_players, start_at):
        tournament = Tournament(name=name, max_players=max_players, start_at=start_at)
        self.db.add(tournament)
        await self.db.commit()
        await self.db.refresh(tournament)
        return tournament

    async def get_tournament(self, tournament_id: int):
        result = await self.db.execute(select(Tournament).where(Tournament.id == tournament_id))
        # get one row or none with .scalar_one_or_none()
        return result.scalar_one_or_none()

    async def count_registered(self, tournament_id: int):
        result = await self.db.execute(
            select(func.count(Player.id)).where(Player.tournament_id == tournament_id)
        )
        # get 1st col of 1st row with .scalar()
        return result.scalar()

    async def register_player(self, tournament_id: int, name: str, email: str):
        existing = self.db.execute(
            select(Player).where(Player.tournament_id == tournament_id, Player.email == email)
        )
        if existing.scalar():
            raise ValueError('Player with this email already registered.')
        
        registered_count = await self.count_registered(tournament_id)
        tournament = await self.get_tournament(tournament_id)

        if registered_count >= tournament.max_players:
            raise ValueError('Tournament is full.')
        
        player = Player(name=name, email=email, tournament_id=tournament_id)
        self.db.add(player)
        await self.db.commit()
        await self.db.refresh(player)
        return player

    async def get_players(self, tournament_id: int):
        result = await self.db.execute(
            select(Player).where(Player.tournament_id == tournament_id)
        )
        # get multiple rows(list of ORM objects)
        return result.scalars().all()
