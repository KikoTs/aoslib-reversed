"""
VXL restoration tests.

Workflow:
    1. Python 2.7 against the original implementation:
       py2 .\tests\test_vxl.py
    2. Python 3 against the restored implementation:
       py .\tests\test_vxl.py
"""

import json
import os
import struct
import sys


IS_PY2 = sys.version_info[0] < 3
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
AOSDUMP_ROOT = os.path.join(PROJECT_ROOT, "aosdump")

if IS_PY2:
    os.chdir(AOSDUMP_ROOT)
    sys.path.insert(0, AOSDUMP_ROOT)
    MAP_PATH = os.path.join(AOSDUMP_ROOT, "maps", "Classic.vxl")
    REF_ROOT = AOSDUMP_ROOT
else:
    sys.path.insert(0, PROJECT_ROOT)
    MAP_PATH = os.path.join(AOSDUMP_ROOT, "maps", "Classic.vxl")
    REF_ROOT = AOSDUMP_ROOT

import aoslib.vxl as vxl


MODULE_API = [
    "A2",
    "CChunk",
    "VXL",
    "add_ground_color",
    "array",
    "clamp",
    "create_shadow_vbo",
    "delete_shadow_vbo",
    "generate_ground_color_table",
    "get_color_tuple",
    "memoryview",
    "parse_constant_overrides",
    "reset_ground_colors",
    "sphere_in_frustum",
]

VXL_API = [
    "add_point",
    "add_static_light",
    "change_thread_state",
    "check_only",
    "chunk_to_pointlist",
    "cleanup",
    "clear_checked_geometry",
    "color_block",
    "create_spot_shadows",
    "destroy",
    "done_processing",
    "draw",
    "draw_sea",
    "draw_spot_shadows",
    "erase_prefab_from_world",
    "generate_vxl",
    "get_color",
    "get_color_tuple",
    "get_ground_colors",
    "get_max_modifiable_z",
    "get_overview",
    "get_point",
    "get_prefab_touches_world",
    "get_solid",
    "has_neighbors",
    "is_space_to_add_blocks",
    "minimap_texture",
    "place_prefab_in_world",
    "post_load_draw_setup",
    "refresh_ground_colors",
    "remove_point",
    "remove_point_nochecks",
    "remove_static_light",
    "set_max_modifiable_z",
    "set_point",
    "set_shadow_char_height",
    "update_static_light_colour",
]

CCHUNK_API = [
    "delete",
    "draw",
    "get_colors",
    "to_block_list",
    "x1",
    "x2",
    "y1",
    "y2",
    "z1",
    "z2",
]

FORBIDDEN_MODULE_NAMES = [
    "Enum",
    "MapPacker",
    "MapSerializer",
    "MapSyncChunker",
    "VXLMap",
    "get_chunker",
    "load_vxl",
]

FORBIDDEN_VXL_NAMES = [
    "block_line",
    "build_point",
    "columns",
    "depth",
    "destroy_point",
    "estimated_size",
    "get_chunker",
    "get_random_pos",
    "get_z",
    "height",
    "is_water",
    "load_vxl",
    "map_info",
    "name",
    "ready",
    "width",
]

BLANK_VXL = b"\x00\xF0\xEF\x00" * (512 * 512)
FAILED = 0


def to_bytes(data):
    if data is None:
        return b""
    if IS_PY2:
        if isinstance(data, unicode):
            return data.encode("utf-8")
        return data
    if isinstance(data, bytes):
        return data
    if isinstance(data, bytearray):
        return bytes(data)
    if isinstance(data, str):
        return data.encode("utf-8")
    return str(data).encode("utf-8")


def hex_preview(data, limit=32):
    data = to_bytes(data)[:limit]
    if IS_PY2:
        return " ".join("{:02X}".format(ord(ch)) for ch in data)
    return " ".join("{:02X}".format(ch) for ch in data)


def ref_path(name, ext):
    return os.path.join(REF_ROOT, "vxl_ref_%s.%s" % (name, ext))


def write_reference(name, data, ext):
    path = ref_path(name, ext)
    with open(path, "wb") as handle:
        handle.write(to_bytes(data))
    print("[SAVED] %s" % os.path.basename(path))


def compare_reference(name, data, ext):
    global FAILED
    path = ref_path(name, ext)
    if not os.path.exists(path):
        print("[SKIP] Missing reference %s" % os.path.basename(path))
        return

    current = to_bytes(data)
    with open(path, "rb") as handle:
        reference = handle.read()

    if current == reference:
        print("[MATCH] %s" % name)
        return

    FAILED += 1
    print("[DIFF] %s" % name)
    print("  ref : %s" % hex_preview(reference))
    print("  ours: %s" % hex_preview(current))


def check_reference(name, data, ext):
    if IS_PY2:
        write_reference(name, data, ext)
    else:
        compare_reference(name, data, ext)


def check_condition(label, condition, detail):
    global FAILED
    if condition:
        print("[OK] %s" % label)
        return
    FAILED += 1
    print("[FAIL] %s: %s" % (label, detail))


def json_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def pack_u32(value):
    return struct.pack("<I", value)


def make_blank_vxl():
    source = "" if IS_PY2 else b""
    return vxl.VXL(-1, source, 0, 2)


def public_dir(value):
    return sorted(name for name in dir(value) if not name.startswith("_"))


def module_api_dir():
    return sorted(name for name in MODULE_API if hasattr(vxl, name))


def load_map_bytes():
    with open(MAP_PATH, "rb") as handle:
        return handle.read()


def first_solid(map_obj):
    for z in range(240):
        for y in range(512):
            for x in range(512):
                if map_obj.get_solid(x, y, z):
                    return (x, y, z)
    return None


def build_loader_fixture():
    empty = b"\x00\xF0\xEF\x00"
    single = b"\x00\x01\x01\x00" + pack_u32(0x7F112233)
    hidden_gap = (
        b"\x02\x00\x00\x00"
        + pack_u32(0x7F445566)
        + b"\x00\x02\x02\x02"
        + pack_u32(0x7F778899)
    )
    return empty + single + hidden_gap + empty


def build_shift_fixture():
    return b"\x00\x01\x01\x00" + pack_u32(0x7F0A141E)


def build_invalid_fixture():
    return b"\x00\xF1\xF1\x00" + pack_u32(0x7F010203)


def run_surface_tests(blank):
    check_reference("module_api", json_bytes(module_api_dir()), "json")
    check_reference("vxl_api", json_bytes(public_dir(blank)), "json")
    check_reference("cchunk_api", json_bytes(public_dir(vxl.CChunk())), "json")

    check_condition(
        "module API exact",
        module_api_dir() == MODULE_API,
        "module public names changed",
    )
    check_condition(
        "VXL API exact",
        public_dir(blank) == VXL_API,
        "VXL public names changed",
    )
    check_condition(
        "CChunk API exact",
        public_dir(vxl.CChunk()) == CCHUNK_API,
        "CChunk public names changed",
    )

    forbidden_module = {name: hasattr(vxl, name) for name in FORBIDDEN_MODULE_NAMES}
    forbidden_vxl = {name: hasattr(blank, name) for name in FORBIDDEN_VXL_NAMES}
    if not IS_PY2:
        check_condition(
            "forbidden module names absent",
            not any(forbidden_module.values()),
            str(forbidden_module),
        )
        check_condition(
            "forbidden VXL names absent",
            not any(forbidden_vxl.values()),
            str(forbidden_vxl),
        )


def run_constructor_tests():
    raw_map = load_map_bytes()
    constructor_results = {}
    cases = [
        ("zero_args", ()),
        ("one_arg", (1,)),
        ("two_args", (1, MAP_PATH)),
        ("three_args_path", (1, MAP_PATH, 3)),
        ("four_args_bytes", (-1, raw_map, len(raw_map), 2)),
    ]

    for label, args in cases:
        try:
            vxl.VXL(*args)
            constructor_results[label] = "ok"
        except Exception as exc:
            constructor_results[label] = type(exc).__name__

    check_reference("constructor_results", json_bytes(constructor_results), "json")
    check_condition(
        "constructor contract",
        constructor_results == {
            "zero_args": "TypeError",
            "one_arg": "TypeError",
            "two_args": "TypeError",
            "three_args_path": "ok",
            "four_args_bytes": "ok",
        },
        str(constructor_results),
    )


def run_blank_reference_tests(blank):
    color_cases = {}
    for value in [0x000000, 0xFFFFFF, 0xFF0000, 0x00FF00, 0x0000FF, 0x7F804020]:
        color_cases["0x%08X" % value] = list(vxl.get_color_tuple(value))

    blank_state = {
        "point_0_0_0": list(blank.get_point(0, 0, 0)),
        "color_tuple_0_0_0": list(blank.get_color_tuple(0, 0, 0)),
        "solid_0_0_0": blank.get_solid(0, 0, 0),
        "done_processing": blank.done_processing(),
        "ground_colors": blank.get_ground_colors(),
        "max_modifiable_z": blank.get_max_modifiable_z(),
        "has_neighbors": blank.has_neighbors(1, 2, 3, False),
        "is_space_to_add_blocks": blank.is_space_to_add_blocks(),
    }

    check_reference("module_color_cases", json_bytes(color_cases), "json")
    check_reference("blank_state", json_bytes(blank_state), "json")
    check_reference("blank_generate_vxl", blank.generate_vxl(), "bin")
    check_reference("blank_overview", blank.get_overview(), "bin")
    check_reference("blank_overview_transparent", blank.get_overview(0), "bin")

    check_condition(
        "blank generate_vxl bytes",
        blank.generate_vxl() == BLANK_VXL,
        "blank serialization changed",
    )
    check_condition(
        "blank overview length",
        len(blank.get_overview()) == 512 * 512 * 4,
        "unexpected overview size",
    )
    check_condition(
        "blank transparent overview length",
        len(blank.get_overview(0)) == 512 * 512 * 4,
        "unexpected transparent overview size",
    )


def run_py3_loader_tests():
    raw_map = load_map_bytes()
    by_path = vxl.VXL(1, MAP_PATH, 3)
    by_bytes = vxl.VXL(-1, raw_map, len(raw_map), 2)
    blank = make_blank_vxl()
    solid = first_solid(by_path)

    check_condition(
        "real map path/bytes roundtrip",
        by_path.generate_vxl() == by_bytes.generate_vxl() == raw_map,
        "path and bytes load differ",
    )
    check_condition(
        "real map has at least one solid voxel",
        solid is not None,
        "no solid voxel found after loading real map",
    )
    check_condition(
        "real map overview size",
        len(by_path.get_overview()) == 512 * 512 * 4,
        "real map overview size mismatch",
    )
    check_condition(
        "real map transparent overview size",
        len(by_path.get_overview(0)) == 512 * 512 * 4,
        "real map transparent overview size mismatch",
    )
    check_condition(
        "real map overview differs from blank",
        by_path.get_overview() != blank.get_overview(),
        "real map overview unexpectedly matches blank overview",
    )

    if solid is not None:
        point_a = by_path.get_point(*solid)
        point_b = by_bytes.get_point(*solid)
        check_condition(
            "real map solid point preserved",
            point_a == point_b and point_a[0] is True,
            "loaded point mismatch at %s" % (solid,),
        )

    fixture = build_loader_fixture()
    fixture_map = vxl.VXL(-1, fixture, len(fixture), 2)
    shift_fixture = build_shift_fixture()
    shift_map = vxl.VXL(-1, shift_fixture, len(shift_fixture), 2)
    base = 255

    check_condition(
        "fixture roundtrip bytes",
        fixture_map.generate_vxl() == fixture,
        "fixture did not roundtrip cleanly",
    )
    check_condition(
        "fixture centering and z shift",
        shift_map.get_point(base, base, 239) == (True, (10, 20, 30, 253)),
        str(shift_map.get_point(base, base, 239)),
    )
    check_condition(
        "fixture hidden solid gap",
        fixture_map.get_point(base, base + 1, 1) == (True, (0, 0, 0, 0)),
        str(fixture_map.get_point(base, base + 1, 1)),
    )
    check_condition(
        "fixture top and bottom colors",
        fixture_map.get_point(base + 1, base, 1) == (True, (17, 34, 51, 253))
        and fixture_map.get_point(base, base + 1, 0) == (True, (68, 85, 102, 253))
        and fixture_map.get_point(base, base + 1, 2) == (True, (119, 136, 153, 253)),
        "fixture colors decoded incorrectly",
    )

    invalid = build_invalid_fixture()
    invalid_map = vxl.VXL(-1, invalid, len(invalid), 2)
    check_condition(
        "invalid fixture falls back to blank",
        invalid_map.generate_vxl() == BLANK_VXL,
        "invalid map did not fall back to blank output",
    )


def main():
    print("=" * 60)
    if IS_PY2:
        print("TESTING ORIGINAL VXL (Python 2) - generating references")
    else:
        print("TESTING RESTORED VXL (Python 3) - comparing references")
    print("=" * 60)

    blank = make_blank_vxl()
    run_surface_tests(blank)
    run_constructor_tests()
    run_blank_reference_tests(blank)

    if not IS_PY2:
        run_py3_loader_tests()

    print("=" * 60)
    if IS_PY2:
        print("Reference generation complete.")
    elif FAILED:
        print("VXL tests finished with %d failure(s)." % FAILED)
    else:
        print("VXL tests passed.")
    print("=" * 60)
    return 0 if IS_PY2 or FAILED == 0 else 1


if __name__ == "__main__":
    exit_code = main()
    if IS_PY2:
        sys.stdout.flush()
        os._exit(exit_code)
    sys.exit(exit_code)
