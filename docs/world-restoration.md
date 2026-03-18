# World Restoration

## Scope

This slice restores `aoslib.world` around the original native `aoslib.world.so`
surface and uses `shared.constants` plus the restored `aoslib.vxl` as the
authoritative dependencies.

## Public API

Module helpers kept:

- `A2`
- `cube_line`
- `floor`
- `get_next_cube`
- `get_random_vector`
- `is_centered`
- `parse_constant_overrides`
- `World`
- `Object`
- `Player`
- `PlayerMovementHistory`
- `Grenade`
- `GenericMovement`
- `ControlledGenericMovement`
- `FallingBlocks`
- `Debris`

Server-only compatibility names intentionally deferred in this slice:

- `cast_ray`
- `Player.set_animation`
- `Player.set_weapon`
- `Player.eye`
- `Player.dead`
- `Grenade.next_collision`

## Constructor Contracts

- `World(map)`
  - `map` must be `aoslib.vxl.VXL` or `None`
- `Object(parent, *args, **kwargs)`
  - `parent` must be `World` or `None`
  - forwards extra args to `initialize`
- `Player(parent)`
- `PlayerMovementHistory(player, loop_count)`
- `Grenade(parent, position, velocity, fuse)`
- `GenericMovement(parent, position[, velocity])`
- `ControlledGenericMovement(parent, position[, velocity[, forward_vector]])`
- `FallingBlocks(parent, x, y, z)`
- `Debris(parent, position, velocity, rotation, gravity_multiplier, rotation_speed)`

## Native Anchors Used

Main wrapper and kernel references pulled from IDA:

- `move_player`
- `boxclipmove`
- `collide_with_players`
- `check_cube_placement`
- `hitscan`
- `hitscan_accurate`
- `GetBlockFromRayWorldSpace`
- `set_walk`
- `set_crouch`
- `set_dead`
- `set_exploded`
- `Object.__init__`
- `Object.check_valid_position`

## Implementation Notes

- Gravity is kept as the native shared module-global value and defaults to `1.0`.
- Movement multipliers source directly from `shared.constants`.
- The player movement pass follows the native shape:
  - forward/strafe acceleration
  - diagonal scaling
  - airborne acceleration reduction
  - gravity and friction split
  - player-vs-player cylinder push
  - voxel collision with basic step-up handling
- `Player.update()` preserves the native contract of returning `None` when dead
  and a numeric movement/fall-damage result otherwise.
- `hitscan` and `hitscan_accurate` use voxel DDA against the restored `VXL`
  interface.

## Files Touched

- `aoslib/world.pyx`
- `tests/test_world.py`
- `tests/test_player_physics.py`
- `docs/world-restoration.md`

## Build And Test Workflow

Build the extension in a VS developer environment:

```powershell
$vc = 'C:\Program Files\Microsoft Visual Studio\2022\Enterprise\VC\Auxiliary\Build\vcvars64.bat'
cmd /c "`"$vc`" && C:\Python312\python.exe setup.py build_ext --inplace"
```

Run reference and restored world tests:

```powershell
C:\Python27_32\py2.exe tests\test_world.py
C:\Python312\python.exe tests\test_world.py
C:\Python312\python.exe tests\test_player_physics.py
```
