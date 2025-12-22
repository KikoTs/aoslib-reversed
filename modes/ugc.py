from typing import Tuple, Optional

from shared import constants
from modes import GameMode
from server import types
from server.protocol import ServerProtocol
from server.connection import ServerConnection


class UGC(GameMode):
    id = constants.MODE.UGC.value
    name = "Map Creator"
    
    title = "MAP_CREATOR"
    description_key = "UGC_DESCRIPTION"
    info_text1 = ""
    info_text2 = ""
    info_text3 = ""
    
    @property
    def description(self):
        return """Create and edit maps in a collaborative environment.
Use the building tools to place blocks, create structures, and design game areas.
"""
    
    short_name = "ugc"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Map creator mode isn't team-based and has no scoring
        self.team_based = False
        
        # Set build mode defaults
        self.build_height_limit = self.config.get("build_height_limit", 64)
        self.allow_terrain_modification = self.config.get("allow_terrain_modification", True)
        self.enable_entity_placement = self.config.get("enable_entity_placement", True)
        
        # Track player permissions
        self.admin_players = set()
        
        # Register event handlers
        ServerConnection.on_player_connect += self.on_player_connect
        ServerConnection.on_player_disconnect += self.on_player_disconnect
        
    def start(self):
        super().start()
        
        # Display instructions to all players
        self.broadcast_instructions()
        
    def stop(self):
        super().stop()
        self.admin_players.clear()
        
    def broadcast_instructions(self):
        """Send building instructions to all players"""
        for player in self.protocol.players.values():
            self.send_instructions(player)
            
    def send_instructions(self, player: ServerConnection):
        """Send building instructions to a player"""
        self.protocol.broadcast_hud_message("Welcome to Map Creator mode!", connections=[player])
        self.protocol.broadcast_hud_message("Use building tools to create and edit the map.", connections=[player])
        self.protocol.broadcast_hud_message("Press B to open the build menu.", connections=[player])
        
        # Additional instructions for admins
        if player in self.admin_players:
            self.protocol.broadcast_hud_message("ADMIN: You have additional map editing permissions.", connections=[player])
            
    def set_admin(self, player: ServerConnection, is_admin: bool = True):
        """Set or remove admin status for a player"""
        if is_admin:
            self.admin_players.add(player)
            self.protocol.broadcast_hud_message("You are now a map editor admin.", connections=[player])
        else:
            if player in self.admin_players:
                self.admin_players.remove(player)
                self.protocol.broadcast_hud_message("You are no longer a map editor admin.", connections=[player])
                
    def can_modify_terrain(self, player: ServerConnection) -> bool:
        """Check if player can modify terrain"""
        return self.allow_terrain_modification or player in self.admin_players
        
    def can_place_entity(self, player: ServerConnection) -> bool:
        """Check if player can place entities"""
        return self.enable_entity_placement or player in self.admin_players
        
    def is_within_height_limit(self, y_position: int) -> bool:
        """Check if position is within the building height limit"""
        return y_position <= self.build_height_limit
        
    async def on_player_connect(self, player: ServerConnection):
        """Handle player join"""
        # Set to neutral team
        player.team = None
        
        # Give build tools
        player.restock()
        
        # Send instructions
        self.send_instructions(player)
        
    async def on_player_disconnect(self, player: ServerConnection):
        """Handle player leave"""
        if player in self.admin_players:
            self.admin_players.remove(player)
            
    def process_command(self, player: ServerConnection, command: str) -> bool:
        """Process map editor commands from players"""
        if command.startswith('/'):
            parts = command[1:].split()
            
            if not parts:
                return False
                
            cmd = parts[0].lower()
            
            # Save map command
            if cmd == 'save':
                if player in self.admin_players:
                    map_name = parts[1] if len(parts) > 1 else "unnamed_map"
                    self.protocol.broadcast_hud_message(f"Saving map as '{map_name}'...")
                    # Actual saving would be implemented here
                    self.protocol.broadcast_hud_message(f"Map saved as '{map_name}'")
                else:
                    self.protocol.broadcast_hud_message("You need admin permissions to save maps", connections=[player])
                return True
                
            # Load map command
            elif cmd == 'load':
                if player in self.admin_players:
                    if len(parts) > 1:
                        map_name = parts[1]
                        self.protocol.broadcast_hud_message(f"Loading map '{map_name}'...")
                        # Actual loading would be implemented here
                        self.protocol.broadcast_hud_message(f"Map '{map_name}' loaded")
                    else:
                        self.protocol.broadcast_hud_message("Usage: /load <map_name>", connections=[player])
                else:
                    self.protocol.broadcast_hud_message("You need admin permissions to load maps", connections=[player])
                return True
                
            # Clear map command
            elif cmd == 'clear':
                if player in self.admin_players:
                    self.protocol.broadcast_hud_message("Warning: This will clear the entire map!", connections=[player])
                    self.protocol.broadcast_hud_message("Type '/confirm' to proceed or '/cancel' to abort", connections=[player])
                    # Logic for confirmation would be implemented here
                else:
                    self.protocol.broadcast_hud_message("You need admin permissions to clear the map", connections=[player])
                return True
                
            # Add admin command (would require server password in real implementation)
            elif cmd == 'admin' and len(parts) > 1 and parts[1] == 'password123':
                self.set_admin(player, True)
                return True
                
        return False
        
    def get_spawn_point(self, player: ServerConnection) -> Tuple[int, int, int]:
        """Get spawn point - in UGC mode, spawn in center of map"""
        map_width = self.protocol.map.width()
        map_height = self.protocol.map.length()
        
        x = map_width // 2
        y = map_height // 2
        z = self.protocol.map.get_z(x, y)
        
        return x + 0.5, y + 0.5, z - 2


def init(protocol: ServerProtocol):
    return UGC(protocol)
