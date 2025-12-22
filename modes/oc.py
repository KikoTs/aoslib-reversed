import random
from typing import Dict, List, Tuple

from shared import constants
from modes import GameMode
from server import types, util
from server.protocol import ServerProtocol
from server.connection import ServerConnection
from server.loaders import progress_bar


DEFAULT_CAPTURE_DISTANCE = 16
DEFAULT_CAPTURE_RATE = 0.05
DEFAULT_SCORE_LIMIT = 300
DEFAULT_SECTOR_COUNT = 5


class Sector(types.CommandPost):
    on_capture = util.AsyncEvent()
    
    def __init__(self, *args, capture_radius=None, capture_rate=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._progress = float(self.team.id) if self.team is not None else 0.5
        self._rate = 0
        self.players = []
        self.control_time = 0
        
        self.capture_radius = capture_radius or DEFAULT_CAPTURE_DISTANCE
        self.capture_rate = capture_rate or DEFAULT_CAPTURE_RATE
        
    def update(self, dt):
        if self.destroyed:
            return
        self.do_gravity()
        self.get_players()
        
        if self.team is not None:
            self.control_time += dt
            if self.control_time >= 1:
                points = int(self.control_time)
                self.team.score += points
                self.control_time -= points
        
        self.progress += self.rate * dt
    
    def get_players(self):
        old = self.players.copy()
        self.players.clear()
        
        for player in self.protocol.players.values():
            if player.dead:
                continue
                
            dist = self.position.sq_distance(player.position)
            if dist <= self.capture_radius ** 2:
                self.players.append(player)
                
        # Update progress bar when players change
        if self.players != old:
            left = set(old) - set(self.players)
            progress_bar.stopped = True
            self.protocol.broadcast_loader(progress_bar, connections=left)
            
            if not old and self.players:
                grid = self.protocol.map.to_grid(self.position.x, self.position.y)
                self.protocol.broadcast_hud_message(f"Players entering sector {grid}")
    
    @property
    def progress(self):
        return self._progress
    
    @progress.setter
    def progress(self, value):
        value = max(0.0, min(1.0, value))
        if value == self._progress:
            return
        old = self._progress
        self._progress = value
        
        if self._progress == 0.0:
            team = self.protocol.team1
        elif self._progress == 1.0:
            team = self.protocol.team2
        elif min(old, self._progress) <= 0.5 <= max(old, self._progress):
            team = None
        else:
            return
            
        if team != self.team:
            self.set_team(team)
            self.protocol.loop.create_task(self.on_capture(self, team))
    
    @property
    def rate(self):
        team1_count = sum(1 for p in self.players if p.team is self.protocol.team1)
        team2_count = sum(1 for p in self.players if p.team is self.protocol.team2)
        
        if team1_count == team2_count:
            rate = 0
        elif team1_count > team2_count:
            rate = -self.capture_rate * team1_count
        else:
            rate = self.capture_rate * team2_count
            
        if rate != self._rate:
            self.send_progress_bar(rate)
        
        self._rate = rate
        return rate
    
    def send_progress_bar(self, rate):
        progress_bar.set(self._progress, rate)
        progress_bar.color1.rgb = self.protocol.team1.color
        progress_bar.color2.rgb = self.protocol.team2.color
        self.protocol.broadcast_loader(progress_bar, connections=self.players)
        

class Occupation(GameMode):
    id = constants.MODE.OCCUPATION.value    
    name = "Occupation"
    
    title = "OCCUPATION_MODE_TITLE"
    description_key = "OCCUPATION_MODE_DESCRIPTION"
    info_text1 = "OCC_INFOGRAPHIC_TEXT1"
    info_text2 = "OCC_INFOGRAPHIC_TEXT2"
    info_text3 = "OCC_INFOGRAPHIC_TEXT3"
    
    @property
    def description(self):
        return f"""Capture and hold sectors across the map to gain points.
More team members in a sector means faster capture.
        
First team to reach {self.score_limit} points wins!
"""
    
    short_name = "oc"
    
    @property
    def score_limit(self):
        return self.config.get("score_limit", DEFAULT_SCORE_LIMIT)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sectors: List[Sector] = []
        Sector.on_capture += self.on_sector_captured
        
    def start(self):
        super().start()
        self.spawn_sectors()
        self.protocol.team1.score = 0
        self.protocol.team2.score = 0
        
    def stop(self):
        super().stop()
        for sector in self.sectors:
            sector.destroy()
        self.sectors.clear()
        
    def spawn_sectors(self):
        map_width = self.protocol.map.width()
        map_height = self.protocol.map.length()
        sector_count = self.config.get("sector_count", DEFAULT_SECTOR_COUNT)
        
        # Create a grid of sectors across the map
        cols = int(sector_count ** 0.5) + 1
        rows = (sector_count // cols) + 1
        
        cell_width = map_width / cols
        cell_height = map_height / rows
        
        count = 0
        for row in range(rows):
            for col in range(cols):
                if count >= sector_count:
                    break
                    
                # Position in center of cell with some randomness
                x = int((col + 0.5) * cell_width + random.randint(-10, 10))
                y = int((row + 0.5) * cell_height + random.randint(-10, 10))
                position = types.Position(x, y, 0)
                
                # Assign initial team based on position
                if col < cols // 2:
                    team = self.protocol.team1
                elif col > cols // 2:
                    team = self.protocol.team2
                else:
                    team = None
                    
                sector = self.protocol.create_entity(
                    Sector,
                    position=position,
                    team=team,
                    capture_radius=self.config.get("capture_radius"),
                    capture_rate=self.config.get("capture_rate")
                )
                self.sectors.append(sector)
                count += 1
    
    async def on_sector_captured(self, sector: Sector, team: types.Team):
        grid = self.protocol.map.to_grid(sector.position.x, sector.position.y)
        if team is None:
            self.protocol.broadcast_hud_message(f"Sector {grid} has been neutralized")
        else:
            self.protocol.broadcast_hud_message(f"{team.name} team captured sector {grid}")
        self.check_win()
        
    def check_win(self):
        if self.protocol.team1.score >= self.score_limit:
            self.end_game(self.protocol.team1)
        elif self.protocol.team2.score >= self.score_limit:
            self.end_game(self.protocol.team2)
            
    def get_spawn_point(self, player: ServerConnection) -> Tuple[int, int, int]:
        # Find sectors controlled by player's team
        team_sectors = [s for s in self.sectors if s.team is player.team]
        
        if team_sectors:
            # Spawn near a controlled sector
            sector = random.choice(team_sectors)
            # Find spawn point in radius around sector
            angle = random.random() * 2 * 3.14159
            distance = random.randint(20, 30)
            spawn_x = sector.position.x + int(distance * util.math.cos(angle))
            spawn_y = sector.position.y + int(distance * util.math.sin(angle))
            spawn_x = max(0, min(self.protocol.map.width() - 1, spawn_x))
            spawn_y = max(0, min(self.protocol.map.length() - 1, spawn_y))
            z = self.protocol.map.get_z(spawn_x, spawn_y)
            return spawn_x + 0.5, spawn_y + 0.5, z - 2
            
        # Default spawn if no sectors are controlled
        return super().get_spawn_point(player)


def init(protocol: ServerProtocol):
    return Occupation(protocol)
