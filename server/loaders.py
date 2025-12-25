from shared import packet as packets

__all__ = [
    "create_player", "position_data", "client_data", "oriented_item", "set_color",
    "fog_color", "existing_player", "player_left", "server_block_action", "block_build", "kill_action", "chat_message",
    "map_sync_start", "map_sync_chunk", "map_sync_end", "pack_start", "pack_chunk", "state_data", "create_entity", "change_entity",
    "destroy_entity", "restock", "set_hp", "change_class", "change_team", "weapon_reload", "progress_bar", "damage", "initiate_kick_message",
    "world_update", "block_line", "set_score", "play_sound", "stop_sound", "initial_info", "map_data_validation", "skybox_data", "clock_sync", "set_class_loadout", "new_player_connection"
]

create_player = packets.CreatePlayer()
position_data = packets.PositionData()
client_data = packets.ClientData()
oriented_item = packets.UseOrientedItem()
set_color = packets.SetColor()
fog_color = packets.FogColor()
existing_player = packets.ExistingPlayer()
player_left = packets.PlayerLeft()
server_block_action = packets.ServerBlockAction()
block_build = packets.BlockBuild()
kill_action = packets.KillAction()
chat_message = packets.ChatMessage()
map_sync_start = packets.MapSyncStart()
map_sync_chunk = packets.MapSyncChunk()
map_sync_end = packets.MapSyncEnd()
pack_start = packets.PackStart()
pack_chunk = packets.PackChunk()
state_data = packets.StateData()
create_entity = packets.CreateEntity()
change_entity = packets.ChangeEntity()
destroy_entity = packets.DestroyEntity()
restock = packets.Restock()
set_hp = packets.SetHP()
change_class = packets.ChangeClass()
change_team = packets.ChangeTeam()
weapon_reload = packets.WeaponReload()
progress_bar = packets.ProgressBar()
world_update = packets.WorldUpdate()
block_line = packets.BlockLine()
set_score = packets.SetScore()
play_sound = packets.PlaySound()
stop_sound = packets.StopSound()
initial_info = packets.InitialInfo()

# InitialInfo default values (matching reference client data)
initial_info.disabled_tools = [0]
initial_info.movement_speed_multipliers = [1.40625, 1.453125, 1.09375, 1.25, 1.40625, 1.65625, 1.328125, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 3.0, 3.0, 1.0, 1.546875, 1.34375]
initial_info.ugc_prefab_sets = [0, 1]
initial_info.ground_colors = [(59, 58, 55, 238), (40, 54, 64, 239)]
initial_info.server_steam_id = 0
initial_info.server_ip = 0
initial_info.server_port = 27015
initial_info.query_port = 27115
initial_info.server_name = ""
initial_info.mode_name = ""
initial_info.mode_description = ""
initial_info.mode_infographic_text1 = ""
initial_info.mode_infographic_text2 = ""
initial_info.mode_infographic_text3 = ""
initial_info.mode_key = 8
initial_info.map_name = ""
initial_info.filename = ""
initial_info.checksum = 0
initial_info.map_is_ugc = 0
initial_info.classic = 0
initial_info.enable_minimap = 1
initial_info.same_team_collision = 0
initial_info.max_draw_distance = 192
initial_info.enable_colour_picker = 1
initial_info.enable_colour_palette = 0
initial_info.enable_deathcam = 1
initial_info.enable_sniper_beam = 1
initial_info.enable_spectator = 1
initial_info.exposed_teams_always_on_minimap = 0
initial_info.enable_numeric_hp = 1
initial_info.texture_skin = None
initial_info.beach_z_modifiable = 1
initial_info.enable_minimap_height_icons = 0
initial_info.enable_fall_on_water_damage = 1
initial_info.block_wallet_multiplier = 1.0
initial_info.block_health_multiplier = 1.0
initial_info.enable_player_score = 1
initial_info.allow_shooting_holding_intel = 1
initial_info.friendly_fire = 1
initial_info.enable_corpse_explosion = 1
initial_info.ugc_mode = 8
map_data_validation = packets.MapDataValidation()
skybox_data = packets.SkyboxData()
clock_sync = packets.ClockSync()
set_class_loadout = packets.SetClassLoadout()
new_player_connection = packets.NewPlayerConnection()
damage = packets.Damage()
initiate_kick_message = packets.InitiateKickMessage()