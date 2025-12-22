import asyncio
from typing import List, Dict, Tuple, Optional

from shared import constants
from modes import GameMode
from server import types, util
from server.protocol import ServerProtocol
from server.connection import ServerConnection


class TutorialStage:
    def __init__(self, title: str, description: str, objectives: List[str], callback=None):
        self.title = title
        self.description = description
        self.objectives = objectives
        self.callback = callback
        self.completed = False
        
    def complete(self):
        self.completed = True
        if self.callback:
            self.callback()


class Tutorial(GameMode):
    id = constants.MODE.TUTORIAL.value
    name = "Tutorial"
    
    title = "TUTORIAL_MODE_TITLE"
    description_key = "TUTORIAL_DESCRIPTION"
    info_text1 = ""
    info_text2 = ""
    info_text3 = ""
    
    @property
    def description(self):
        return """Learn the basics of the game through guided instruction.
Complete each objective to progress through the tutorial.
"""
    
    short_name = "tut"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_stage = 0
        self.stages: List[TutorialStage] = []
        self.player_progress: Dict[ServerConnection, int] = {}
        self.targets: List[types.Entity] = []
        self.completed_objectives: Dict[ServerConnection, List[bool]] = {}
        
        # Ensure only one player in tutorial
        self.max_players = 1
        self.team_based = False
        
        # Bind events
        ServerConnection.on_player_connect += self.on_player_connect
        ServerConnection.on_player_disconnect += self.on_player_disconnect
        
    def start(self):
        super().start()
        self.setup_tutorial_stages()
        
    def setup_tutorial_stages(self):
        """Define all tutorial stages"""
        self.stages = [
            TutorialStage(
                "Welcome to the Tutorial",
                "Learn the basics of movement and combat in this tutorial.",
                ["Move around using WASD", "Look around using the mouse"],
                self.advance_to_next_stage
            ),
            TutorialStage(
                "Basic Combat",
                "Let's learn how to use your weapons.",
                ["Press left mouse button to fire", "Press R to reload", "Eliminate the target dummy"],
                self.advance_to_next_stage
            ),
            TutorialStage(
                "Advanced Movement",
                "Let's try some advanced movement techniques.",
                ["Press SPACE to jump", "Press SHIFT to sprint", "Reach the marked location"],
                self.advance_to_next_stage
            ),
            TutorialStage(
                "Game Objectives",
                "Different game modes have different objectives.",
                ["Interact with the objective marker", "Defend the position for 10 seconds"],
                self.advance_to_next_stage
            ),
            TutorialStage(
                "Congratulations",
                "You've completed the tutorial! You're now ready to join real matches.",
                ["Join a multiplayer game from the main menu"],
                None
            )
        ]
        
    def advance_to_next_stage(self):
        """Move to the next tutorial stage"""
        if self.current_stage < len(self.stages) - 1:
            self.current_stage += 1
            self.setup_current_stage()
            
    def setup_current_stage(self):
        """Setup the current tutorial stage"""
        # Clean up previous stage if needed
        self.cleanup_current_stage()
        
        stage = self.stages[self.current_stage]
        
        # Announce new stage
        for player in self.protocol.players.values():
            self.protocol.broadcast_hud_message(f"Stage {self.current_stage + 1}: {stage.title}", connections=[player])
            self.protocol.broadcast_hud_message(stage.description, connections=[player])
            
            # Reset objective completion
            if player not in self.completed_objectives:
                self.completed_objectives[player] = [False] * len(stage.objectives)
            else:
                self.completed_objectives[player] = [False] * len(stage.objectives)
                
            # Show objectives
            for i, objective in enumerate(stage.objectives):
                self.protocol.broadcast_hud_message(f"Objective {i+1}: {objective}", connections=[player])
            
        # Setup stage-specific elements
        if self.current_stage == 1:  # Combat stage
            # Create target dummy
            map_width = self.protocol.map.width()
            map_height = self.protocol.map.length()
            x, y = map_width // 2, map_height // 2
            z = self.protocol.map.get_z(x, y)
            dummy = self.protocol.create_entity(types.CommandPost, position=types.Position(x, y, z), team=None)
            self.targets.append(dummy)
        
        elif self.current_stage == 2:  # Movement stage
            # Create location marker
            map_width = self.protocol.map.width()
            map_height = self.protocol.map.length()
            x, y = int(map_width * 0.75), int(map_height * 0.75)
            z = self.protocol.map.get_z(x, y)
            marker = self.protocol.create_entity(types.Flag, position=types.Position(x, y, z), team=None)
            self.targets.append(marker)
        
        elif self.current_stage == 3:  # Objectives stage
            # Create objective point
            map_width = self.protocol.map.width()
            map_height = self.protocol.map.length()
            x, y = map_width // 2, map_height // 2
            z = self.protocol.map.get_z(x, y)
            objective = self.protocol.create_entity(types.CommandPost, position=types.Position(x, y, z), team=None)
            self.targets.append(objective)
    
    def cleanup_current_stage(self):
        """Clean up entities from the current stage"""
        for target in self.targets:
            target.destroy()
        self.targets.clear()
    
    def stop(self):
        super().stop()
        self.cleanup_current_stage()
        self.player_progress.clear()
        self.completed_objectives.clear()
    
    async def on_player_connect(self, player: ServerConnection):
        """Handle player joining the tutorial"""
        # Set to neutral team
        player.team = None
        
        # Reset progress
        self.player_progress[player] = 0
        
        # Welcome message
        self.protocol.broadcast_hud_message("Welcome to the Tutorial!", connections=[player])
        self.protocol.broadcast_hud_message("Follow the instructions to learn how to play.", connections=[player])
        
        # Start first stage
        self.setup_current_stage()
    
    async def on_player_disconnect(self, player: ServerConnection):
        """Handle player leaving the tutorial"""
        if player in self.player_progress:
            del self.player_progress[player]
        if player in self.completed_objectives:
            del self.completed_objectives[player]
    
    def update(self, dt):
        super().update(dt)
        
        if not self.stages or not self.protocol.players:
            return
            
        stage = self.stages[self.current_stage]
        
        # Check stage-specific completion conditions
        for player in self.protocol.players.values():
            if player not in self.completed_objectives:
                continue
                
            # Stage 0: Movement tutorial
            if self.current_stage == 0:
                # Track WASD movement (would need actual input tracking)
                if not self.completed_objectives[player][0] and player.velocity.length() > 0:
                    self.completed_objectives[player][0] = True
                    self.protocol.broadcast_hud_message("Objective complete: Moving around", connections=[player])
                
                # Track mouse movement (would need actual input tracking)
                # Simulating completion after a delay
                if not self.completed_objectives[player][1]:
                    self.protocol.loop.call_later(5, self.complete_objective, player, 1)
            
            # Stage 1: Combat tutorial
            elif self.current_stage == 1:
                # Track shooting (would need actual input tracking)
                if not self.completed_objectives[player][0]:
                    self.protocol.loop.call_later(5, self.complete_objective, player, 0)
                
                # Track reloading (would need actual input tracking)
                if not self.completed_objectives[player][1]:
                    self.protocol.loop.call_later(10, self.complete_objective, player, 1)
                
                # Track target dummy destruction
                # Would check for actual target destruction
                if not self.completed_objectives[player][2]:
                    self.protocol.loop.call_later(15, self.complete_objective, player, 2)
            
            # Stage 2: Advanced movement
            elif self.current_stage == 2:
                # Track jumping (would need actual input tracking)
                if not self.completed_objectives[player][0]:
                    self.protocol.loop.call_later(5, self.complete_objective, player, 0)
                
                # Track sprinting (would need actual input tracking)
                if not self.completed_objectives[player][1]:
                    self.protocol.loop.call_later(10, self.complete_objective, player, 1)
                
                # Track reaching marker
                if not self.completed_objectives[player][2] and self.targets:
                    marker = self.targets[0]
                    if player.position.sq_distance(marker.position) < 9:  # Within 3 blocks
                        self.complete_objective(player, 2)
            
            # Stage 3: Game objectives
            elif self.current_stage == 3:
                # Track interaction with objective
                if not self.completed_objectives[player][0] and self.targets:
                    objective = self.targets[0]
                    if player.position.sq_distance(objective.position) < 16:  # Within 4 blocks
                        self.complete_objective(player, 0)
                
                # Track defending position
                if self.completed_objectives[player][0] and not self.completed_objectives[player][1]:
                    # Start defense timer after interacting
                    if not hasattr(player, 'defense_start_time'):
                        player.defense_start_time = self.protocol.time
                    
                    # Check if player has defended for 10 seconds
                    if self.protocol.time - player.defense_start_time >= 10:
                        self.complete_objective(player, 1)
            
            # Check if all objectives are completed
            if all(self.completed_objectives[player]) and not stage.completed:
                stage.completed = True
                self.protocol.broadcast_hud_message(f"Stage {self.current_stage + 1} complete!", connections=[player])
                
                if stage.callback:
                    stage.callback()
    
    def complete_objective(self, player: ServerConnection, objective_index: int):
        """Mark an objective as completed for a player"""
        if player in self.completed_objectives and 0 <= objective_index < len(self.completed_objectives[player]):
            if not self.completed_objectives[player][objective_index]:
                self.completed_objectives[player][objective_index] = True
                
                stage = self.stages[self.current_stage]
                self.protocol.broadcast_hud_message(
                    f"Objective complete: {stage.objectives[objective_index]}",
                    connections=[player]
                )
    
    def get_spawn_point(self, player: ServerConnection) -> Tuple[int, int, int]:
        """Get tutorial spawn point"""
        map_width = self.protocol.map.width()
        map_height = self.protocol.map.length()
        
        # Default spawn in center of map
        x, y = map_width // 2, map_height // 2
        
        # Move spawn based on stage
        if self.current_stage == 0:  # Basic movement
            x, y = int(map_width * 0.25), int(map_height * 0.25)
        elif self.current_stage == 2:  # Advanced movement
            x, y = int(map_width * 0.25), int(map_height * 0.25)
        
        z = self.protocol.map.get_z(x, y)
        return x + 0.5, y + 0.5, z - 2


def init(protocol: ServerProtocol):
    return Tutorial(protocol)
