# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
"""
World Module - Ace of Spades World Physics & Entities

Core game logic for player movement, physics simulation, and game objects.
"""

import math
import random
from libc.math cimport sqrt, floor as c_floor, sin, cos

# Physics Constants (from shared.constants)
DEF GRAVITY = -32.0
DEF PLAYER_RADIUS = 0.45
DEF PLAYER_STANDING_POS_ABOVE_GROUND = 2.25
DEF PLAYER_CROUCHING_POS_ABOVE_GROUND = 1.35
DEF PLAYER_STANDING_HEIGHT = 2.7  # 2.25 + 0.45
DEF PLAYER_CROUCHING_HEIGHT = 1.8  # 1.35 + 0.45

# Movement Constants
DEF BASE_WALK_SPEED = 4.0
DEF TERMINAL_VELOCITY = 60.0
DEF JUMP_VELOCITY = 8.0
DEF FRICTION_GROUND = 10.0
DEF FRICTION_AIR = 0.5
DEF WATER_FRICTION = 8.0

# ============================================================================
# Module-level functions
# ============================================================================

cpdef object A2(object arg):
    """Passthrough function for compatibility"""
    return arg

cpdef object cube_line(int x1, int y1, int z1, int x2, int y2, int z2):
    """
    Traverse a line through voxel space using 3D DDA algorithm
    Returns list of (x, y, z) coordinates along the line
    """
    cdef list result = []
    cdef int dx = abs(x2 - x1)
    cdef int dy = abs(y2 - y1)
    cdef int dz = abs(z2 - z1)
    cdef int n = 1 + dx + dy + dz
    
    cdef int sx = 1 if x2 > x1 else (0 if x2 == x1 else -1)
    cdef int sy = 1 if y2 > y1 else (0 if y2 == y1 else -1)
    cdef int sz = 1 if z2 > z1 else (0 if z2 == z1 else -1)
    
    cdef int x = x1
    cdef int y = y1
    cdef int z = z1
    
    cdef int x_err = dx
    cdef int y_err = dy
    cdef int z_err = dz
    
    cdef int i
    for i in range(n):
        result.append((x, y, z))
        
        # Advance axis with highest error
        # On tie, priority depends on axis magnitudes  
        if x_err > y_err and x_err > z_err:
            x += sx
            x_err -= n
        elif y_err > x_err and y_err > z_err:
            y += sy
            y_err -= n
        elif z_err > x_err and z_err > y_err:
            z += sz
            z_err -= n
        else:
            # Tie - use delta-based priority
            if dz >= dy and dz >= dx:
                # Z dominant: Z > Y > X
                if z_err >= y_err and z_err >= x_err:
                    z += sz
                    z_err -= n
                elif y_err >= x_err:
                    y += sy
                    y_err -= n
                else:
                    x += sx
                    x_err -= n
            elif dy >= dx:
                # Y dominant: Y > X > Z (Note: Original comment said Y > X > Z, let's stick to that)
                if y_err >= x_err and y_err >= z_err:
                    y += sy
                    y_err -= n
                elif x_err >= z_err:
                    x += sx
                    x_err -= n
                else:
                    z += sz
                    z_err -= n
            else:
                # X dominant: X > Y > Z
                if x_err >= y_err and x_err >= z_err:
                    x += sx
                    x_err -= n
                elif y_err >= z_err:
                    y += sy
                    y_err -= n
                else:
                    z += sz
                    z_err -= n
        
        x_err += dx
        y_err += dy
        z_err += dz
    
    return result

cpdef float floor(float val):
    """Floor function - returns float to match original"""
    return c_floor(val)

cpdef tuple get_next_cube(tuple pos, tuple direction):
    """Get the next cube position in a given direction"""
    cdef float x = pos[0] + direction[0]
    cdef float y = pos[1] + direction[1]
    cdef float z = pos[2] + direction[2]
    return (int(c_floor(x)), int(c_floor(y)), int(c_floor(z)))

cpdef tuple get_random_vector():
    """Get a random normalized direction vector"""
    cdef float theta = random.random() * 2.0 * 3.14159265359
    cdef float phi = random.random() * 3.14159265359
    cdef float sp = sin(phi)
    return (sp * cos(theta), sp * sin(theta), cos(phi))

cpdef bint is_centered(tuple pos):
    """Check if position is centered in a block"""
    cdef float fx = pos[0] - c_floor(pos[0])
    cdef float fy = pos[1] - c_floor(pos[1])
    return abs(fx - 0.5) < 0.1 and abs(fy - 0.5) < 0.1

cpdef object parse_constant_overrides(object arg):
    """Parse constant overrides (compatibility)"""
    return arg


# ============================================================================
# World Class
# ============================================================================

cdef class World:
    """Main world container - holds map and manages game objects"""
    
    def __init__(self, object map_obj):
        self.map = map_obj
        self.timer = 0.0
        self._gravity = GRAVITY
        self.objects = []
    
    cpdef object create_object(self, object obj_type):
        """Create a new object in the world"""
        obj = obj_type(self)
        self.objects.append(obj)
        return obj
    
    cpdef tuple get_block_face_center_position(self, object pos, int face):
        """Get the center position of a block face (0-5: +x,-x,+y,-y,+z,-z)"""
        if isinstance(pos, tuple) or isinstance(pos, list):
            x, y, z = pos
        else:
            x, y, z = pos.x, pos.y, pos.z
            
        cdef float fx = x + 0.5
        cdef float fy = y + 0.5
        cdef float fz = z + 0.5
        
        if face == 0:    # +X
            return (x + 1.0, fy, fz)
        elif face == 1:  # -X
            return (float(x), fy, fz)
        elif face == 2:  # +Y
            return (fx, y + 1.0, fz)
        elif face == 3:  # -Y
            return (fx, float(y), fz)
        elif face == 4:  # +Z
            return (fx, fy, z + 1.0)
        else:            # -Z
            return (fx, fy, float(z))
    
    cpdef float get_gravity(self):
        """Get world gravity"""
        return self._gravity
    
    cpdef void set_gravity(self, float gravity):
        """Set world gravity"""
        self._gravity = gravity
    
    cpdef bint get_solid(self, int x, int y, int z):
        """Check if block is solid at position"""
        if self.map is None:
            return False
        if x < 0 or x >= 512 or y < 0 or y >= 512 or z < 0 or z >= 64:
            return z >= 63  # Water at bottom
        return self.map.get_solid(x, y, z)
    
    cpdef object hitscan(self, tuple start, tuple direction, float max_distance):
        """Perform hitscan raycast using 3D DDA algorithm"""
        cdef float x = start[0]
        cdef float y = start[1]
        cdef float z = start[2]
        cdef float dx = direction[0]
        cdef float dy = direction[1]
        cdef float dz = direction[2]
        
        cdef int map_x = int(c_floor(x))
        cdef int map_y = int(c_floor(y))
        cdef int map_z = int(c_floor(z))
        
        cdef float side_dist_x = 0.0
        cdef float side_dist_y = 0.0
        cdef float side_dist_z = 0.0
        
        cdef float delta_dist_x = abs(1.0 / dx) if dx != 0 else 1e30
        cdef float delta_dist_y = abs(1.0 / dy) if dy != 0 else 1e30
        cdef float delta_dist_z = abs(1.0 / dz) if dz != 0 else 1e30
        
        cdef float perp_wall_dist = 0.0
        
        cdef int step_x, step_y, step_z
        
        cdef int hit = 0
        cdef int side = 0 # 0=x, 1=y, 2=z
        
        if dx < 0:
            step_x = -1
            side_dist_x = (x - map_x) * delta_dist_x
        else:
            step_x = 1
            side_dist_x = (map_x + 1.0 - x) * delta_dist_x
            
        if dy < 0:
            step_y = -1
            side_dist_y = (y - map_y) * delta_dist_y
        else:
            step_y = 1
            side_dist_y = (map_y + 1.0 - y) * delta_dist_y
            
        if dz < 0:
            step_z = -1
            side_dist_z = (z - map_z) * delta_dist_z
        else:
            step_z = 1
            side_dist_z = (map_z + 1.0 - z) * delta_dist_z
            
        # DDA Loop
        while hit == 0 and perp_wall_dist < max_distance:
            if side_dist_x < side_dist_y:
                if side_dist_x < side_dist_z:
                    side_dist_x += delta_dist_x
                    map_x += step_x
                    side = 0
                else:
                    side_dist_z += delta_dist_z
                    map_z += step_z
                    side = 2
            else:
                if side_dist_y < side_dist_z:
                    side_dist_y += delta_dist_y
                    map_y += step_y
                    side = 1
                else:
                    side_dist_z += delta_dist_z
                    map_z += step_z
                    side = 2
            
            # Check collision
            if self.get_solid(map_x, map_y, map_z):
                hit = 1
                
                # Calculate intersection point and normal
                # Normal
                nx, ny, nz = 0.0, 0.0, 0.0
                if side == 0:
                    perp_wall_dist = (map_x - x + (1 - step_x) / 2) / dx
                    nx = -step_x
                elif side == 1:
                    perp_wall_dist = (map_y - y + (1 - step_y) / 2) / dy
                    ny = -step_y
                else:
                    perp_wall_dist = (map_z - z + (1 - step_z) / 2) / dz
                    nz = -step_z
                    
                # Exact hit position
                hit_x = x + perp_wall_dist * dx
                hit_y = y + perp_wall_dist * dy
                hit_z = z + perp_wall_dist * dz
                
                return ((hit_x, hit_y, hit_z), (nx, ny, nz), perp_wall_dist)
                
        return None
    
    cpdef object hitscan_accurate(self, tuple start, tuple direction, float max_distance):
        """Accurate hitscan using DDA algorithm"""
        return self.hitscan(start, direction, max_distance)
    
    cpdef void update(self, float dt):
        """Update world and all objects"""
        self.timer += dt
        
        # Update all objects
        cdef list to_remove = []
        for obj in self.objects:
            obj.update(dt)
            if obj.deleted:
                to_remove.append(obj)
        
        # Remove deleted objects
        for obj in to_remove:
            self.objects.remove(obj)


# ============================================================================
# Base Object Class
# ============================================================================

cdef class Object:
    """Base class for all world objects"""
    
    def __init__(self, object world=None):
        self.deleted = False
        self.name = ""
        self.position = (0.0, 0.0, 0.0)
        self.world = world
    
    cpdef bint check_valid_position(self, tuple pos):
        """Check if position is valid (not inside solid block)"""
        if self.world is None:
            return True
        cdef int x = int(c_floor(pos[0]))
        cdef int y = int(c_floor(pos[1]))
        cdef int z = int(c_floor(pos[2]))
        return not self.world.get_solid(x, y, z)
    
    cpdef void delete(self):
        """Mark this object for deletion"""
        self.deleted = True
    
    cpdef void initialize(self):
        """Initialize object (called after creation)"""
        pass
    
    cpdef void update(self, float dt):
        """Update object (called each frame)"""
        pass


# ============================================================================
# Player Class - Core Movement Physics
# ============================================================================

cdef class Player(Object):
    """Player with full movement physics"""
    
    def __init__(self, object world):
        super().__init__(world)
        
        # Input state
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.jump = False
        self.crouch = False
        self.sneak = False
        self.sprint = False
        self.jump_this_frame = False
        
        # Movement state
        self.airborne = False
        self.burdened = False
        self.fall = False
        self.hover = False
        self.is_locked_to_box = False
        self.jetpack = False
        self.jetpack_active = False
        self.jetpack_passive = False
        self.parachute = False
        self.parachute_active = False
        self.wade = False
        
        self.orientation = (1.0, 0.0, 0.0)  # Forward direction
        self.velocity = (0.0, 0.0, 0.0)
        self.s = None
        self.position = (256.0, 256.0, 32.0)  # Default spawn
        
        # Class multipliers (default soldier values)
        self._accel_multiplier = 0.7
        self._sprint_multiplier = 1.4
        self._crouch_sneak_multiplier = 0.5
        self._jump_multiplier = 1.2
        self._water_friction = 8.0
        self._falling_damage_min_dist = 10.0
        self._falling_damage_max_dist = 40.0
        self._falling_damage_max_damage = 100.0
        self._fall_on_water_damage_mult = 0.5
        self._can_sprint_uphill = False
        self._climb_slowdown = 0.5
        self._dead = False
        self._exploded = False
        self._walk = False
    
    cpdef bint check_cube_placement(self, int x, int y, int z):
        """Check if a cube can be placed at this position"""
        if self.world is None:
            return True
        # Can't place where solid block exists
        if self.world.get_solid(x, y, z):
            return False
        # Must be adjacent to existing block
        cdef int dx, dy, dz
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                for dz in [-1, 0, 1]:
                    if dx == 0 and dy == 0 and dz == 0:
                        continue
                    if self.world.get_solid(x + dx, y + dy, z + dz):
                        return True
        return False
    
    cpdef void clear_locked_to_box(self):
        """Clear locked to box state"""
        self.is_locked_to_box = False
    
    cpdef float get_cube_sq_distance(self, int x, int y, int z):
        """Get squared distance to cube center"""
        cdef float px = self.position[0]
        cdef float py = self.position[1]
        cdef float pz = self.position[2]
        cdef float dx = (x + 0.5) - px
        cdef float dy = (y + 0.5) - py
        cdef float dz = (z + 0.5) - pz
        return dx*dx + dy*dy + dz*dz
    
    # Class multiplier setters
    cpdef void set_class_accel_multiplier(self, float multiplier):
        self._accel_multiplier = multiplier
    
    cpdef void set_class_can_sprint_uphill(self, bint can_sprint):
        self._can_sprint_uphill = can_sprint
    
    cpdef void set_class_crouch_sneak_multiplier(self, float multiplier):
        self._crouch_sneak_multiplier = multiplier
    
    cpdef void set_class_fall_on_water_damage_multiplier(self, float multiplier):
        self._fall_on_water_damage_mult = multiplier
    
    cpdef void set_class_falling_damage_max_damage(self, float damage):
        self._falling_damage_max_damage = damage
    
    cpdef void set_class_falling_damage_max_distance(self, float distance):
        self._falling_damage_max_dist = distance
    
    cpdef void set_class_falling_damage_min_distance(self, float distance):
        self._falling_damage_min_dist = distance
    
    cpdef void set_class_jump_multiplier(self, float multiplier):
        self._jump_multiplier = multiplier
    
    cpdef void set_class_sprint_multiplier(self, float multiplier):
        self._sprint_multiplier = multiplier
    
    cpdef void set_class_water_friction(self, float friction):
        self._water_friction = friction
    
    cpdef void set_climb_slowdown(self, float slowdown):
        self._climb_slowdown = slowdown
    
    cpdef void set_crouch(self, bint crouch):
        self.crouch = crouch
    
    cpdef void set_dead(self, bint dead):
        self._dead = dead

    @property
    def dead(self):
        return self._dead
        
    @dead.setter
    def dead(self, value):
        self._dead = value

    
    cpdef void set_exploded(self, bint exploded):
        self._exploded = exploded
    
    cpdef void set_locked_to_box(self, object box):
        self.is_locked_to_box = True
    
    cpdef void set_orientation(self, object orientation):
        """Set player orientation (forward direction)"""
        self.orientation = tuple(orientation) if not isinstance(orientation, tuple) else orientation
    
    cpdef void set_position(self, object x, object y, object z):
        """Set player position"""
        self.position = (float(x), float(y), float(z))
    
    cpdef void set_velocity(self, object x, object y, object z):
        """Set player velocity"""
        self.velocity = (float(x), float(y), float(z))
    
    cpdef void set_walk(self, bint walk):
        self._walk = walk
    



    cpdef void update(self, float dt):
        """Main player update - physics simulation"""
        if self._dead:
            return
        
        cdef float px = self.position[0]
        cdef float py = self.position[1]
        cdef float pz = self.position[2]
        cdef float vx = self.velocity[0]
        cdef float vy = self.velocity[1]
        cdef float vz = self.velocity[2]
        cdef float ox, oy, speed, move_x, move_y, move_len, friction
        cdef int gx, gy, gz
        
        # Apply gravity
        if self.airborne and not self.hover:
            vz += GRAVITY * dt
            if vz < -TERMINAL_VELOCITY:
                vz = -TERMINAL_VELOCITY
        
        # Handle jumping
        if self.jump_this_frame and not self.airborne:
            vz = JUMP_VELOCITY * self._jump_multiplier
            self.airborne = True
            self.jump_this_frame = False
        
        # Calculate horizontal movement
        ox = self.orientation[0]
        oy = self.orientation[1]
        speed = BASE_WALK_SPEED * self._accel_multiplier
        
        if self.sprint and not self.crouch:
            speed *= self._sprint_multiplier
        elif self.crouch and self.sneak:
            speed *= self._crouch_sneak_multiplier
        
        # Movement input
        move_x = 0.0
        move_y = 0.0
        
        if self.up:
            move_x += ox
            move_y += oy
        if self.down:
            move_x -= ox
            move_y -= oy
        if self.left:
            move_x -= oy
            move_y += ox
        if self.right:
            move_x += oy
            move_y -= ox
        
        # Normalize horizontal movement
        move_len = sqrt(move_x * move_x + move_y * move_y)
        if move_len > 0.01:
            move_x /= move_len
            move_y /= move_len
            
            # Apply movement
            vx = move_x * speed
            vy = move_y * speed
        else:
            # Apply friction
            friction = FRICTION_GROUND if not self.airborne else FRICTION_AIR
            vx *= (1.0 - friction * dt)
            vy *= (1.0 - friction * dt)
        
        # Apply velocity to position
        px += vx * dt
        py += vy * dt
        pz += vz * dt
        
        # Ground collision (simple)
        if self.world is not None:
            gx = int(c_floor(px))
            gy = int(c_floor(py))
            gz = int(c_floor(pz))
            
            # Check if we hit ground
            if pz < 0:
                pz = 0
                vz = 0
                self.airborne = False
            elif self.world.get_solid(gx, gy, gz):
                pz = gz + 1.0
                vz = 0
                self.airborne = False
            else:
                # Check if there's ground below
                if not self.world.get_solid(gx, gy, gz - 1):
                    self.airborne = True
        
        # Check for water (z >= 63)
        self.wade = pz <= 0.5
        
        self.position = (px, py, pz)
        self.velocity = (vx, vy, vz)


# ============================================================================
# PlayerMovementHistory Class
# ============================================================================

cdef class PlayerMovementHistory:
    """Stores player movement history for validation/replay"""
    
    def __init__(self):
        self.loop_count = 0
        self.position = []
        self.velocity = []
    
    cpdef dict get_client_data(self):
        """Get data for client"""
        return {"loop_count": self.loop_count, "position": self.position, "velocity": self.velocity}
    
    cpdef void set_all_data(self, dict data):
        """Set all history data"""
        self.loop_count = data.get("loop_count", 0)
        self.position = data.get("position", [])
        self.velocity = data.get("velocity", [])


# ============================================================================
# Grenade Class
# ============================================================================

cdef class Grenade(Object):
    """Grenade with physics"""
    
    def __init__(self, object world):
        super().__init__(world)
        self.fuse = 3.0
        self.velocity = (0.0, 0.0, 0.0)
        self._gravity_mult = 1.0
        self._bounce = 0.4
    
    cpdef void update(self, float dt):
        """Update grenade physics"""
        self.fuse -= dt
        if self.fuse <= 0:
            self.delete()
            return
        
        cdef float px = self.position[0]
        cdef float py = self.position[1]
        cdef float pz = self.position[2]
        cdef float vx = self.velocity[0]
        cdef float vy = self.velocity[1]
        cdef float vz = self.velocity[2]
        
        # Apply gravity
        vz += GRAVITY * self._gravity_mult * dt
        
        # Apply velocity
        px += vx * dt
        py += vy * dt
        pz += vz * dt
        
        # Simple ground collision
        if pz < 0:
            pz = 0
            vz = -vz * self._bounce
            vx *= 0.8
            vy *= 0.8
        
        self.position = (px, py, pz)
        self.velocity = (vx, vy, vz)


# ============================================================================
# GenericMovement Class
# ============================================================================

cdef class GenericMovement(Object):
    """Generic physics object with customizable behavior"""
    
    def __init__(self, object world):
        super().__init__(world)
        self.last_hit_collision_block = None
        self.last_hit_normal = (0.0, 0.0, 0.0)
        self.velocity = (0.0, 0.0, 0.0)
        
        self._allow_burying = False
        self._allow_floating = False
        self._bouncing = False
        self._gravity_mult = 1.0
        self._max_speed = 100.0
        self._stop_on_collision = True
        self._stop_on_face = -1
    
    cpdef void set_allow_burying(self, bint allow):
        self._allow_burying = allow
    
    cpdef void set_allow_floating(self, bint allow):
        self._allow_floating = allow
    
    cpdef void set_bouncing(self, bint bouncing):
        self._bouncing = bouncing
    
    cpdef void set_gravity_multiplier(self, float multiplier):
        self._gravity_mult = multiplier
    
    cpdef void set_max_speed(self, float speed):
        self._max_speed = speed
    
    cpdef void set_position(self, float x, float y, float z):
        self.position = (x, y, z)
    
    cpdef void set_stop_on_collision(self, bint stop):
        self._stop_on_collision = stop
    
    cpdef void set_stop_on_face(self, int face):
        self._stop_on_face = face
    
    cpdef void set_velocity(self, float x, float y, float z):
        self.velocity = (x, y, z)
    
    cpdef void update(self, float dt):
        """Update generic movement physics"""
        cdef float px = self.position[0]
        cdef float py = self.position[1]
        cdef float pz = self.position[2]
        cdef float vx = self.velocity[0]
        cdef float vy = self.velocity[1]
        cdef float vz = self.velocity[2]
        
        # Apply gravity
        if not self._allow_floating:
            vz += GRAVITY * self._gravity_mult * dt
        
        # Clamp speed
        cdef float speed = sqrt(vx*vx + vy*vy + vz*vz)
        cdef float scale
        if speed > self._max_speed:
            scale = self._max_speed / speed
            vx *= scale
            vy *= scale
            vz *= scale
        
        # Apply velocity
        px += vx * dt
        py += vy * dt
        pz += vz * dt
        
        # Collision
        cdef int gx, gy, gz
        if self._stop_on_collision and self.world is not None:
            gx = int(c_floor(px))
            gy = int(c_floor(py))
            gz = int(c_floor(pz))
            
            if self.world.get_solid(gx, gy, gz):
                self.last_hit_collision_block = (gx, gy, gz)
                if self._bouncing:
                    vz = -vz * 0.5
                else:
                    vx = vy = vz = 0.0
        
        self.position = (px, py, pz)
        self.velocity = (vx, vy, vz)


# ============================================================================
# FallingBlocks Class
# ============================================================================

cdef class FallingBlocks(Object):
    """Falling blocks after block destruction"""
    
    def __init__(self, object world):
        super().__init__(world)
        self.rotation = (0.0, 0.0, 0.0)
        self.velocity = (0.0, 0.0, 0.0)
        self.blocks = []
    
    cpdef void update(self, float dt):
        """Update falling blocks"""
        cdef float px = self.position[0]
        cdef float py = self.position[1]
        cdef float pz = self.position[2]
        cdef float vx = self.velocity[0]
        cdef float vy = self.velocity[1]
        cdef float vz = self.velocity[2]
        
        # Apply gravity
        vz += GRAVITY * dt
        
        # Apply velocity
        px += vx * dt
        py += vy * dt
        pz += vz * dt
        
        # Hit water/ground
        if pz <= 0:
            self.delete()
            return
        
        self.position = (px, py, pz)
        self.velocity = (vx, vy, vz)


# ============================================================================
# Debris Class
# ============================================================================

cdef class Debris(Object):
    """Small debris particles"""
    
    def __init__(self, object world):
        super().__init__(world)
        self.in_use = False
        self.rotation = (0.0, 0.0, 0.0)
        self.rotation_speed = (0.0, 0.0, 0.0)
        self.velocity = (0.0, 0.0, 0.0)
        self._lifetime = 5.0
    
    cpdef void free(self):
        self.in_use = False
    
    cpdef void use(self):
        self.in_use = True
    
    cpdef void update(self, float dt):
        """Update debris"""
        if not self.in_use:
            return
        
        self._lifetime -= dt
        if self._lifetime <= 0:
            self.free()
            return
        
        cdef float px = self.position[0]
        cdef float py = self.position[1]
        cdef float pz = self.position[2]
        cdef float vx = self.velocity[0]
        cdef float vy = self.velocity[1]
        cdef float vz = self.velocity[2]
        
        vz += GRAVITY * dt
        px += vx * dt
        py += vy * dt
        pz += vz * dt
        
        if pz < 0:
            self.free()
            return
        
        self.position = (px, py, pz)
        self.velocity = (vx, vy, vz)


# ============================================================================
# ControlledGenericMovement Class
# ============================================================================

cdef class ControlledGenericMovement(Object):
    """Generic movement with input controls (vehicles, etc.)"""
    
    def __init__(self, object world):
        super().__init__(world)
        self.forward_vector = (1.0, 0.0, 0.0)
        self.input_back = False
        self.input_forward = False
        self.input_left = False
        self.input_right = False
        self.last_hit_collision_block = None
        self.last_hit_normal = (0.0, 0.0, 0.0)
        self.speed_back = 1.0
        self.speed_forward = 1.0
        self.speed_left = 1.0
        self.speed_right = 1.0
        self.strafing = False
        self.velocity = (0.0, 0.0, 0.0)
        
        self._allow_burying = False
        self._allow_floating = False
        self._bouncing = False
        self._gravity_mult = 1.0
        self._max_speed = 100.0
        self._stop_on_collision = True
        self._stop_on_face = -1
    
    cpdef void set_allow_burying(self, bint allow):
        self._allow_burying = allow
    
    cpdef void set_allow_floating(self, bint allow):
        self._allow_floating = allow
    
    cpdef void set_bouncing(self, bint bouncing):
        self._bouncing = bouncing
    
    cpdef void set_forward_vector(self, tuple vector):
        self.forward_vector = vector
    
    cpdef void set_gravity_multiplier(self, float multiplier):
        self._gravity_mult = multiplier
    
    cpdef void set_max_speed(self, float speed):
        self._max_speed = speed
    
    cpdef void set_position(self, float x, float y, float z):
        self.position = (x, y, z)
    
    cpdef void set_stop_on_collision(self, bint stop):
        self._stop_on_collision = stop
    
    cpdef void set_stop_on_face(self, int face):
        self._stop_on_face = face
    
    cpdef void set_velocity(self, float x, float y, float z):
        self.velocity = (x, y, z)
    
    cpdef void update(self, float dt):
        """Update with input controls"""
        cdef float px = self.position[0]
        cdef float py = self.position[1]
        cdef float pz = self.position[2]
        cdef float vx = self.velocity[0]
        cdef float vy = self.velocity[1]
        cdef float vz = self.velocity[2]
        
        cdef float fx = self.forward_vector[0]
        cdef float fy = self.forward_vector[1]
        
        # Calculate right vector
        cdef float rx = -fy
        cdef float ry = fx
        
        # Apply input
        if self.input_forward:
            vx += fx * self.speed_forward * dt
            vy += fy * self.speed_forward * dt
        if self.input_back:
            vx -= fx * self.speed_back * dt
            vy -= fy * self.speed_back * dt
        if self.input_left:
            vx -= rx * self.speed_left * dt
            vy -= ry * self.speed_left * dt
        if self.input_right:
            vx += rx * self.speed_right * dt
            vy += ry * self.speed_right * dt
        
        # Apply gravity
        if not self._allow_floating:
            vz += GRAVITY * self._gravity_mult * dt
        
        # Apply velocity
        px += vx * dt
        py += vy * dt
        pz += vz * dt
        
        self.position = (px, py, pz)
        self.velocity = (vx, vy, vz)
