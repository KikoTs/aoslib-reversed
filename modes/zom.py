import random
from typing import Tuple

from shared import constants
from shared.constants import KILL
from modes import GameMode
from server import types
from server.protocol import ServerProtocol
from server.connection import ServerConnection


class ZombieMode(GameMode):
    id = constants.MODE.ZOMBIE.value
    name = "Zombie Mode"

    title = "ZOMBIE_MODE_TITLE"
    description_key = "ZOMBIE_MODE_DESCRIPTION"
    info_text1 = "ZOM_INFOGRAPHIC_TEXT1"
    info_text2 = "ZOM_INFOGRAPHIC_TEXT2"
    info_text3 = "ZOM_INFOGRAPHIC_TEXT3"

    @property
    def description(self):
        return """Survive the zombie apocalypse! Humans must stay alive while zombies try to infect them.
        
Last human standing wins, or zombies win if everyone is infected.
"""

    short_name = "zom"
    score_limit = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.zombies = set()
        self.humans = set()
        self.zombie_spawn_points = []
        self.human_spawn_points = []
        ServerConnection.on_player_disconnect += self.on_player_disconnect

    def start(self):
        super().start()
        self.setup_spawn_points()
        self.assign_initial_roles()

    def stop(self):
        super().stop()
        self.zombies.clear()
        self.humans.clear()

    def setup_spawn_points(self):
        # Setup spawn points for zombies and humans
        map_width = self.protocol.map.width()
        map_height = self.protocol.map.length()
        
        # Zombies spawn on one side
        for _ in range(5):
            pos = self.protocol.map.get_random_pos(0, 0, map_width * 0.2, map_height)
            self.zombie_spawn_points.append(pos)
            
        # Humans spawn on the other side
        for _ in range(5):
            pos = self.protocol.map.get_random_pos(map_width * 0.8, 0, map_width, map_height)
            self.human_spawn_points.append(pos)

    def assign_initial_roles(self):
        # Assign initial zombie(s)
        players = list(self.protocol.players.values())
        if not players:
            return
            
        # Select initial zombie(s)
        zombie_count = max(1, len(players) // 5)  # 20% of players start as zombies
        initial_zombies = random.sample(players, min(zombie_count, len(players)))
        
        for player in players:
            if player in initial_zombies:
                self.make_zombie(player)
            else:
                self.make_human(player)

    def make_zombie(self, player: ServerConnection):
        self.zombies.add(player)
        if player in self.humans:
            self.humans.remove(player)
        player.team = self.protocol.team2  # Assuming team2 is for zombies
        player.restock()
        self.protocol.broadcast_hud_message(f"{player} is now a zombie!")

    def make_human(self, player: ServerConnection):
        self.humans.add(player)
        if player in self.zombies:
            self.zombies.remove(player)
        player.team = self.protocol.team1  # Assuming team1 is for humans
        player.restock()

    async def on_player_disconnect(self, player: ServerConnection):
        self.zombies.discard(player)
        self.humans.discard(player)
        self.check_win_condition()

    async def on_player_kill(self, player: ServerConnection, kill_type: KILL, killer: ServerConnection, respawn_time: int):
        await super().on_player_kill(player, kill_type, killer, respawn_time)
        
        # If a human dies, they become a zombie
        if player in self.humans:
            self.make_zombie(player)
            
        self.check_win_condition()

    def check_win_condition(self):
        # Zombies win if no humans left
        if not self.humans:
            self.end_game(self.protocol.team2)
            
        # Last human standing wins if only one human left and game continues for a set time
        elif len(self.humans) == 1:
            last_human = next(iter(self.humans))
            self.protocol.broadcast_hud_message(f"{last_human} is the last human standing!")
            # Could start a timer here for last human survival bonus

    def get_spawn_point(self, player: ServerConnection) -> Tuple[int, int, int]:
        if player in self.zombies:
            x, y, z = random.choice(self.zombie_spawn_points)
        else:
            x, y, z = random.choice(self.human_spawn_points)
        return x + 0.5, y + 0.5, z - 2


def init(protocol: ServerProtocol):
    return ZombieMode(protocol)
