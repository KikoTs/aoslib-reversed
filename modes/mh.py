import asyncio
import random
from typing import List, Tuple

from shared import constants
from modes import GameMode
from server import types, util
from server.protocol import ServerProtocol
from server.connection import ServerConnection
from server.loaders import progress_bar


DEFAULT_HILL_RADIUS = 16
DEFAULT_CAPTURE_RATE = 0.1
DEFAULT_HILL_COUNT = 3
DEFAULT_SCORE_LIMIT = 100


class Hill(types.Entity):
    on_capture = util.AsyncEvent()

    def __init__(self, *args, capture_radius=None, capture_rate=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.team = None
        self.controlling_players = []
        self.capture_radius = capture_radius or DEFAULT_HILL_RADIUS
        self.capture_rate = capture_rate or DEFAULT_CAPTURE_RATE
        self.control_points = 0
        self.indicator = self.protocol.create_entity(types.CommandPost, position=self.position, team=None)

    def update(self, dt):
        if self.destroyed:
            return
        self.check_players()
        team1_count = sum(1 for p in self.controlling_players if p.team is self.protocol.team1)
        team2_count = sum(1 for p in self.controlling_players if p.team is self.protocol.team2)
        
        # Determine which team controls the hill
        if team1_count > team2_count:
            new_team = self.protocol.team1
        elif team2_count > team1_count:
            new_team = self.protocol.team2
        else:
            new_team = None
            
        # If control changed
        if new_team != self.team:
            self.team = new_team
            self.indicator.set_team(new_team)
            if new_team:
                self.protocol.loop.create_task(self.on_capture(self, new_team))
        
        # Award points to controlling team
        if self.team:
            self.control_points += dt
            if self.control_points >= 1:
                points_to_award = int(self.control_points)
                self.team.score += points_to_award
                self.control_points -= points_to_award

    def check_players(self):
        old_players = self.controlling_players.copy()
        self.controlling_players.clear()
        
        for player in self.protocol.players.values():
            if player.dead:
                continue
                
            dist = self.position.sq_distance(player.position)
            if dist <= self.capture_radius ** 2:
                self.controlling_players.append(player)
                
        if self.controlling_players != old_players:
            grid = self.protocol.map.to_grid(self.position.x, self.position.y)
            if not old_players and self.controlling_players:
                self.protocol.broadcast_hud_message(f"Players entering hill at {grid}")

    def destroy(self):
        self.indicator.destroy()
        super().destroy()


class MultiHill(GameMode):
    id = constants.MODE.MULTIHILL.value 
    name = "Multi Hill"

    title = "MULTIHILL_TITLE"
    description_key = "MULTIHILL_DESCRIPTION"
    info_text1 = ""
    info_text2 = ""
    info_text3 = ""

    @property
    def description(self):
        return f"""Control the hills to earn points for your team.
More players on a hill means faster control.

First team to reach {self.score_limit} points wins!
"""

    short_name = "mh"

    @property
    def score_limit(self):
        return self.config.get("score_limit", DEFAULT_SCORE_LIMIT)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hills: List[Hill] = []
        Hill.on_capture += self.on_hill_captured

    def start(self):
        super().start()
        self.spawn_hills()
        self.protocol.team1.score = 0
        self.protocol.team2.score = 0

    def stop(self):
        super().stop()
        for hill in self.hills:
            hill.destroy()
        self.hills.clear()

    def spawn_hills(self):
        map_width = self.protocol.map.width()
        map_height = self.protocol.map.length()
        hill_count = self.config.get("hill_count", DEFAULT_HILL_COUNT)
        
        # Create hills in strategic locations
        for i in range(hill_count):
            # Center hill
            if i == 0 and hill_count > 1:
                x = map_width // 2
                y = map_height // 2
                position = types.Position(x, y, 0)
            # Other hills distributed around the map
            else:
                segment = 2 * 3.14159 * i / hill_count
                radius = min(map_width, map_height) * 0.35
                x = map_width // 2 + int(radius * util.math.cos(segment))
                y = map_height // 2 + int(radius * util.math.sin(segment))
                position = types.Position(x, y, 0)
            
            hill = self.protocol.create_entity(
                Hill, 
                position=position,
                capture_radius=self.config.get("capture_radius"),
                capture_rate=self.config.get("capture_rate")
            )
            self.hills.append(hill)

    async def on_hill_captured(self, hill: Hill, team: types.Team):
        if not team:
            self.protocol.broadcast_hud_message(f"Hill has been neutralized")
        else:
            grid = self.protocol.map.to_grid(hill.position.x, hill.position.y)
            self.protocol.broadcast_hud_message(f"{team.name} team now controls hill at {grid}")
        self.check_win()

    def check_win(self):
        if self.protocol.team1.score >= self.score_limit:
            self.end_game(self.protocol.team1)
        elif self.protocol.team2.score >= self.score_limit:
            self.end_game(self.protocol.team2)

    def get_spawn_point(self, player: ServerConnection) -> Tuple[int, int, int]:
        # Find hills controlled by player's team
        team_hills = [h for h in self.hills if h.team is player.team]
        
        # If team controls hills, spawn near one
        if team_hills:
            hill = random.choice(team_hills)
            x, y = hill.position.x, hill.position.y
            angle = random.random() * 2 * 3.14159
            distance = random.randint(30, 50)  # Not too close but not too far
            spawn_x = x + int(distance * util.math.cos(angle))
            spawn_y = y + int(distance * util.math.sin(angle))
            spawn_x = max(0, min(self.protocol.map.width() - 1, spawn_x))
            spawn_y = max(0, min(self.protocol.map.length() - 1, spawn_y))
            z = self.protocol.map.get_z(spawn_x, spawn_y)
            return spawn_x + 0.5, spawn_y + 0.5, z - 2
        
        # Otherwise use default spawn
        return super().get_spawn_point(player)


def init(protocol: ServerProtocol):
    return MultiHill(protocol)
