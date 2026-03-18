# KV6 Restoration

## Scope

This slice restores `aoslib.kv6` around the original native
`aoslib.kv6.so`/`kv6.pyd` Python surface, with the implementation centered in
`aoslib/kv6.pyx`.

Files touched in this slice:

- `aoslib/kv6.pyx`
- `tests/test_kv6.py`
- `docs/kv6-restoration.md`

## Restored Public Surface

### Module-level names

The restored module keeps the native Python-facing names observed from the
original module:

- `Enum`
- `KV6`
- `MAGIC`
- `PALETTE_MAGIC`
- `_memoryviewslice`
- `array`
- `crc32`
- `memoryview`
- `random`
- `set_kv6_default_color`
- `state`

`MAGIC` remains `b"Kvxl"` and `PALETTE_MAGIC` remains `b"SPal"`.

### `KV6`

The restored `KV6` class exposes only the native public methods:

- `add_points`
- `destroy_kv6`
- `draw`
- `get_adjacent_points`
- `get_bounding_box_sizes`
- `get_bounds`
- `get_crc`
- `get_max_z_size`
- `get_pivots`
- `get_points`
- `get_scale`
- `get_sizes`
- `offset_pivots`
- `replace`
- `reset_prefab_pivots`
- `save`
- `set_adjacent_points`

## Constructor Contract

The restored constructor follows the original Cython wrapper contract:

```python
KV6(filename, billboards, offset=None, load_display=True, invscale=3, detail_level=0)
```

Observed rules used in the tests:

- `KV6()` is invalid
- `KV6(arg)` is invalid
- `KV6(None, 0)` is a type error
- `KV6(path, 0)` is valid
- `KV6(path, 0, None, False, 1, 0)` is valid
- keyword forms for `offset`, `load_display`, `invscale`, and `detail_level`
  are valid

## Loader And Save Notes

The Python 3 port now handles the native KV6 data path directly in
`aoslib/kv6.pyx`:

- standard `Kvxl` header parsing
- legacy 28-byte local fixture parsing for `simple.kv6`
- voxel record decode as 8-byte entries
- `xlen`/`ylen` metadata handling
- signed `crc32` behavior
- constructor-side pivot offset application
- `invscale` down-scaling during load
- exact `save()` byte round-tripping for the tracked `prefab.kv6` fixture

Two native quirks are preserved in the restored behavior:

- `replace(other)` transfers the display ownership handle only; it does not
  replace the receiving object's voxel data.
- `xlen` metadata excludes zeroed filler records, while `ylen` still counts all
  records in a column.

## Pivot And Adjacency Behavior

Restored behaviors covered by the slice:

- `offset_pivots(x, y, z)` adds offsets divided by the current scale
- `reset_prefab_pivots()` zeros all pivots
- `get_points()` returns a `_memoryviewslice` with six values per row:
  `x, y, z, r, g, b`
- `get_adjacent_points()` returns JSON-friendly coordinate triples
- `set_adjacent_points()` accepts the cache payload shape used by
  `aosdump/aoslib/models.py`

## Native Anchors Used

The implementation was shaped against the decompiled native KV6 flow described
in IDA:

- `load_kv6`
- `scale_kv6`
- `add_points`
- `save_kv6`
- `create_display`
- `draw_display`
- `destroy_display`
- `set_kv6_default_color`

## Test Coverage

`tests/test_kv6.py` now covers:

- module and class surface parity
- constructor arity and keyword handling
- `crc32("test") == -662733300`
- fixture loads for `simple.kv6` and `prefab.kv6`
- scaled load behavior through `invscale`
- `offset_pivots()` and `reset_prefab_pivots()`
- `save()` roundtrip on `prefab.kv6`
- adjacency cache JSON roundtrip
- `add_points()` overwrite behavior
- `replace()` ownership semantics and draw compatibility

When the original Python 2 binary fails to import because of missing native DLL
dependencies, the py2 harness reports that explicitly and exits cleanly instead
of silently comparing against guessed behavior.
