# VXL Restoration Notes

This document tracks the `aoslib.vxl` restoration slice that rebuilds the
Python-facing VXL surface around the original native loader behavior.

## Scope

- Main implementation file: `aoslib/vxl.pyx`
- Test entrypoint: `tests/test_vxl.py`
- Cleanup for an outdated probe: `tests/verify_gravity.py`
- Build fix used for local Windows rebuilds: `setup.py`

## Restored Python Surface

### Module-level API

The restored module keeps the original public entrypoints used by the old
`aosdump/aoslib/vxl.pyd` surface:

- `A2`
- `CChunk`
- `VXL`
- `add_ground_color`
- `array`
- `clamp`
- `create_shadow_vbo`
- `delete_shadow_vbo`
- `generate_ground_color_table`
- `get_color_tuple`
- `memoryview`
- `parse_constant_overrides`
- `reset_ground_colors`
- `sphere_in_frustum`

### `CChunk`

Restored public members:

- `delete`
- `draw`
- `get_colors`
- `to_block_list`
- `x1`
- `x2`
- `y1`
- `y2`
- `z1`
- `z2`

### `VXL`

Restored public members:

- `add_point`
- `add_static_light`
- `change_thread_state`
- `check_only`
- `chunk_to_pointlist`
- `cleanup`
- `clear_checked_geometry`
- `color_block`
- `create_spot_shadows`
- `destroy`
- `done_processing`
- `draw`
- `draw_sea`
- `draw_spot_shadows`
- `erase_prefab_from_world`
- `generate_vxl`
- `get_color`
- `get_color_tuple`
- `get_ground_colors`
- `get_max_modifiable_z`
- `get_overview`
- `get_point`
- `get_prefab_touches_world`
- `get_solid`
- `has_neighbors`
- `is_space_to_add_blocks`
- `minimap_texture`
- `place_prefab_in_world`
- `post_load_draw_setup`
- `refresh_ground_colors`
- `remove_point`
- `remove_point_nochecks`
- `remove_static_light`
- `set_max_modifiable_z`
- `set_point`
- `set_shadow_char_height`
- `update_static_light_colour`

Removed/privatized experimental surface:

- `Enum`
- `MapPacker`
- `MapSerializer`
- `MapSyncChunker`
- `VXLMap`
- `block_line`
- `build_point`
- `columns`
- `depth`
- `destroy_point`
- `estimated_size`
- `get_chunker`
- `get_random_pos`
- `get_z`
- `height`
- `is_water`
- `load_vxl`
- `map_info`
- `name`
- `ready`
- `width`

## Constructor Contract

The restored constructor follows the original arity rules:

- `VXL()` is invalid
- `VXL(arg)` is invalid
- `VXL(arg1, arg2)` is invalid
- `VXL(1, "maps/classic.vxl", 3)` is accepted
- `VXL(-1, raw_bytes, len(raw_bytes), 2)` is accepted

When the source is a filesystem path, constructor loading is the authoritative
map load path. There is no public `load_vxl` helper anymore.

## Loader Notes

The current loader in `aoslib/vxl.pyx` ports the native VXL span walk used by
the original binary:

1. `get_vxl_size` walks each packed column, follows chained spans, counts
   columns, and tracks the highest referenced Z value.
2. The constructor validates:
   - square column count
   - edge length `<= 512`
   - `max_z < 241`
3. Valid maps are centered with `(512 - size) // 2`.
4. Valid maps are shifted upward with `max(0, 239 - max_z)`.
5. Span decoding preserves:
   - explicit top colors
   - hidden solid air-gap fill
   - explicit bottom colors

Invalid sources fall back to the blank-map serialization buffer.

## Post-load Setup

IDA shows the original threaded load path calling:

- `load_vxl`
- `post_load_map_setup`

The current Python-side restoration keeps `post_load_draw_setup()` as the
compatibility hook that finalizes overview buffers. The full native
post-processing routine also performs extra marker, ground-color, and shadow
work that should be restored in a later pass when the rendering/runtime state
is available.

## IDA References Used

The following native routines were used as primary references from
`aoslib.vxl.so`:

- `get_vxl_size` at `0x7A90`
- `load_vxl` at `0xDB40`
- `post_load_map_setup` at `0xD140`

## Tests Added/Updated

`tests/test_vxl.py` now covers:

- public API surface parity
- constructor arity parity
- blank-map behavior parity
- py3-only real-map path-vs-bytes roundtrip checks
- handcrafted loader fixtures for:
  - square-size detection
  - centering offset
  - Z shifting
  - hidden solid gap fill
  - invalid-map fallback

`tests/verify_gravity.py` was updated to stop using the removed zero-argument
`VXL()` constructor.

## Build Note

Local Windows rebuilds in this workspace needed `/MANIFEST:NO` in `setup.py`
because `link.exe` could not launch `rc.exe` from the current shell
environment. That change is build-only and does not affect the VXL runtime API.
