#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Compare working InitialInfo hex vs our output byte-by-byte.
"""
import sys

# Working hex from real server
WORKING_HEX = "72 00 7C 55 81 7A 0E 40 01 58 50 9B FC 87 69 00 00 43 54 46 5F 54 49 54 4C 45 00 43 54 46 5F 44 45 53 43 52 49 50 54 49 4F 4E 00 43 54 46 5F 49 4E 46 4F 47 52 41 50 48 49 43 5F 54 45 58 54 31 00 43 54 46 5F 49 4E 46 4F 47 52 41 50 48 49 43 5F 54 45 58 54 32 00 43 54 46 5F 49 4E 46 4F 47 52 41 50 48 49 43 5F 54 45 58 54 33 00 43 69 74 79 20 6F 66 20 43 68 69 63 61 67 6F 00 4C 6F 6E 64 6F 6E 00 80 1B 53 23 08 00 EB 69 00 01 00 C0 01 00 01 01 01 00 01 00 01 00 01 40 00 40 00 01 00 00 12 5A 00 5D 00 46 00 50 00 5A 00 6A 00 55 00 60 00 60 00 60 00 60 00 60 00 60 00 C0 00 C0 00 40 00 63 00 56 00 02 00 01 01 4B 69 6B 6F 54 73 20 41 63 65 2E 70 79 20 3C 33 00 02 3B 3A 37 EE 28 36 40 EF 00 01 01 00 01 08"

def hex_to_bytes(hex_str):
    return bytearray.fromhex(hex_str.replace(' ', ''))

def annotate_field(offset, size, name, data, verbose=True):
    """Print a field's bytes and decoded value."""
    end = offset + size
    if end > len(data):
        print("  {:3d}-{:3d}: {} [TRUNCATED - only {} bytes available]".format(offset, end-1, name, len(data) - offset))
        return offset, None
    
    field_bytes = data[offset:end]
    hex_str = ' '.join('{:02X}'.format(b) for b in field_bytes)
    
    # Decode based on type
    if size == 1:
        value = field_bytes[0]
    elif size == 2:
        value = field_bytes[0] | (field_bytes[1] << 8)
    elif size == 4:
        value = field_bytes[0] | (field_bytes[1] << 8) | (field_bytes[2] << 16) | (field_bytes[3] << 24)
    elif size == 8:
        value = 0
        for i in range(8):
            value |= field_bytes[i] << (8 * i)
    else:
        value = hex_str
    
    if verbose:
        print("  {:3d}-{:3d}: {} = {} ({})".format(offset, end-1, name, value, hex_str))
    
    return end, value

def read_string(data, offset):
    """Read null-terminated string."""
    end = offset
    while end < len(data) and data[end] != 0:
        end += 1
    s = bytes(data[offset:end]).decode('utf-8', errors='replace')
    print("  {:3d}-{:3d}: STRING = '{}' ({} bytes)".format(offset, end, s, end - offset + 1))
    return end + 1, s

def main():
    print("=" * 60)
    print("ANALYZING WORKING InitialInfo PACKET")
    print("=" * 60)
    
    data = hex_to_bytes(WORKING_HEX)
    print("Total length: {} bytes".format(len(data)))
    print("")
    
    pos = 0
    
    # Fixed fields
    pos, _ = annotate_field(pos, 1, "packet_id", data)
    pos, steam_id = annotate_field(pos, 8, "server_steam_id", data)
    pos, _ = annotate_field(pos, 4, "server_ip", data)
    pos, _ = annotate_field(pos, 4, "server_port", data)
    
    # Strings
    pos, _ = read_string(data, pos)  # mode_name
    pos, _ = read_string(data, pos)  # mode_description
    pos, _ = read_string(data, pos)  # mode_infographic_text1
    pos, _ = read_string(data, pos)  # mode_infographic_text2
    pos, _ = read_string(data, pos)  # mode_infographic_text3
    pos, _ = read_string(data, pos)  # map_name
    pos, _ = read_string(data, pos)  # filename
    
    pos, _ = annotate_field(pos, 4, "checksum", data)
    pos, _ = annotate_field(pos, 1, "mode_key", data)
    pos, _ = annotate_field(pos, 1, "map_is_ugc", data)
    pos, _ = annotate_field(pos, 2, "query_port", data)
    pos, _ = annotate_field(pos, 1, "classic", data)
    pos, _ = annotate_field(pos, 1, "enable_minimap", data)
    pos, _ = annotate_field(pos, 1, "same_team_collision", data)
    pos, _ = annotate_field(pos, 1, "max_draw_distance", data)
    pos, _ = annotate_field(pos, 1, "enable_colour_picker", data)
    pos, _ = annotate_field(pos, 1, "enable_colour_palette", data)
    pos, _ = annotate_field(pos, 1, "enable_deathcam", data)
    pos, _ = annotate_field(pos, 1, "enable_sniper_beam", data)
    pos, _ = annotate_field(pos, 1, "enable_spectator", data)
    pos, _ = annotate_field(pos, 1, "exposed_teams_always_on_minimap", data)
    pos, _ = annotate_field(pos, 1, "enable_numeric_hp", data)
    pos, _ = annotate_field(pos, 1, "texture_skin_or_padding", data)
    pos, _ = annotate_field(pos, 1, "beach_z_modifiable", data)
    pos, _ = annotate_field(pos, 1, "enable_minimap_height_icons", data)
    pos, _ = annotate_field(pos, 1, "enable_fall_on_water_damage", data)
    
    # Multipliers - check if 2 bytes (short) or 4 bytes (float)
    pos, _ = annotate_field(pos, 2, "block_wallet_multiplier (short)", data)
    pos, _ = annotate_field(pos, 2, "block_health_multiplier (short)", data)
    pos, _ = annotate_field(pos, 1, "enable_player_score", data)
    
    # Disabled tools
    pos, disabled_tools_count = annotate_field(pos, 1, "disabled_tools_count", data)
    for i in range(disabled_tools_count):
        pos, _ = annotate_field(pos, 1, "disabled_tool[{}]".format(i), data)
    
    # Disabled classes
    pos, disabled_classes_count = annotate_field(pos, 1, "disabled_classes_count", data)
    for i in range(disabled_classes_count):
        pos, _ = annotate_field(pos, 1, "disabled_class[{}]".format(i), data)
    
    # Movement speed multipliers - 2 bytes each (short)
    pos, movement_speed_count = annotate_field(pos, 1, "movement_speed_count", data)
    for i in range(movement_speed_count):
        pos, _ = annotate_field(pos, 2, "movement_speed[{}]".format(i), data)
    
    # UGC prefab sets
    pos, ugc_prefab_count = annotate_field(pos, 1, "ugc_prefab_sets_count", data)
    for i in range(ugc_prefab_count):
        pos, _ = annotate_field(pos, 1, "ugc_prefab_set[{}]".format(i), data)
    
    # enable_player_score again?
    pos, _ = annotate_field(pos, 1, "enable_player_score2", data)
    
    # server_name string
    pos, _ = read_string(data, pos)
    
    # Ground colors
    pos, ground_colors_count = annotate_field(pos, 1, "ground_colors_count", data)
    for i in range(ground_colors_count):
        pos, _ = annotate_field(pos, 4, "ground_color[{}] (RGBA)".format(i), data)
    # Null terminator
    pos, _ = annotate_field(pos, 1, "ground_colors_null_term", data)
    
    pos, _ = annotate_field(pos, 1, "allow_shooting_holding_intel", data)
    pos, _ = annotate_field(pos, 1, "friendly_fire", data)
    pos, _ = annotate_field(pos, 1, "padding_or_field", data)
    pos, _ = annotate_field(pos, 1, "enable_corpse_explosion", data)
    pos, _ = annotate_field(pos, 1, "ugc_mode", data)
    
    print("")
    print("Remaining bytes: {}".format(len(data) - pos))
    if pos < len(data):
        remaining = ' '.join('{:02X}'.format(b) for b in data[pos:])
        print("Remaining: {}".format(remaining))

if __name__ == "__main__":
    main()
