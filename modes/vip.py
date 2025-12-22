import random
from typing import Dict, List, Tuple, Optional

from shared import constants
from shared.constants import KILL
from modes import GameMode
from server import types, util
from server.protocol import ServerProtocol
from server.connection import ServerConnection


DEFAULT_SCORE_LIMIT = 3
DEFAULT_VIP_HEALTH_MULTIPLIER = 2.0
DEFAULT_ROUND_TIME = 300  # 5 minutes


class VIPMode(GameMode):
    id = constants.MODE.VIP.value   
    name = "VIP"
    
    title = "VIP_MODE_TITLE"
    description_key = "VIP_MODE_DESCRIPTION"
    info_text1 = "VIP_INFOGRAPHIC_TEXT1"
    info_text2 = "VIP_INFOGRAPHIC_TEXT2"
    info_text3 = "VIP_INFOGRAPHIC_TEXT3"
    
    @property
    def description(self):
        return f"""Each team has a VIP that must be protected at all costs. 
Your team scores when the enemy VIP is eliminated.
        
First team to eliminate the enemy VIP {self.score_limit} times wins!
"""
    
    short_name = "vip"
    
    @property
    def score_limit(self):
        return self.config.get("score_limit", DEFAULT_SCORE_LIMIT)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vips: Dict[types.Team, ServerConnection] = {}
        self.round_time = self.config.get("round_time", DEFAULT_ROUND_TIME)
        self.round_end_time = 0
        self.vip_health_multiplier = self.config.get("vip_health_multiplier", DEFAULT_VIP_HEALTH_MULTIPLIER)
        self.round_in_progress = False
        
        # Add extra handlers
        ServerConnection.on_player_disconnect += self.on_player_disconnect
        
    def start(self):
        super().start()
        
        # Reset scores
        self.protocol.team1.score = 0
        self.protocol.team2.score = 0
        
        # Start first round
        self.start_new_round()
        
    def stop(self):
        super().stop()
        self.vips.clear()
        self.round_in_progress = False
        
    def start_new_round(self):
        """Start a new round with new VIPs"""
        # Clear previous VIPs
        self.vips.clear()
        
        # Select new VIPs from each team if possible
        team1_players = [p for p in self.protocol.players.values() if p.team is self.protocol.team1]
        team2_players = [p for p in self.protocol.players.values() if p.team is self.protocol.team2]
        
        if team1_players and team2_players:
            # Randomly select VIPs
            vip1 = random.choice(team1_players)
            vip2 = random.choice(team2_players)
            
            self.vips[self.protocol.team1] = vip1
            self.vips[self.protocol.team2] = vip2
            
            # Announce VIPs
            self.protocol.broadcast_hud_message(f"{vip1} is the {self.protocol.team1.name} team VIP!")
            self.protocol.broadcast_hud_message(f"{vip2} is the {self.protocol.team2.name} team VIP!")
            
            # Apply VIP effects
            for vip in self.vips.values():
                vip.max_hp = int(100 * self.vip_health_multiplier)
                vip.hp = vip.max_hp
                vip.restock()
                
            # Set round timer
            self.round_end_time = self.protocol.time + self.round_time
            self.round_in_progress = True
        else:
            # Not enough players
            self.protocol.broadcast_hud_message("Waiting for players to join both teams...")
            self.round_in_progress = False
    
    def is_vip(self, player: ServerConnection) -> bool:
        """Check if a player is a VIP"""
        return player in self.vips.values()
    
    def get_team_vip(self, team: types.Team) -> Optional[ServerConnection]:
        """Get the VIP for a specific team"""
        return self.vips.get(team)
    
    async def on_player_disconnect(self, player: ServerConnection):
        """Handle a player disconnecting - if they're a VIP, select a new one"""
        for team, vip in list(self.vips.items()):
            if vip is player:
                # VIP disconnected, select a new one
                team_players = [p for p in self.protocol.players.values() 
                               if p.team is team and p is not player]
                
                if team_players:
                    new_vip = random.choice(team_players)
                    self.vips[team] = new_vip
                    
                    # Announce new VIP
                    self.protocol.broadcast_hud_message(f"{new_vip} is the new {team.name} team VIP!")
                    
                    # Apply VIP effects
                    new_vip.max_hp = int(100 * self.vip_health_multiplier)
                    new_vip.hp = new_vip.max_hp
                    new_vip.restock()
                else:
                    # No more players on this team
                    self.vips.pop(team)
                    # Award win to the other team
                    other_team = self.protocol.team2 if team is self.protocol.team1 else self.protocol.team1
                    self.end_game(other_team)
                    
    async def on_player_kill(self, player: ServerConnection, kill_type: KILL, killer: ServerConnection, respawn_time: int):
        await super().on_player_kill(player, kill_type, killer, respawn_time)
        
        # Check if killed player was a VIP
        if self.is_vip(player):
            # Find which team this VIP belongs to
            for team, vip in self.vips.items():
                if vip is player:
                    # Enemy team scores a point
                    enemy_team = self.protocol.team2 if team is self.protocol.team1 else self.protocol.team1
                    enemy_team.score += 1
                    
                    # Announce VIP killed
                    if killer:
                        self.protocol.broadcast_hud_message(f"{killer} eliminated the {team.name} team VIP!")
                        killer.score += 10  # Bonus points for killing VIP
                    else:
                        self.protocol.broadcast_hud_message(f"The {team.name} team VIP has been eliminated!")
                    
                    # Check win condition
                    if enemy_team.score >= self.score_limit:
                        self.end_game(enemy_team)
                    else:
                        # Start new round
                        self.protocol.broadcast_hud_message(f"Round over! Next round starting soon...")
                        self.protocol.loop.call_later(5, self.start_new_round)
                        
                    break
                    
    def update(self, dt):
        super().update(dt)
        
        # Check round timer
        if self.round_in_progress and self.protocol.time >= self.round_end_time:
            # Round time expired
            self.protocol.broadcast_hud_message("Round time expired! It's a draw!")
            
            # Start new round
            self.protocol.loop.call_later(5, self.start_new_round)
            self.round_in_progress = False
            
    def get_spawn_point(self, player: ServerConnection) -> Tuple[int, int, int]:
        """Get spawn point based on team"""
        map_width = self.protocol.map.width()
        map_height = self.protocol.map.length()
        
        if player.team is self.protocol.team1:
            # Team 1 spawns on left side
            x = random.randint(0, int(map_width * 0.25))
            y = random.randint(0, map_height)
        else:
            # Team 2 spawns on right side
            x = random.randint(int(map_width * 0.75), map_width - 1)
            y = random.randint(0, map_height)
            
        z = self.protocol.map.get_z(x, y)
        return x + 0.5, y + 0.5, z - 2


def init(protocol: ServerProtocol):
    return VIPMode(protocol)
