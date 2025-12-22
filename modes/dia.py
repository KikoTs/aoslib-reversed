import asyncio
import random
from typing import Dict, List, Tuple

from shared import constants
from modes import GameMode
from server import types, util
from server.protocol import ServerProtocol
from server.connection import ServerConnection


DEFAULT_DIAMOND_COUNT = 10
DEFAULT_SCORE_LIMIT = 10
DEFAULT_RESPAWN_TIME = 15


class Diamond(types.Entity):
    on_pickup = util.AsyncEvent()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.carrier = None
        self.indicator = self.protocol.create_entity(types.Flag, position=self.position, team=None)
        
    def update(self, dt):
        if self.destroyed:
            return
        self.do_gravity()
        
        # Check for player collisions if not carried
        if self.carrier is None:
            for player in self.protocol.players.values():
                if player.dead:
                    continue
                    
                if self.position.sq_distance(player.position) <= 9:  # 3 blocks radius
                    self.protocol.loop.create_task(self.on_pickup(self, player))
                    self.set_carrier(player)
                    break
    
    def set_carrier(self, player: ServerConnection):
        self.carrier = player
        if player is not None:
            self.indicator.set_carrier(player)
        else:
            self.indicator.set_carrier(None)
            
    def set_position(self, x, y, z):
        super().set_position(x, y, z)
        self.indicator.set_position(x, y, z)
        
    def destroy(self):
        self.indicator.destroy()
        super().destroy()


class Base(types.CommandPost):
    on_diamond_deposit = util.AsyncEvent()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def update(self, dt):
        if self.destroyed:
            return
        self.do_gravity()
        
        # Check for players with diamonds
        for player in self.protocol.players.values():
            if player.dead or player.team is not self.team:
                continue
                
            if self.position.sq_distance(player.position) <= 16:  # 4 blocks radius
                # Check if player has diamonds
                game_mode = self.protocol.game_mode
                if isinstance(game_mode, DiamondMine):
                    diamonds = game_mode.player_diamonds.get(player, [])
                    if diamonds:
                        for diamond in diamonds[:]:
                            self.protocol.loop.create_task(self.on_diamond_deposit(self, player, diamond))
                            game_mode.deposit_diamond(player, diamond)


class DiamondMine(GameMode):
    id = constants.MODE.DIAMONDMINE.value 
    name = "Diamond Mine"
    
    title = "DIAMOND_MINE_TITLE"
    description_key = "DIAMOND_MINE_DESCRIPTION"
    info_text1 = "DIA_INFOGRAPHIC_TEXT1"
    info_text2 = "DIA_INFOGRAPHIC_TEXT2"
    info_text3 = "DIA_INFOGRAPHIC_TEXT3"
    
    @property
    def description(self):
        return f"""Mine and collect diamonds from around the map, then return them to your base.
Watch out for enemy players who will try to steal your hard-earned diamonds!
        
First team to collect {self.score_limit} diamonds wins!
"""
    
    short_name = "dia"
    
    @property
    def score_limit(self):
        return self.config.get("score_limit", DEFAULT_SCORE_LIMIT)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.diamonds: List[Diamond] = []
        self.diamond_spawn_points = []
        self.player_diamonds: Dict[ServerConnection, List[Diamond]] = {}
        
        Diamond.on_pickup += self.on_diamond_pickup
        Base.on_diamond_deposit += self.on_diamond_deposit
        ServerConnection.on_player_disconnect += self.on_player_disconnect
        
        self.pickup_sound = self.protocol.create_sound("pickup")
        self.deposit_sound = self.protocol.create_sound("deposit")
        
    def start(self):
        super().start()
        
        # Create team bases
        team1_pos = self.get_team_position(self.protocol.team1)
        team2_pos = self.get_team_position(self.protocol.team2)
        
        self.team1_base = self.protocol.create_entity(Base, position=team1_pos, team=self.protocol.team1)
        self.team2_base = self.protocol.create_entity(Base, position=team2_pos, team=self.protocol.team2)
        
        # Generate diamond spawn points
        self.generate_diamond_spawn_points()
        
        # Spawn initial diamonds
        self.spawn_diamonds()
        
        # Reset scores
        self.protocol.team1.score = 0
        self.protocol.team2.score = 0
        
    def stop(self):
        super().stop()
        
        # Clean up diamonds
        for diamond in self.diamonds:
            diamond.destroy()
        self.diamonds.clear()
        
        # Clean up bases
        self.team1_base.destroy()
        self.team2_base.destroy()
        
        # Clear player diamonds
        self.player_diamonds.clear()
        
    def get_team_position(self, team: types.Team) -> types.Position:
        """Get a position for team's base"""
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
        
    def generate_diamond_spawn_points(self):
        """Generate potential spawn points for diamonds"""
        map_width = self.protocol.map.width()
        map_height = self.protocol.map.length()
        
        # Clear existing points
        self.diamond_spawn_points.clear()
        
        # Generate points in middle area of map
        for _ in range(30):
            x = random.randint(int(map_width * 0.3), int(map_width * 0.7))
            y = random.randint(int(map_height * 0.3), int(map_height * 0.7))
            self.diamond_spawn_points.append((x, y))
            
    def spawn_diamonds(self):
        """Spawn diamonds around the map"""
        diamond_count = self.config.get("diamond_count", DEFAULT_DIAMOND_COUNT)
        
        # Limit to available spawn points
        count = min(diamond_count, len(self.diamond_spawn_points))
        
        # Select random spawn points
        spawn_points = random.sample(self.diamond_spawn_points, count)
        
        for x, y in spawn_points:
            z = self.protocol.map.get_z(x, y)
            position = types.Position(x, y, z)
            diamond = self.protocol.create_entity(Diamond, position=position)
            self.diamonds.append(diamond)
            
    async def respawn_diamond(self, diamond: Diamond):
        """Respawn a diamond after some time"""
        await asyncio.sleep(self.config.get("diamond_respawn_time", DEFAULT_RESPAWN_TIME))
        
        if self.diamonds and diamond in self.diamonds:
            # Choose a new spawn point
            if self.diamond_spawn_points:
                x, y = random.choice(self.diamond_spawn_points)
                z = self.protocol.map.get_z(x, y)
                diamond.set_position(x, y, z)
                diamond.set_carrier(None)
                
    async def on_diamond_pickup(self, diamond: Diamond, player: ServerConnection):
        """Handle a player picking up a diamond"""
        if diamond not in self.diamonds:
            return
            
        self.protocol.broadcast_hud_message(f"{player} found a diamond!")
        
        # Add to player's diamonds
        if player not in self.player_diamonds:
            self.player_diamonds[player] = []
        self.player_diamonds[player].append(diamond)
        
        # Play pickup sound
        self.pickup_sound.position = player.position
        await self.pickup_sound.play()
        
    async def on_diamond_deposit(self, base: Base, player: ServerConnection, diamond: Diamond):
        """Handle a player depositing a diamond at their base"""
        grid = self.protocol.map.to_grid(base.position.x, base.position.y)
        self.protocol.broadcast_hud_message(f"{player} delivered a diamond to {grid}!")
        
        # Play deposit sound
        self.deposit_sound.position = base.position
        await self.deposit_sound.play()
        
    def deposit_diamond(self, player: ServerConnection, diamond: Diamond):
        """Process a diamond deposit"""
        # Remove from player
        if player in self.player_diamonds and diamond in self.player_diamonds[player]:
            self.player_diamonds[player].remove(diamond)
            
        # Add to team score
        player.team.score += 1
        player.score += 5
        
        # Prepare to respawn diamond
        self.protocol.loop.create_task(self.respawn_diamond(diamond))
        
        # Check for win
        self.check_win()
        
    async def on_player_disconnect(self, player: ServerConnection):
        """Handle player disconnect - drop their diamonds"""
        if player in self.player_diamonds:
            diamonds = self.player_diamonds[player]
            for diamond in diamonds:
                diamond.set_carrier(None)
                diamond.set_position(*player.position.xyz)
            self.player_diamonds.pop(player)
            
    async def on_player_kill(self, player: ServerConnection, kill_type, killer, respawn_time):
        await super().on_player_kill(player, kill_type, killer, respawn_time)
        
        # Drop diamonds when player dies
        if player in self.player_diamonds:
            diamonds = self.player_diamonds[player]
            for diamond in diamonds:
                diamond.set_carrier(None)
                diamond.set_position(*player.position.xyz)
                
                # Notify if killer gets diamonds
                if killer and killer != player:
                    self.protocol.broadcast_hud_message(f"{killer} stole a diamond from {player}!")
                    
            self.player_diamonds.pop(player)
            
    def get_spawn_point(self, player: ServerConnection) -> Tuple[int, int, int]:
        """Get spawn point near player's base"""
        if player.team is self.protocol.team1:
            base = self.team1_base
        else:
            base = self.team2_base
            
        # Spawn in radius around base
        angle = random.random() * 2 * 3.14159
        distance = random.randint(10, 20)
        spawn_x = base.position.x + int(distance * util.math.cos(angle))
        spawn_y = base.position.y + int(distance * util.math.sin(angle))
        spawn_x = max(0, min(self.protocol.map.width() - 1, spawn_x))
        spawn_y = max(0, min(self.protocol.map.length() - 1, spawn_y))
        z = self.protocol.map.get_z(spawn_x, spawn_y)
        
        return spawn_x + 0.5, spawn_y + 0.5, z - 2


def init(protocol: ServerProtocol):
    return DiamondMine(protocol)
