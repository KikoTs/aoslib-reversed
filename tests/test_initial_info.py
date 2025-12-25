#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test InitialInfo packet serialization between Python 3 (write) and Python 2 (read).

Run with Python 3 first to generate hex:
    py test_initial_info.py

Then run with Python 2 to verify it reads correctly:
    py2 test_initial_info.py
"""
import sys
import os

# Set the root directory based on Python version
if sys.version_info[0] < 3:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.join(script_dir, "aosdump")
    os.chdir(root_dir)
    sys.path.insert(0, root_dir)
else:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, script_dir)

from shared import packet as packets
from shared.bytes import ByteWriter, ByteReader

def to_hex(data):
    """Convert data to hex string."""
    if sys.version_info[0] >= 3:
        if isinstance(data, str):
            data = data.encode('latin-1')
        return ' '.join('{:02X}'.format(b) for b in data)
    else:
        return ' '.join('{:02X}'.format(ord(b)) for b in data)

def create_test_initial_info():
    """Create an InitialInfo packet with known test values."""
    info = packets.InitialInfo()
    
    # Server info
    info.server_steam_id = 12345678901234
    info.server_ip = 0x12345678
    info.server_port = 27015
    
    # Mode info
    info.mode_name = "TEST_MODE"
    info.mode_description = "TEST_DESC"
    info.mode_infographic_text1 = "INFO1"
    info.mode_infographic_text2 = "INFO2"
    info.mode_infographic_text3 = "INFO3"
    info.mode_key = 8
    
    # Map info
    info.map_name = "TestMap"
    info.filename = "test.vxl"
    info.checksum = 123456
    info.map_is_ugc = 0
    
    # Game settings
    info.query_port = 27115
    info.classic = 0
    info.enable_minimap = 1
    info.same_team_collision = 0
    info.max_draw_distance = 192
    info.enable_colour_picker = 1
    info.enable_colour_palette = 0
    info.enable_deathcam = 1
    info.enable_sniper_beam = 1
    info.enable_spectator = 1
    info.exposed_teams_always_on_minimap = 0
    info.enable_numeric_hp = 1
    info.texture_skin = ""
    info.beach_z_modifiable = 1
    info.enable_minimap_height_icons = 0
    info.enable_fall_on_water_damage = 1
    info.block_wallet_multiplier = 1.0
    info.block_health_multiplier = 1.0
    info.enable_player_score = 1
    
    # Lists
    info.disabled_tools = [0]
    info.disabled_classes = []
    info.movement_speed_multipliers = [1.5, 1.5, 1.5]
    info.ugc_prefab_sets = [0, 1]
    
    info.server_name = "TestServer"
    info.ground_colors = [(100, 110, 120, 255)]
    info.allow_shooting_holding_intel = 1
    info.friendly_fire = 1
    info.enable_corpse_explosion = 1
    info.ugc_mode = 8
    
    return info

def main():
    if sys.version_info[0] >= 3:
        # Python 3: Write the packet and output hex
        print("=== Python 3: Writing InitialInfo packet ===")
        info = create_test_initial_info()
        
        writer = ByteWriter()
        try:
            info.write(writer)
        except Exception as e:
            print("ERROR writing packet: {}".format(e))
            import traceback
            traceback.print_exc()
            return
        
        # Convert to bytes using same encoding as ByteWriter.__str__
        raw_bytes = str(writer).encode('cp437')
        hex_output = to_hex(raw_bytes)
        print("Hex output:")
        print(hex_output)
        print("")
        print("Length: {} bytes".format(len(raw_bytes)))
        
        # Save hex to file for Python 2 to read (use absolute path)
        hex_file_path = os.path.join(script_dir, "test_initial_info_hex.txt")
        with open(hex_file_path, "w") as f:
            f.write(hex_output)
        print("Saved to {}".format(hex_file_path))
        
    else:
        # Python 2: Read the hex from file and verify
        print("=== Python 2: Reading InitialInfo packet ===")
        
        # Use parent directory (script_dir) to find the hex file
        hex_file_path = os.path.join(script_dir, "test_initial_info_hex.txt")
        try:
            with open(hex_file_path, "r") as f:
                hex_str = f.read().strip()
        except IOError:
            print("ERROR: Run with Python 3 first to generate test_initial_info_hex.txt")
            print("Expected at: {}".format(hex_file_path))
            return
        
        # Convert hex to bytes
        data = bytearray.fromhex(hex_str.replace(' ', ''))
        data_str = str(data)
        
        print("Read {} bytes".format(len(data)))
        
        reader = ByteReader(data_str)
        
        # Read packet ID
        packet_id = reader.read_byte()
        print("Packet ID: {} (expected 114)".format(packet_id))
        
        # Read InitialInfo
        info = packets.InitialInfo()
        try:
            info.read(reader)
            print("")
            print("=== Successfully read all fields! ===")
            print("server_steam_id: {}".format(info.server_steam_id))
            print("server_ip: {}".format(hex(info.server_ip)))
            print("server_port: {}".format(info.server_port))
            print("mode_name: {}".format(info.mode_name))
            print("mode_description: {}".format(info.mode_description))
            print("mode_key: {}".format(info.mode_key))
            print("map_name: {}".format(info.map_name))
            print("filename: {}".format(info.filename))
            print("checksum: {}".format(info.checksum))
            print("query_port: {}".format(info.query_port))
            print("classic: {}".format(info.classic))
            print("enable_minimap: {}".format(info.enable_minimap))
            print("max_draw_distance: {}".format(info.max_draw_distance))
            print("block_wallet_multiplier: {}".format(info.block_wallet_multiplier))
            print("block_health_multiplier: {}".format(info.block_health_multiplier))
            print("enable_player_score: {}".format(info.enable_player_score))
            print("disabled_tools: {}".format(info.disabled_tools))
            print("disabled_classes: {}".format(info.disabled_classes))
            print("movement_speed_multipliers: {}".format(info.movement_speed_multipliers))
            print("ugc_prefab_sets: {}".format(info.ugc_prefab_sets))
            print("server_name: {}".format(info.server_name))
            print("ground_colors: {}".format(info.ground_colors))
            print("allow_shooting_holding_intel: {}".format(info.allow_shooting_holding_intel))
            print("friendly_fire: {}".format(info.friendly_fire))
            print("enable_corpse_explosion: {}".format(info.enable_corpse_explosion))
            print("ugc_mode: {}".format(info.ugc_mode))
            print("")
            print("SUCCESS: InitialInfo packet read correctly in Python 2!")
        except Exception as e:
            print("ERROR reading packet: {}".format(e))
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()
