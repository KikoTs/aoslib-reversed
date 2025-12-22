import random
from typing import Dict, List, Tuple

from shared import constants
from shared.constants import KILL
from modes import GameMode
from server import types
from server.protocol import ServerProtocol
from server.connection import ServerConnection


class CCTF(GameMode):
    id = constants.MODE.CCTF.value  
    name = "Classic Capture the Flag"

    title = "CTF_TITLE"
    description_key = "CTF_DESCRIPTION"
    info_text1 = "CTF_INFOGRAPHIC_TEXT1"
    info_text2 = "CTF_INFOGRAPHIC_TEXT2"
    info_text3 = "CTF_INFOGRAPHIC_TEXT3"

    @property
    def description(self):
        return f"""Capture the enemy flag and return it to your base, but your team's flag must be at your base to score.
Dropped flags return to base after 30 seconds.

First team to capture {self.score_limit} flags wins.
"""

    short_name = "cctf"
    
    @property
    def score_limit(self):
        return self.config.get("score_limit", 5)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.team1_flag = None
        self.team2_flag = None
        self.team1_base = None
        self.team2_base = None
        self.flag_drop_times = {}
        self.flag_return_delay = 30  # seconds

        self.pickup_sound = self.protocol.create_sound("pickup")
        self.capture_sound = self.protocol.create_sound("deposit")
        
        # Register event handlers
        ServerConnection.on_player_disconnect += self.on_player_disconnect
        types.Flag.on_collide += self.on_flag_collide
        types.CommandPost.on_collide += self.on_base_collide

    def start(self):
        super().start()
        
        # Get team base positions
        team1_pos = self.get_base_position(self.protocol.team1)
        team2_pos = self.get_base_position(self.protocol.team2)
        
        # Create flags at team bases
        self.team1_flag = self.protocol.create_entity(types.Flag, position=team1_pos, team=self.protocol.team1, color=self.protocol.team1.color)
        self.team2_flag = self.protocol.create_entity(types.Flag, position=team2_pos, team=self.protocol.team2, color=self.protocol.team2.color)
        
        # Create team bases (capture points)
        self.team1_base = self.protocol.create_entity(types.CommandPost, position=team1_pos, team=self.protocol.team1)
        self.team2_base = self.protocol.create_entity(types.CommandPost, position=team2_pos, team=self.protocol.team2)
        
        # Reset scores
        self.protocol.team1.score = 0
        self.protocol.team2.score = 0

    def stop(self):
        super().stop()
        
        # Clean up entities
        if self.team1_flag:
            self.team1_flag.destroy()
        if self.team2_flag:
            self.team2_flag.destroy()
        if self.team1_base:
            self.team1_base.destroy()
        if self.team2_base:
            self.team2_base.destroy()

    def get_base_position(self, team: types.Team) -> types.Position:
        """Get position for team's base"""
        map_width = self.protocol.map.width()
        map_height = self.protocol.map.length()
        
        if team is self.protocol.team1:
            # Team 1 base on left side
            x = int(map_width * 0.1)
            y = int(map_height * 0.5)
        else:
            # Team 2 base on right side
            x = int(map_width * 0.9)
            y = int(map_height * 0.5)
            
        return types.Position(x, y, 0)

    def on_flag_collide(self, flag: types.Flag, player: ServerConnection):
        """Handle player colliding with a flag"""
        # Can't pick up your own flag unless it's dropped
        if flag.team is player.team:
            if flag.carrier is None and flag.position != self.get_base_position(flag.team):
                # Return dropped flag to base
                self.return_flag(flag)
                self.protocol.broadcast_hud_message(f"{player} returned the {flag.team.name} flag!")
            return
            
        # Can't pick up enemy flag if your flag is not at base
        team_flag = self.team1_flag if player.team is self.protocol.team1 else self.team2_flag
        if team_flag.carrier is not None or team_flag.position != self.get_base_position(team_flag.team):
            self.protocol.broadcast_hud_message(f"You cannot take the enemy flag until your flag is at base!", connections=[player])
            return
            
        # Pick up enemy flag
        flag.set_carrier(player)
        self.protocol.broadcast_hud_message(f"{player} has the {flag.team.name} flag!")
        
        # Play pickup sound
        self.pickup_sound.position = player.position
        self.pickup_sound.play()
        
        # Remove from drop tracking if was dropped
        if flag in self.flag_drop_times:
            del self.flag_drop_times[flag]

    def on_base_collide(self, base: types.CommandPost, player: ServerConnection):
        """Handle player colliding with a base"""
        if base.team is not player.team:
            return
            
        # Find which flag player is carrying
        carrying_flag = None
        if self.team1_flag.carrier is player:
            carrying_flag = self.team1_flag
        elif self.team2_flag.carrier is player:
            carrying_flag = self.team2_flag
            
        if carrying_flag is None:
            # Restock player when at base
            if self.protocol.time - player.store.get("cctf_last_restock", 0) >= 3:
                player.restock()
                player.store["cctf_last_restock"] = self.protocol.time
            return
            
        # Can only capture if your team's flag is at base
        team_flag = self.team1_flag if player.team is self.protocol.team1 else self.team2_flag
        if team_flag.carrier is not None or team_flag.position != self.get_base_position(team_flag.team):
            self.protocol.broadcast_hud_message(f"You cannot capture until your flag is at base!", connections=[player])
            return
            
        # Capture the flag
        self.capture_flag(player, carrying_flag)

    def capture_flag(self, player: ServerConnection, flag: types.Flag):
        """Process flag capture"""
        # Reset flag
        flag.set_carrier(None)
        flag.set_position(*self.get_base_position(flag.team).xyz)
        
        # Award points
        player.team.score += 1
        player.score += 10
        
        # Broadcast capture
        self.protocol.broadcast_hud_message(f"{player} captured the {flag.team.name} flag!")
        
        # Play capture sound
        self.capture_sound.position = player.position
        self.capture_sound.play()
        
        # Check win condition
        self.check_win()

    def check_win(self):
        """Check if a team has reached score limit"""
        if self.protocol.team1.score >= self.score_limit:
            self.end_game(self.protocol.team1)
        elif self.protocol.team2.score >= self.score_limit:
            self.end_game(self.protocol.team2)

    def return_flag(self, flag: types.Flag):
        """Return a flag to its base"""
        flag.set_carrier(None)
        flag.set_position(*self.get_base_position(flag.team).xyz)
        
        # Remove from drop tracking
        if flag in self.flag_drop_times:
            del self.flag_drop_times[flag]

    def drop_flag(self, player: ServerConnection):
        """Drop flag if player is carrying one"""
        for flag in [self.team1_flag, self.team2_flag]:
            if flag.carrier is player:
                flag.set_carrier(None)
                flag.set_position(*player.position.xyz)
                
                # Track drop time for auto-return
                self.flag_drop_times[flag] = self.protocol.time
                
                # Announce drop
                self.protocol.broadcast_hud_message(f"{player} dropped the {flag.team.name} flag!")
                break

    async def on_player_disconnect(self, player: ServerConnection):
        """Handle player disconnect - drop flag if carrying"""
        self.drop_flag(player)

    async def on_player_kill(self, player: ServerConnection, kill_type: KILL, killer: ServerConnection, respawn_time: int):
        await super().on_player_kill(player, kill_type, killer, respawn_time)
        
        # Drop flag if carrying
        self.drop_flag(player)
        
        # Award bonus points for killing flag carrier
        if killer and killer != player and killer.team is not player.team:
            if self.team1_flag.carrier is player or self.team2_flag.carrier is player:
                killer.score += 3
                self.protocol.broadcast_hud_message(f"{killer} killed enemy flag carrier!")

    def update(self, dt):
        super().update(dt)
        
        # Check for auto flag returns
        current_time = self.protocol.time
        for flag, drop_time in list(self.flag_drop_times.items()):
            if current_time - drop_time >= self.flag_return_delay:
                self.return_flag(flag)
                self.protocol.broadcast_hud_message(f"The {flag.team.name} flag has been returned to base!")

    def get_spawn_point(self, player: ServerConnection) -> Tuple[int, int, int]:
        """Get spawn point near team's base"""
        if player.team is self.protocol.team1:
            base_pos = self.get_base_position(self.protocol.team1)
        else:
            base_pos = self.get_base_position(self.protocol.team2)
            
        # Spawn in radius around base
        angle = random.random() * 2 * 3.14159
        distance = random.randint(5, 15)  # Not too far from base
        spawn_x = base_pos.x + int(distance * util.math.cos(angle)) if hasattr(util, "math") else base_pos.x + distance
        spawn_y = base_pos.y + int(distance * util.math.sin(angle)) if hasattr(util, "math") else base_pos.y
        spawn_x = max(0, min(self.protocol.map.width() - 1, spawn_x))
        spawn_y = max(0, min(self.protocol.map.length() - 1, spawn_y))
        z = self.protocol.map.get_z(spawn_x, spawn_y)
        
        return spawn_x + 0.5, spawn_y + 0.5, z - 2


def init(protocol: ServerProtocol):
    return CCTF(protocol)
