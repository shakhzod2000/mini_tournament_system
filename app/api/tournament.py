from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.tournament import TournamentCreate, TournamentOut, PlayerCreate, PlayerOut
from app.db import async_session
from app.repositories.tournament import TournamentRepository
from app.services.tournament import TournamentService


router = APIRouter()

async def get_service(db: AsyncSession = Depends(async_session)):
    repo = TournamentRepository(db)
    return TournamentService(repo)


@router.post('/tournaments', response_model=TournamentOut)
async def create_tournament(data: TournamentCreate, service: TournamentService = Depends(get_service)):
    tournament = await service.create_tournament(data)
    return await service.get_tournament_info(tournament.id)


@router.post('/tournaments/{tournament_id}/register', response_model=PlayerOut)
async def register(tournament_id: int, player: PlayerCreate, service: TournamentService = Depends(get_service)):
    try:
        return await service.register_player(tournament_id, player)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/tournaments/{tournament_id}/players', response_model=list[PlayerOut])
async def list_players(tournament_id: int, service: TournamentService = Depends(get_service)):
    return await service.list_players(tournament_id)
