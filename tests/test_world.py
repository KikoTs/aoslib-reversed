"""
World restoration tests.

Workflow:
    1. Python 2.7 against the original implementation:
       py2 .\tests\test_world.py
    2. Python 3 against the restored implementation:
       py .\tests\test_world.py
"""

import json
import os
import sys


IS_PY2 = sys.version_info[0] < 3
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
AOSDUMP_ROOT = os.path.join(PROJECT_ROOT, "aosdump")
FAILED = 0

if IS_PY2:
    os.chdir(AOSDUMP_ROOT)
    sys.path.insert(0, AOSDUMP_ROOT)
    REF_ROOT = AOSDUMP_ROOT
else:
    sys.path.insert(0, PROJECT_ROOT)
    REF_ROOT = AOSDUMP_ROOT

try:
    import aoslib.world as world
    from shared import glm
except ImportError as exc:
    message = str(exc)
    if IS_PY2:
        print("[SKIP] Could not import original aoslib.world: %s" % message)
        print("[INFO] Missing native DLL dependency or incomplete py2 runtime.")
        sys.exit(0)
    raise


WORLD_API = [
    "create_object",
    "get_block_face_center_position",
    "get_gravity",
    "hitscan",
    "hitscan_accurate",
    "map",
    "set_gravity",
    "timer",
    "update",
]

OBJECT_API = [
    "check_valid_position",
    "delete",
    "deleted",
    "initialize",
    "name",
    "position",
    "update",
]

PLAYER_API = [
    "airborne",
    "burdened",
    "check_cube_placement",
    "check_valid_position",
    "clear_locked_to_box",
    "crouch",
    "delete",
    "deleted",
    "down",
    "fall",
    "get_cube_sq_distance",
    "hover",
    "initialize",
    "is_locked_to_box",
    "jetpack",
    "jetpack_active",
    "jetpack_passive",
    "jump",
    "jump_this_frame",
    "left",
    "name",
    "orientation",
    "parachute",
    "parachute_active",
    "position",
    "right",
    "s",
    "set_class_accel_multiplier",
    "set_class_can_sprint_uphill",
    "set_class_crouch_sneak_multiplier",
    "set_class_fall_on_water_damage_multiplier",
    "set_class_falling_damage_max_damage",
    "set_class_falling_damage_max_distance",
    "set_class_falling_damage_min_distance",
    "set_class_jump_multiplier",
    "set_class_sprint_multiplier",
    "set_class_water_friction",
    "set_climb_slowdown",
    "set_crouch",
    "set_dead",
    "set_exploded",
    "set_locked_to_box",
    "set_orientation",
    "set_position",
    "set_velocity",
    "set_walk",
    "sneak",
    "sprint",
    "up",
    "update",
    "velocity",
    "wade",
]

GENERIC_API = [
    "check_valid_position",
    "delete",
    "deleted",
    "initialize",
    "last_hit_collision_block",
    "last_hit_normal",
    "name",
    "position",
    "set_allow_burying",
    "set_allow_floating",
    "set_bouncing",
    "set_gravity_multiplier",
    "set_max_speed",
    "set_position",
    "set_stop_on_collision",
    "set_stop_on_face",
    "set_velocity",
    "update",
    "velocity",
]

CONTROLLED_API = [
    "check_valid_position",
    "delete",
    "deleted",
    "forward_vector",
    "initialize",
    "input_back",
    "input_forward",
    "input_left",
    "input_right",
    "last_hit_collision_block",
    "last_hit_normal",
    "name",
    "position",
    "set_allow_burying",
    "set_allow_floating",
    "set_bouncing",
    "set_forward_vector",
    "set_gravity_multiplier",
    "set_max_speed",
    "set_position",
    "set_stop_on_collision",
    "set_stop_on_face",
    "set_velocity",
    "speed_back",
    "speed_forward",
    "speed_left",
    "speed_right",
    "strafing",
    "update",
    "velocity",
]

GRENADE_API = ["check_valid_position", "delete", "deleted", "fuse", "initialize", "name", "position", "update", "velocity"]
FALLING_BLOCKS_API = ["check_valid_position", "delete", "deleted", "initialize", "name", "position", "rotation", "update", "velocity"]
DEBRIS_API = ["check_valid_position", "delete", "deleted", "free", "in_use", "initialize", "name", "position", "rotation", "rotation_speed", "update", "use", "velocity"]
HISTORY_API = ["get_client_data", "loop_count", "position", "set_all_data", "velocity"]

REQUIRED_MODULE_NAMES = [
    "A2",
    "Debris",
    "FallingBlocks",
    "GenericMovement",
    "Grenade",
    "Object",
    "Player",
    "PlayerMovementHistory",
    "World",
    "ControlledGenericMovement",
    "cube_line",
    "floor",
    "get_next_cube",
    "get_random_vector",
    "is_centered",
    "json",
    "parse_constant_overrides",
    "sys",
    "time",
]

FORBIDDEN_MODULE_NAMES = ["cast_ray"]


def ref_path(name):
    return os.path.join(REF_ROOT, "world_ref_%s.json" % name)


def serialize(value):
    if hasattr(value, "x") and hasattr(value, "y") and hasattr(value, "z"):
        return [value.x, value.y, value.z]
    if isinstance(value, dict):
        return dict((key, serialize(val)) for key, val in sorted(value.items()))
    if isinstance(value, (list, tuple)):
        return [serialize(item) for item in value]
    return value


def save_or_compare(name, value):
    global FAILED
    payload = json.dumps(serialize(value), sort_keys=True, separators=(",", ":")).encode("utf-8")
    path = ref_path(name)
    if IS_PY2:
        with open(path, "wb") as handle:
            handle.write(payload)
        print("[SAVED] %s" % os.path.basename(path))
        return

    if not os.path.exists(path):
        FAILED += 1
        print("[FAIL] Missing reference %s" % os.path.basename(path))
        return

    with open(path, "rb") as handle:
        reference = handle.read()
    if payload == reference:
        print("[MATCH] %s" % name)
    else:
        FAILED += 1
        print("[DIFF] %s" % name)
        print("  ref : %s" % reference[:120])
        print("  ours: %s" % payload[:120])


def check(label, condition, detail):
    global FAILED
    if condition:
        print("[OK] %s" % label)
    else:
        FAILED += 1
        print("[FAIL] %s: %s" % (label, detail))


def dir_list(obj):
    return [name for name in dir(obj) if not name.startswith("__")]


def mutability_result(obj, assignments):
    result = {}
    for name, value in assignments:
        try:
            setattr(obj, name, value)
            result[name] = True
        except Exception:
            result[name] = False
    return result


def test_module_surface():
    for name in REQUIRED_MODULE_NAMES:
        check("module has %s" % name, hasattr(world, name), "missing")
    for name in FORBIDDEN_MODULE_NAMES:
        check("module lacks %s" % name, not hasattr(world, name), "unexpected public name")


def test_class_dirs():
    check("World dir", dir_list(world.World) == WORLD_API, dir_list(world.World))
    check("Object dir", dir_list(world.Object) == OBJECT_API, dir_list(world.Object))
    check("Player dir", dir_list(world.Player) == PLAYER_API, dir_list(world.Player))
    check("GenericMovement dir", dir_list(world.GenericMovement) == GENERIC_API, dir_list(world.GenericMovement))
    check("ControlledGenericMovement dir", dir_list(world.ControlledGenericMovement) == CONTROLLED_API, dir_list(world.ControlledGenericMovement))
    check("Grenade dir", dir_list(world.Grenade) == GRENADE_API, dir_list(world.Grenade))
    check("FallingBlocks dir", dir_list(world.FallingBlocks) == FALLING_BLOCKS_API, dir_list(world.FallingBlocks))
    check("Debris dir", dir_list(world.Debris) == DEBRIS_API, dir_list(world.Debris))
    check("PlayerMovementHistory dir", dir_list(world.PlayerMovementHistory) == HISTORY_API, dir_list(world.PlayerMovementHistory))


def test_helpers_and_reference_values():
    save_or_compare("cube_line_2_1_0", world.cube_line(0, 0, 0, 2, 1, 0))
    save_or_compare("cube_line_3_3_3", world.cube_line(0, 0, 0, 3, 3, 3))
    save_or_compare(
        "get_next_cube_faces",
        [serialize(world.get_next_cube(glm.IntVector3(10, 20, 30), face)) for face in range(8)],
    )
    save_or_compare("floor_neg", world.floor(-2.3))
    save_or_compare("A2", world.A2())
    save_or_compare("parse_constant_overrides", world.parse_constant_overrides())
    save_or_compare(
        "is_centered",
        world.is_centered(0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.1),
    )


def test_world_and_player_reference_values():
    test_world = world.World(None)
    save_or_compare("world_default_gravity", test_world.get_gravity())
    test_world.set_gravity(3.5)
    save_or_compare("world_shared_gravity", world.World(None).get_gravity())
    test_world.set_gravity(1.0)

    face_centers = [
        serialize(test_world.get_block_face_center_position(glm.IntVector3(5, 6, 7), face))
        for face in range(6)
    ]
    save_or_compare("world_face_centers", face_centers)

    player = world.Player(test_world)
    defaults = {
        "name": player.name,
        "position": serialize(player.position),
        "velocity": serialize(player.velocity),
        "orientation": serialize(player.orientation),
        "s": serialize(player.s),
        "airborne": player.airborne,
        "burdened": player.burdened,
        "crouch": player.crouch,
        "down": player.down,
        "fall": player.fall,
        "hover": player.hover,
        "jump": player.jump,
        "jump_this_frame": player.jump_this_frame,
        "left": player.left,
        "right": player.right,
        "sneak": player.sneak,
        "sprint": player.sprint,
        "up": player.up,
        "wade": player.wade,
    }
    save_or_compare("player_defaults", defaults)

    player.set_position(0.0, 0.0, 0.0)
    placement = player.check_cube_placement(glm.IntVector3(1, 2, 3), 10.0)
    save_or_compare("player_cube_placement", {"ok": placement, "sq_dist": player.get_cube_sq_distance()})

    mutability = mutability_result(
        player,
        [
            ("airborne", False),
            ("crouch", False),
            ("down", False),
            ("fall", False),
            ("left", False),
            ("right", False),
            ("up", False),
            ("wade", False),
            ("burdened", True),
            ("hover", True),
            ("is_locked_to_box", True),
            ("jetpack", True),
            ("jetpack_active", True),
            ("jetpack_passive", True),
            ("jump", True),
            ("jump_this_frame", True),
            ("orientation", glm.Vector3(0.0, 1.0, 0.0)),
            ("parachute", True),
            ("parachute_active", True),
            ("position", glm.Vector3(1.0, 2.0, 3.0)),
            ("s", glm.Vector3(1.0, 0.0, 0.0)),
            ("sneak", True),
            ("sprint", True),
            ("velocity", glm.Vector3(4.0, 5.0, 6.0)),
        ],
    )
    save_or_compare("player_mutability", mutability)


def test_constructor_contracts():
    check("World() fails", _raises(lambda: world.World()), "expected TypeError")
    check("World(None) works", isinstance(world.World(None), world.World), "constructor failed")
    check("Object(None) works", isinstance(world.Object(None), world.Object), "constructor failed")
    check("Player(None) works", isinstance(world.Player(None), world.Player), "constructor failed")
    check(
        "Grenade ctor",
        isinstance(world.Grenade(world.World(None), glm.Vector3(1, 2, 3), glm.Vector3(4, 5, 6), 2.5), world.Grenade),
        "constructor failed",
    )


def _raises(fn):
    try:
        fn()
    except Exception:
        return True
    return False


def main():
    test_module_surface()
    test_class_dirs()
    test_helpers_and_reference_values()
    test_world_and_player_reference_values()
    test_constructor_contracts()

    if FAILED:
        print("\n[FAIL] %d world checks failed" % FAILED)
        sys.exit(1)

    print("\n[OK] world checks passed")


if __name__ == "__main__":
    main()
