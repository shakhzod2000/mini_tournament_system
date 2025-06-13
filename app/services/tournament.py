from app.repositories.tournament import TournamentRepository


class TournamentService:
    def __init__(self, repo: TournamentRepository):
        self.repo = repo

    async def create_tournament(self, data):
        return await self.repo.create_tournament(**data.dict())
    
    async def register_player(self, tournament_id, player_data):
        return await self.repo.register_player(tournament_id, player_data.name, player_data.email)
    
    async def list_players(self, tournament_id):
        return await self.repo.get_players(tournament_id)
    
    async def get_tournament_info(self, tournament_id):
        tournament = await self.repo.get_tournament(tournament_id)
        count = await self.repo.count_registered(tournament_id)

        return {
            'id': tournament.id,
            'name': tournament.name,
            'max_players': tournament.max_players,
            'start_at': tournament.start_at,
            'registered_players': count
        }
