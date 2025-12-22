import random
from typing import List, Tuple

from shared import constants
from shared.constants import KILL
from modes import GameMode
from server import types
from server.protocol import ServerProtocol
from server.connection import ServerConnection


DEFAULT_SCORE_LIMIT = 50
DEFAULT_KILL_POINTS = 1


class TDM(GameMode):
    id = constants.MODE.TDM.value
    name = "Team Deathmatch"
    
    title = "TDM_TITLE"
    description_key = "TDM_DESCRIPTION"
    info_text1 = "TDM_INFOGRAPHIC_TEXT1"
    info_text2 = "TDM_INFOGRAPHIC_TEXT2"
    info_text3 = "TDM_INFOGRAPHIC_TEXT3"
    
    @property
    def description(self):
        return f"""Eliminate players from the enemy team to score points.
Teamwork is essential for victory!
        
First team to reach {self.score_limit} kills wins.
"""
    
    short_name = "tdm"
    
    @property
    def score_limit(self):
        return self.config.get("score_limit", DEFAULT_SCORE_LIMIT)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.spawn_points_team1 = []
        self.spawn_points_team2 = []
        self.kill_points = self.config.get("kill_points", DEFAULT_KILL_POINTS)
        
    def start(self):
        super().start()
        self.generate_spawn_points()
        
        # Reset team scores
        self.protocol.team1.score = 0
        self.protocol.team2.score = 0
        
        # Reset player scores
        for player in self.protocol.players.values():
            player.score = 0
            
    def generate_spawn_points(self):
        """Generate team-specific spawn points"""
        map_width = self.protocol.map.width()
        map_height = self.protocol.map.length()
        
        # Clear existing spawn points
        self.spawn_points_team1.clear()
        self.spawn_points_team2.clear()
        
        # Team 1 spawns on left side
        for _ in range(10):
            x = random.randint(0, int(map_width * 0.3))
            y = random.randint(0, map_height)
            z = self.protocol.map.get_z(x, y)
            self.spawn_points_team1.append((x, y, z))
            
        # Team 2 spawns on right side
        for _ in range(10):
            x = random.randint(int(map_width * 0.7), map_width)
            y = random.randint(0, map_height)
            z = self.protocol.map.get_z(x, y)
            self.spawn_points_team2.append((x, y, z))
            
    async def on_player_kill(self, player: ServerConnection, kill_type: KILL, killer: ServerConnection, respawn_time: int):
        await super().on_player_kill(player, kill_type, killer, respawn_time)
        
        # Award points for kills
        if killer and killer != player and killer.team != player.team:
            killer.team.score += self.kill_points
            killer.score += self.kill_points
            
            # Broadcast kill message
            self.protocol.broadcast_hud_message(f"{killer} eliminated {player}")
            
            # Check for win condition
            self.check_win()
            
    def check_win(self):
        """Check if a team has reached the score limit"""
        if self.protocol.team1.score >= self.score_limit:
            self.end_game(self.protocol.team1)
        elif self.protocol.team2.score >= self.score_limit:
            self.end_game(self.protocol.team2)
            
    def get_spawn_point(self, player: ServerConnection) -> Tuple[int, int, int]:
        """Get a spawn point for the player based on their team"""
        if player.team is self.protocol.team1:
            if not self.spawn_points_team1:
                return super().get_spawn_point(player)
            x, y, z = random.choice(self.spawn_points_team1)
        else:
            if not self.spawn_points_team2:
                return super().get_spawn_point(player)
            x, y, z = random.choice(self.spawn_points_team2)
            
        return x + 0.5, y + 0.5, z - 2


def init(protocol: ServerProtocol):
    return TDM(protocol)
