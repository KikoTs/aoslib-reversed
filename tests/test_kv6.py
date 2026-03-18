"""
KV6 restoration tests.

Workflow:
    1. Python 2.7 against the original implementation:
       py2 .\tests\test_kv6.py
    2. Python 3 against the restored implementation:
       py .\tests\test_kv6.py
"""

import json
import os
import sys
import tempfile


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
    import aoslib.kv6 as kv6
except ImportError as exc:
    if IS_PY2:
        print("[SKIP] Could not import original aoslib.kv6: %s" % exc)
        print("[INFO] Missing native DLL dependency or incomplete py2 runtime.")
        sys.exit(0)
    raise


MODULE_API = [
    "Enum",
    "KV6",
    "MAGIC",
    "PALETTE_MAGIC",
    "_memoryviewslice",
    "array",
    "crc32",
    "memoryview",
    "random",
    "set_kv6_default_color",
    "state",
]

KV6_API = [
    "add_points",
    "destroy_kv6",
    "draw",
    "get_adjacent_points",
    "get_bounding_box_sizes",
    "get_bounds",
    "get_crc",
    "get_max_z_size",
    "get_pivots",
    "get_points",
    "get_scale",
    "get_sizes",
    "offset_pivots",
    "replace",
    "reset_prefab_pivots",
    "save",
    "set_adjacent_points",
]

FORBIDDEN_MODULE_NAMES = ["num_voxels", "os", "struct", "zlib"]
SIMPLE_PATH = os.path.join(PROJECT_ROOT, "simple.kv6")
PREFAB_PATH = os.path.join(PROJECT_ROOT, "prefab.kv6")


def to_bytes(value):
    if value is None:
        return b""
    if IS_PY2:
        if isinstance(value, unicode):
            return value.encode("latin-1")
        return value
    if isinstance(value, bytes):
        return value
    if isinstance(value, bytearray):
        return bytes(value)
    if isinstance(value, str):
        return value.encode("latin-1")
    return bytes(value)


def ref_path(name):
    return os.path.join(REF_ROOT, "kv6_ref_%s.json" % name)


def serialize(value):
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
        print("[SKIP] Missing reference %s" % os.path.basename(path))
        return

    with open(path, "rb") as handle:
        reference = handle.read()

    if payload == reference:
        print("[MATCH] %s" % name)
        return

    FAILED += 1
    print("[DIFF] %s" % name)
    print("  ref : %s" % reference[:160])
    print("  ours: %s" % payload[:160])


def check(label, condition, detail):
    global FAILED
    if condition:
        print("[OK] %s" % label)
        return
    FAILED += 1
    print("[FAIL] %s: %s" % (label, detail))


def public_dir(obj):
    return [name for name in dir(obj) if not name.startswith("__")]


def rows(view_obj):
    return [list(row) for row in view_obj]


def constructor_result(callback):
    try:
        callback()
        return "ok"
    except Exception as exc:
        return type(exc).__name__


def model_summary(model):
    point_rows = rows(model.get_points())
    adjacent = model.get_adjacent_points()
    return {
        "crc": model.get_crc(),
        "scale": model.get_scale(),
        "sizes": list(model.get_sizes()),
        "bbox": list(model.get_bounding_box_sizes()),
        "max_z": model.get_max_z_size(),
        "pivots": list(model.get_pivots()),
        "bounds": serialize(model.get_bounds()),
        "points_type": type(model.get_points()).__name__,
        "points_len": len(point_rows),
        "first_points": point_rows[:5],
        "adj_len": len(adjacent),
        "first_adj": serialize(adjacent[:10]),
    }


def test_module_surface():
    module_dir = public_dir(kv6)
    class_dir = public_dir(kv6.KV6)

    save_or_compare("module_api", module_dir)
    save_or_compare("kv6_api", class_dir)

    check("module API exact", module_dir == MODULE_API, module_dir)
    check("KV6 API exact", class_dir == KV6_API, class_dir)
    check("MAGIC exact", to_bytes(kv6.MAGIC) == b"Kvxl", kv6.MAGIC)
    check("PALETTE_MAGIC exact", to_bytes(kv6.PALETTE_MAGIC) == b"SPal", kv6.PALETTE_MAGIC)
    check("state default", hasattr(kv6.state, "value") and kv6.state.value == 0, kv6.state)
    for name in FORBIDDEN_MODULE_NAMES:
        check("module lacks %s" % name, not hasattr(kv6, name), "unexpected public name")


def test_constructor_contract():
    if IS_PY2:
        results = {
            "zero_args": constructor_result(lambda: kv6.KV6()),
            "one_arg": constructor_result(lambda: kv6.KV6(PREFAB_PATH)),
            "none_filename": constructor_result(lambda: kv6.KV6(None, 0)),
        }
        save_or_compare("constructor_type_errors", results)
        check(
            "constructor type errors",
            results == {
                "zero_args": "TypeError",
                "one_arg": "TypeError",
                "none_filename": "TypeError",
            },
            results,
        )
        print("[SKIP] Loader-backed constructor tests skipped under py2: original kv6.pyd hangs on direct repo path loads without its native FS setup.")
        return

    results = {
        "zero_args": constructor_result(lambda: kv6.KV6()),
        "one_arg": constructor_result(lambda: kv6.KV6(PREFAB_PATH)),
        "none_filename": constructor_result(lambda: kv6.KV6(None, 0)),
        "path_two_args": constructor_result(lambda: kv6.KV6(PREFAB_PATH, 0)),
        "path_six_args": constructor_result(lambda: kv6.KV6(PREFAB_PATH, 0, None, False, 1, 0)),
        "keyword_form": constructor_result(
            lambda: kv6.KV6(PREFAB_PATH, 0, offset=(3, 6, 9), load_display=False, invscale=3, detail_level=0)
        ),
    }

    save_or_compare("constructor_results", results)
    check(
        "constructor contract",
        results == {
            "zero_args": "TypeError",
            "one_arg": "TypeError",
            "none_filename": "TypeError",
            "path_two_args": "ok",
            "path_six_args": "ok",
            "keyword_form": "ok",
        },
        results,
    )


def test_fixture_loads():
    if IS_PY2:
        print("[SKIP] Fixture load checks skipped under py2: original kv6.pyd does not complete direct filesystem loads in this repo layout.")
        return

    simple = kv6.KV6(SIMPLE_PATH, 0, None, False, 1, 0)
    prefab = kv6.KV6(PREFAB_PATH, 0, None, False, 1, 0)

    simple_summary = model_summary(simple)
    prefab_summary = model_summary(prefab)

    save_or_compare("simple_summary", simple_summary)
    save_or_compare("prefab_summary", prefab_summary)

    check("crc32 exact", kv6.crc32("test") == -662733300, kv6.crc32("test"))
    check(
        "simple fixture summary",
        simple_summary
        == {
            "crc": 1394873693,
            "scale": 1,
            "sizes": [1, 1, 0],
            "bbox": [0, 0, 0],
            "max_z": 0.0,
            "pivots": [0.5, 0.5, 0.0],
            "bounds": [None, None],
            "points_type": "_memoryviewslice",
            "points_len": 0,
            "first_points": [],
            "adj_len": 0,
            "first_adj": [],
        },
        simple_summary,
    )
    check(
        "prefab fixture summary",
        prefab_summary
        == {
            "crc": -50611042,
            "scale": 1,
            "sizes": [4, 5, 4],
            "bbox": [4, 5, 4],
            "max_z": 3.0,
            "pivots": [0.0, 0.0, 0.0],
            "bounds": [[0, 0, 0], [3, 4, 3]],
            "points_type": "_memoryviewslice",
            "points_len": 45,
            "first_points": [
                [0, 0, 1, 200, 204, 204],
                [0, 0, 2, 200, 204, 204],
                [0, 1, 0, 200, 204, 204],
                [0, 1, 2, 200, 204, 204],
                [0, 1, 3, 232, 232, 232],
            ],
            "adj_len": 74,
            "first_adj": [
                [-1, 0, 1],
                [0, -1, 1],
                [0, 1, 1],
                [0, 0, 0],
                [-1, 0, 2],
                [0, -1, 2],
                [0, 0, 3],
                [-1, 1, 0],
                [0, 1, -1],
                [-1, 1, 2],
            ],
        },
        prefab_summary,
    )


def test_scaled_offsets_and_roundtrip():
    if IS_PY2:
        print("[SKIP] Scale/offset/save fixture checks skipped under py2: native loader depends on the original file-system setup.")
        return

    scaled = kv6.KV6(PREFAB_PATH, 0, None, False, 3, 0)
    scaled_rows = rows(scaled.get_points())
    scaled_summary = {
        "sizes": list(scaled.get_sizes()),
        "bbox": list(scaled.get_bounding_box_sizes()),
        "max_z": scaled.get_max_z_size(),
        "pivots": list(scaled.get_pivots()),
        "points": scaled_rows[:10],
    }

    scaled.offset_pivots(3, 6, 9)
    offset_summary = {
        "pivots": list(scaled.get_pivots()),
        "bounds": serialize(scaled.get_bounds()),
    }
    scaled.reset_prefab_pivots()
    reset_pivots = list(scaled.get_pivots())

    fd, temp_path = tempfile.mkstemp(suffix=".kv6")
    os.close(fd)
    try:
        source = kv6.KV6(PREFAB_PATH, 0, None, False, 1, 0)
        source.save(temp_path)
        roundtrip = kv6.KV6(temp_path, 0, None, False, 1, 0)
        with open(PREFAB_PATH, "rb") as handle:
            reference_bytes = handle.read()
        with open(temp_path, "rb") as handle:
            saved_bytes = handle.read()
        roundtrip_summary = {
            "same_bytes": saved_bytes == reference_bytes,
            "sizes": list(roundtrip.get_sizes()),
            "points_len": len(roundtrip.get_points()),
        }
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)

    save_or_compare("scaled_summary", scaled_summary)
    save_or_compare("offset_summary", offset_summary)
    save_or_compare("roundtrip_summary", roundtrip_summary)

    check(
        "scaled summary",
        scaled_summary
        == {
            "sizes": [2, 2, 2],
            "bbox": [4, 4, 4],
            "max_z": 3.0,
            "pivots": [0.0, 0.0, 0.0],
            "points": [
                [0, 0, 0, 200, 204, 204],
                [0, 0, 3, 232, 232, 232],
                [0, 3, 0, 200, 204, 204],
                [0, 3, 3, 232, 232, 232],
                [3, 0, 0, 200, 204, 204],
                [3, 0, 3, 160, 164, 164],
                [3, 3, 0, 200, 204, 204],
            ],
        },
        scaled_summary,
    )
    check(
        "offset pivots and bounds",
        offset_summary == {"pivots": [1.0, 2.0, 3.0], "bounds": [[-3, -6, -9], [0, -3, -6]]},
        offset_summary,
    )
    check("reset pivots", reset_pivots == [0.0, 0.0, 0.0], reset_pivots)
    check(
        "save roundtrip",
        roundtrip_summary == {"same_bytes": True, "sizes": [4, 5, 4], "points_len": 45},
        roundtrip_summary,
    )


def test_adjacency_cache_and_add_points():
    if IS_PY2:
        print("[SKIP] Adjacency/add_points fixture checks skipped under py2: native loader depends on the original file-system setup.")
        return

    prefab = kv6.KV6(PREFAB_PATH, 0, None, False, 1, 0)
    adjacent = prefab.get_adjacent_points()
    payload = json.dumps((prefab.get_crc(), adjacent))
    cached = kv6.KV6(PREFAB_PATH, 0, None, False, 1, 0)
    cached.set_adjacent_points(json.loads(payload)[1])
    check("adjacent cache roundtrip", cached.get_adjacent_points() == adjacent, cached.get_adjacent_points()[:10])

    added = kv6.KV6(SIMPLE_PATH, 0, None, False, 1, 0)
    added.add_points([(1, 2, 3, 10, 20, 30), (1, 2, 3, 11, 21, 31)])
    add_summary = {
        "crc": added.get_crc(),
        "sizes": list(added.get_sizes()),
        "bounds": serialize(added.get_bounds()),
        "points": rows(added.get_points()),
        "adj_len": len(added.get_adjacent_points()),
        "adj_head": serialize(added.get_adjacent_points()[:10]),
    }

    save_or_compare("add_points_summary", add_summary)
    check(
        "add_points summary",
        add_summary
        == {
            "crc": -1255005017,
            "sizes": [3, 4, 4],
            "bounds": [[2, 3, 3], [2, 3, 3]],
            "points": [[2, 3, 3, 11, 21, 31]],
            "adj_len": 6,
            "adj_head": [[1, 3, 3], [3, 3, 3], [2, 2, 3], [2, 4, 3], [2, 3, 2], [2, 3, 4]],
        },
        add_summary,
    )


def test_display_and_replace():
    if IS_PY2:
        print("[SKIP] Display ownership checks skipped under py2: native loader does not complete direct repo path loads in this environment.")
        return

    kv6.set_kv6_default_color(0.1, 0.2, 0.3)
    donor = kv6.KV6(PREFAB_PATH, 0, None, True, 1, 0)
    recipient = kv6.KV6(SIMPLE_PATH, 0, None, False, 1, 0)
    before = rows(recipient.get_points())
    recipient.replace(donor)
    after = rows(recipient.get_points())

    check("replace keeps voxel data", before == after, after)
    check("draw compatibility", recipient.draw(None) is None, recipient.draw(None))
    print("[SKIP] GL draw smoke test skipped: no OpenGL context in harness.")


def main():
    test_module_surface()
    test_constructor_contract()
    test_fixture_loads()
    test_scaled_offsets_and_roundtrip()
    test_adjacency_cache_and_add_points()
    test_display_and_replace()

    if FAILED:
        print("\n[FAIL] %d kv6 checks failed" % FAILED)
        sys.exit(1)

    print("\n[OK] kv6 checks passed")


if __name__ == "__main__":
    main()
