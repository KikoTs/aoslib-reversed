import sys
import os

# This runs for both python 2 and 3
# Those whole reason for this file is to test original impelementation vs our implementation
# That way we can see if our implementation is correct

#Make root directory "aosdump" if python 2 else keep this dir as root

# Set the root directory based on Python version
if sys.version_info[0] < 3:
    # For Python 2, set "aosdump" as root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.join(script_dir, "aosdump")
    if not os.path.exists(root_dir):
        os.makedirs(root_dir)
    os.chdir(root_dir)
    sys.path.insert(0, root_dir)
else:
    # For Python 3+, keep current directory as root
    pass

# Import after setting up the paths
import shared.packet as packet
from shared.bytes import ByteWriter, ByteReader


def toHex(data):
    #python 2 and 3 support
    if sys.version_info[0] < 3:
        return ' '.join('{:02X}'.format(ord(b)) for b in data)
    else:
        if isinstance(data, str):
            data = data.encode('cp437', 'replace')
        return ' '.join('{:02X}'.format(b) for b in data)
    


def test_initial_info():
    initial_info = packet.InitialInfo()
    initial_info.allow_shooting_holding_intel = 1
    initial_info.beach_z_modifiable = 1
    initial_info.block_health_multiplier = 1.0
    initial_info.block_wallet_multiplier = 1.0
    initial_info.checksum = 592649088
    initial_info.classic = 0
    initial_info.custom_game_rules = []
    initial_info.disabled_classes = []
    initial_info.disabled_tools = []
    initial_info.enable_colour_palette = 1
    initial_info.enable_colour_picker = 1
    initial_info.enable_corpse_explosion = 1
    initial_info.enable_deathcam = 1
    initial_info.enable_fall_on_water_damage = 1
    initial_info.enable_minimap = 1
    initial_info.enable_minimap_height_icons = 1
    initial_info.enable_numeric_hp = 1
    initial_info.enable_player_score = 1
    initial_info.enable_sniper_beam = 1
    initial_info.enable_spectator = 1
    initial_info.exposed_teams_always_on_minimap = 1
    initial_info.filename = "London"
    initial_info.friendly_fire = 0
    initial_info.ground_colors = []
    initial_info.loadout_overrides = {}
    initial_info.map_is_ugc = 0
    initial_info.map_name = "Chicago"
    initial_info.max_draw_distance = 192
    initial_info.mode_description = "Test1"
    initial_info.mode_infographic_text1 = "Test2"
    initial_info.mode_infographic_text2 = "Test3"
    initial_info.mode_infographic_text3 = "Test4"
    initial_info.mode_key = 1
    initial_info.mode_name = "Test5"
    initial_info.movement_speed_multipliers = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    initial_info.query_port = 25017
    initial_info.same_team_collision = 0
    initial_info.server_ip = 1
    initial_info.server_name = "Test Server"
    initial_info.server_port = 2
    initial_info.server_steam_id = 0
    initial_info.texture_skin = "mafia"
    initial_info.ugc_mode = 0
    initial_info.ugc_prefab_sets = []

    return initial_info

def test_set_hp(): # 1:1
    current_packet = packet.SetHP()
    current_packet.hp = 6
    current_packet.damage_type = 1

    current_packet.source_x = 1.1
    current_packet.source_y = 1.2
    current_packet.source_z = 1.3

    return current_packet

def test_hit_entity(): # 1:1
    current_packet = packet.HitEntity()
    current_packet.entity_id = 0
    current_packet.x = 1.0
    current_packet.y = 2.0
    current_packet.z = 3.0
    current_packet.type = 1

    return current_packet

def test_help_message(): # 1:1
    current_packet = packet.HelpMessage()
    current_packet.delay = 0.1
    current_packet.message_ids = ["test1", "test2", "test3"]

    return current_packet

def test_generic_vote_message(): # 1:1
    current_packet = packet.GenericVoteMessage()
    current_packet.allow_revote = 1
    current_packet.can_vote = 2
    current_packet.candidates = [{"name": "KikoTs", "votes": 1}]
    current_packet.title = "Test1"
    current_packet.description = "Test2"
    current_packet.message_type = 3
    current_packet.hide_after_vote = 4
    current_packet.player_id = 5
    return current_packet

def test_initiate_kick_message(): # 1:1
    current_packet = packet.InitiateKickMessage()
    current_packet.player_id = 1
    current_packet.target_id = 2
    current_packet.reason = 3
    return current_packet

def test_kill_action(): # 1:1
    current_packet = packet.KillAction()
    current_packet.player_id = 1
    current_packet.killer_id = 2
    current_packet.kill_type = 3
    current_packet.respawn_time = 4
    current_packet.isDominationKill = 5
    current_packet.isRevengeKill = 6
    current_packet.kill_count = 7
    return current_packet

def test_lock_team(): # 1:1
    current_packet = packet.LockTeam()
    current_packet.team_id = 1
    current_packet.locked = 2
    return current_packet

def test_lock_to_zone(): # 1:1
    current_packet = packet.LockToZone()
    current_packet.A2018 = 1
    current_packet.A2020 = 2
    current_packet.A2022 = 3
    current_packet.A2019 = 4
    current_packet.A2021 = 5
    current_packet.A2023 = 6
    return current_packet

def test_force_team_join(): # 1:1
    current_packet = packet.ForceTeamJoin()
    current_packet.team_id = 1
    current_packet.instant = 2
    return current_packet

def test_force_show_scores(): # 1:1
    current_packet = packet.ForceShowScores()
    current_packet.forced = 1
    return current_packet

def test_restock(): # 1:1
    current_packet = packet.Restock()
    current_packet.player_id = 1
    current_packet.type = 2
    return current_packet

def test_reqest_ugc_entities(): # 1:1
    current_packet = packet.ReqestUGCEntities()
    current_packet.game_mode = 1
    current_packet.in_ugc_mode = 2
    return current_packet

def test_prefab_complete(): # 1:1
    current_packet = packet.PrefabComplete()
    return current_packet

def test_player_left(): # 1:1
    current_packet = packet.PlayerLeft()
    current_packet.player_id = 1
    return current_packet

def test_change_class(): # 1:1
    current_packet = packet.ChangeClass()
    current_packet.player_id = 1
    current_packet.class_id = 2
    return current_packet

def test_change_team(): # 1:1
    current_packet = packet.ChangeTeam()
    current_packet.player_id = 1
    current_packet.team = 2
    return current_packet

def test_chat_message(): # 1:1
    current_packet = packet.ChatMessage()
    current_packet.player_id = 1
    current_packet.chat_type = 2
    current_packet.value = "Test1"
    return current_packet

def test_skybox_data(): # 1:1
    current_packet = packet.SkyboxData()
    current_packet.value = "Test1"
    return current_packet

def test_show_text_message(): # 1:1
    current_packet = packet.ShowTextMessage()
    current_packet.message_id = 1
    current_packet.duration = 2.0
    return current_packet

def test_stop_music(): # 1:1
    current_packet = packet.StopMusic()
    return current_packet

def test_stop_sound(): # 1:1
    current_packet = packet.StopSound()
    current_packet.loop_id = 1
    return current_packet

def test_team_infinite_blocks(): # 1:1
    current_packet = packet.TeamInfiniteBlocks()
    current_packet.team_id = 1
    current_packet.infinite_blocks = 2
    return current_packet

def test_team_lock_class(): # 1:1
    current_packet = packet.TeamLockClass()
    current_packet.team_id = 1
    current_packet.locked = 2
    return current_packet

def test_team_lock_score(): # 1:1
    current_packet = packet.TeamLockScore()
    current_packet.team_id = 1
    current_packet.locked = 2
    return current_packet

def test_team_map_visibility(): # 1:1
    current_packet = packet.TeamMapVisibility()
    current_packet.team_id = 1
    current_packet.visible = 2
    return current_packet

def test_use_command(): # 1:1
    current_packet = packet.UseCommand()
    return current_packet

def test_weapon_reload(): # 1:1
    current_packet = packet.WeaponReload()
    current_packet.player_id = 1
    current_packet.tool_id = 2
    current_packet.is_done = 3
    return current_packet

def test_set_score(): # 1:1
    current_packet = packet.SetScore()
    current_packet.type = 1
    current_packet.reason = 2
    current_packet.specifier = 3
    current_packet.value = 4
    return current_packet

def test_password(): # 1:1
    current_packet = packet.Password()
    current_packet.password = "Test1"
    return current_packet

def test_password_needed(): # 1:1
    current_packet = packet.PasswordNeeded()
    return current_packet

def test_password_provided(): # 1:1
    current_packet = packet.PasswordProvided()
    current_packet.password = "Test1"
    return current_packet

def test_time_scale(): # 1:1
    current_packet = packet.TimeScale()
    current_packet.scale = 1.0
    return current_packet

def test_set_class_loadout(): # 1:1
    current_packet = packet.SetClassLoadout()
    current_packet.player_id = 1
    current_packet.class_id = 2
    current_packet.loadout = [1, 2, 3]
    current_packet.prefabs = ["Test1", "Test2", "Test3"]
    current_packet.ugc_tools = [1, 2, 3]
    return current_packet

def test_clock_sync(): # 1:1
    current_packet = packet.ClockSync()
    current_packet.client_time = 1
    current_packet.server_loop_count = 2
    return current_packet

def test_destroy_entity(): # 1:1
    current_packet = packet.DestroyEntity()
    current_packet.entity_id = 1
    return current_packet

def test_disable_entity(): # 1:1
    current_packet = packet.DisableEntity()
    current_packet.entity_id = 1
    return current_packet

def test_explode_corpse(): # 1:1
    current_packet = packet.ExplodeCorpse()
    current_packet.player_id = 1
    current_packet.show_explosion_effect = 2
    return current_packet

def test_display_countdown(): # 1:1
    current_packet = packet.DisplayCountdown()
    current_packet.timer = 1.0
    return current_packet

def test_place_mg(): # 1:1
    current_packet = packet.PlaceMG()
    current_packet.loop_count = 1
    current_packet.player_id = 1
    current_packet.x = 2
    current_packet.y = 3
    current_packet.z = 4
    current_packet.yaw = 5.0
    return current_packet

def test_place_med_pack(): # 1:1
    current_packet = packet.PlaceMedPack()
    current_packet.loop_count = 1
    current_packet.player_id = 1
    current_packet.x = 2
    current_packet.y = 3
    current_packet.z = 4
    current_packet.face = 5
    return current_packet

def test_place_radar_station(): # 1:1
    current_packet = packet.PlaceRadarStation()
    current_packet.loop_count = 1
    current_packet.player_id = 1
    current_packet.x = 2
    current_packet.y = 3
    current_packet.z = 4
    return current_packet

def test_place_rocket_turret(): # 1:1
    current_packet = packet.PlaceRocketTurret()
    current_packet.loop_count = 1
    current_packet.player_id = 1
    current_packet.x = 2
    current_packet.y = 3
    current_packet.z = 4
    current_packet.yaw = 5.0
    return current_packet

def test_place_ugc(): # 1:1
    current_packet = packet.PlaceUGC()
    current_packet.loop_count = 1
    current_packet.x = 2
    current_packet.y = 3
    current_packet.z = 4
    current_packet.ugc_item_id = 5
    current_packet.placing = 6
    return current_packet

def test_pick_pickup(): # 1:1
    current_packet = packet.PickPickup()
    current_packet.player_id = 1
    current_packet.pickup_id = 2
    current_packet.burdensome = 3
    return current_packet

def test_place_c4(): # 1:1
    current_packet = packet.PlaceC4()
    current_packet.loop_count = 1
    current_packet.x = 2
    current_packet.y = 3
    current_packet.z = 4
    current_packet.face = 5
    return current_packet

def test_place_dynamite(): # 1:1
    current_packet = packet.PlaceDynamite()
    current_packet.loop_count = 1
    current_packet.x = 2
    current_packet.y = 3
    current_packet.z = 4
    current_packet.face = 5
    return current_packet

def test_place_flare_block(): # 1:1
    current_packet = packet.PlaceFlareBlock()
    current_packet.loop_count = 1
    current_packet.x = 2
    current_packet.y = 3
    current_packet.z = 4
    current_packet.face = 5
    return current_packet

def test_place_landmine(): # 1:1
    current_packet = packet.PlaceLandmine()
    current_packet.loop_count = 1
    current_packet.x = 2
    current_packet.y = 3
    current_packet.z = 4
    return current_packet

def test_play_ambient_sound(): # 1:1
    current_packet = packet.PlayAmbientSound()
    current_packet.name = "Test1"
    current_packet.loop_id = 1
    current_packet.looping = True
    current_packet.positioned = True
    current_packet.volume = 1.0
    current_packet.time = 2.0
    current_packet.attenuation = 3.0
    current_packet.x = 4.0
    current_packet.y = 5.0
    current_packet.z = 6.0
    return current_packet
    
def test_play_music(): # 1:1
    current_packet = packet.PlayMusic()
    current_packet.name = "Test1"
    current_packet.seconds_played = 2.0
    return current_packet

def test_play_sound(): # 1:1
    current_packet = packet.PlaySound()
    current_packet.sound_id = 1
    current_packet.loop_id = 2
    current_packet.looping = True
    current_packet.positioned = True
    current_packet.volume = 1.0
    current_packet.time = 2.0
    current_packet.attenuation = 3.0
    current_packet.x = 4.0
    current_packet.y = 5.0
    current_packet.z = 6.0
    return current_packet

def test_ugc_message(): # 1:1
    current_packet = packet.UGCMessage()
    current_packet.message_id = 1
    return current_packet

def test_ugc_map_info(): # 1:1
    current_packet = packet.UGCMapInfo()
    current_packet.png_data = b"test1"
    return current_packet

def test_ugc_map_loading_from_host(): # 1:1
    current_packet = packet.UGCMapLoadingFromHost()
    current_packet.percent_complete = 1
    return current_packet

def test_ugc_objectives(): # 1:1
    current_packet = packet.UGCObjectives()
    current_packet.mode = 1
    current_packet.noOfObjectives = 3
    current_packet.objective_ids = ["test1", "test2", "test3"]
    current_packet.objective_values = [1,2,3]
    return current_packet

def test_team_progress(): # 1:1
    current_packet = packet.TeamProgress()
    current_packet.team_id = 8
    current_packet.denominator = 1
    current_packet.numerator = 2
    current_packet.show_as_percent = 0
    current_packet.show_particle = 1
    current_packet.show_previous = 0
    current_packet.visible = 1
    current_packet.percent = 1.0
    current_packet.icon_id = 2
    return current_packet

def test_add_server(): # 1:1
    current_packet = packet.AddServer()
    current_packet.count = 14
    current_packet.game_mode = "tdm"
    current_packet.map = "London"
    current_packet.max_players = 2
    current_packet.name = "test server"
    current_packet.port = 1
    return current_packet

def test_block_build(): # 1:1
    current_packet = packet.BlockBuild()
    current_packet.loop_count = 1
    current_packet.player_id = 1
    current_packet.x = 2
    current_packet.y = 3
    current_packet.z = 4
    current_packet.block_type = 5
    return current_packet

def test_block_line(): # 1:1
    current_packet = packet.BlockLine()
    current_packet.loop_count = 1
    current_packet.player_id = 1
    current_packet.x1 = 2
    current_packet.y1 = 3
    current_packet.z1 = 4
    current_packet.x2 = 5
    current_packet.y2 = 6
    current_packet.z2 = 7
    return current_packet

def test_block_liberate(): # 1:1
    current_packet = packet.BlockLiberate()
    current_packet.loop_count = 1
    current_packet.player_id = 1
    current_packet.x = 2
    current_packet.y = 3
    current_packet.z = 4
    return current_packet

def test_block_occupy(): # 1:1
    current_packet = packet.BlockOccupy()
    current_packet.loop_count = 1
    current_packet.player_id = 1
    current_packet.x = 2
    current_packet.y = 3
    current_packet.z = 4
    return current_packet

def test_block_sucker_packet(): # 1:1
    current_packet = packet.BlockSuckerPacket()
    current_packet.loop_count = 1
    current_packet.shooter_id = 1
    current_packet.state = 2
    current_packet.shot = 3
    return current_packet

def test_change_player(): # 1:1
    current_packet = packet.ChangePlayer()
    current_packet.player_id = 1
    current_packet.type = 8
    current_packet.chase_cam = 3
    current_packet.high_minimap_visibility = 4
    return current_packet

def test_client_in_menu(): # 1:1
    current_packet = packet.ClientInMenu()
    current_packet.in_menu = 1
    return current_packet

def test_detonate_c4(): # 1:1
    current_packet = packet.DetonateC4()
    current_packet.loop_count = 1
    return current_packet

def test_disguise_packet(): # 1:1
    current_packet = packet.DisguisePacket()
    current_packet.loop_count = 1
    current_packet.active = 1
    return current_packet

def test_poifocus(): # 1:1
    current_packet = packet.POIFocus()
    current_packet.target_x = 1.0
    current_packet.target_y = 2.0
    current_packet.target_z = 3.0
    return current_packet

def test_drop_pickup(): # 1:1
    current_packet = packet.DropPickup()
    current_packet.loop_count = 1
    current_packet.player_id = 1
    current_packet.pickup_id = 2
    current_packet.position = (1.2, 1.2, 1.2)
    current_packet.velocity = (1.3, 1.3, 1.3)
    return current_packet

def test_debug_draw(): # 1:1
    current_packet = packet.DebugDraw()
    current_packet.colour = 1
    current_packet.frames = 2
    current_packet.size = 3.0
    current_packet.type = 1
    current_packet.x = 1.0
    current_packet.x2 = 1.0
    current_packet.y = 1.0
    current_packet.y2 = 1.0
    current_packet.z = 1.0
    current_packet.z2 = 1.0
    return current_packet

def test_voice_data(): # 1:1
    current_packet = packet.VoiceData()
    current_packet.player_id = 1
    current_packet.data = "test"
    current_packet.data_size = 4
    return current_packet

def test_steam_session_ticket(): # 1:1
    current_packet = packet.SteamSessionTicket()
    current_packet.ticket = b"test"
    current_packet.ticket_size = 4
    return current_packet

def test_rank_ups(): # 1:1
    current_packet = packet.RankUps()
    current_packet.new_scores = [1, 1, 1]
    current_packet.noOfRankUps = 3
    current_packet.old_scores = [2, 2, 2]
    current_packet.score_reasons = [3, 3, 3]
    return current_packet

def test_show_game_stats(): # 1:1
    current_packet = packet.ShowGameStats()
    return current_packet

def test_shoot_response(): # 1:1
    current_packet = packet.ShootResponse()
    current_packet.damage_by = 1
    current_packet.damaged = 2
    current_packet.blood = 3
    current_packet.position_x = 1.0
    current_packet.position_y = 2.0
    current_packet.position_z = 3.0
    return current_packet

def test_shoot_packet(): # 1:1
    current_packet = packet.ShootPacket()
    current_packet.loop_count = 1
    current_packet.shooter_id = 1
    current_packet.shot_on_world_update = 2
    current_packet.x = 1.0
    current_packet.y = 2.0
    current_packet.z = 3.0
    current_packet.ori_x = 4.0
    current_packet.ori_y = 5.0
    current_packet.ori_z = 6.0
    current_packet.damage = 7
    current_packet.penetration = 8
    current_packet.secondary = 9
    current_packet.seed = 10
    return current_packet

def test_set_ugc_edit_mode(): # 1:1
    current_packet = packet.SetUGCEditMode()
    current_packet.mode = 1
    return current_packet

def test_ugc_batch_entity(): # 1:1
    current_packet = packet.UGCBatchEntity()
    current_packet.mode = 1
    current_packet.ugc_item_id = 2
    current_packet.x = 3
    current_packet.y = 4
    current_packet.z = 5
    return current_packet

def test_shoot_feedback_packet(): # 1:1
    current_packet = packet.ShootFeedbackPacket()
    current_packet.loop_count = 1
    current_packet.seed = 2
    current_packet.shooter_id = 3
    current_packet.shot_on_world_update = 4
    current_packet.tool_id = 5
    return current_packet

def test_pack_response(): # 1:1
    current_packet = packet.PackResponse()
    current_packet.value = 1
    return current_packet

def test_pack_start(): # 1:1
    current_packet = packet.PackStart()
    current_packet.size = 1
    current_packet.checksum = 2
    return current_packet

def test_minimap_billboard(): # 1:1
    current_packet = packet.MinimapBillboard()
    current_packet.color = (1,2,3)
    current_packet.entity_id = 4
    current_packet.icon_name = 'icon_name'
    current_packet.key = 5
    current_packet.tracking = 6
    current_packet.x = 7.0
    current_packet.y = 8.0
    current_packet.z = 9.0
    return current_packet

def test_minimap_billboard_clear(): # 1:1
    current_packet = packet.MinimapBillboardClear()
    current_packet.entity_id = 1
    return current_packet

def test_minimap_zone(): # 1:1
    current_packet = packet.MinimapZone()
    current_packet.A2018 = 1
    current_packet.A2019 = 2
    current_packet.A2020 = 3
    current_packet.A2021 = 4
    current_packet.A2022 = 5
    current_packet.A2023 = 6
    current_packet.color = (1,2,3)
    current_packet.icon_id = 7
    current_packet.icon_scale = 8.0
    current_packet.key = 9
    current_packet.locked_in_zone = 10
    return current_packet

def test_minimap_zone_clear(): # 1:1
    current_packet = packet.MinimapZoneClear()
    current_packet.A2018 = 1
    current_packet.A2019 = 2
    current_packet.A2020 = 3
    current_packet.A2021 = 4
    current_packet.A2022 = 5
    current_packet.A2023 = 6
    return current_packet

def test_map_ended(): # 1:1
    current_packet = packet.MapEnded()
    return current_packet

def test_create_ambient_sound(): # 1:1
    current_packet = packet.CreateAmbientSound()
    current_packet.loop_id = 5
    current_packet.name = "test"
    current_packet.points = [(1,2,3)]
    return current_packet

def test_fog_color(): # 1:1
    current_packet = packet.FogColor()
    current_packet.color = 16711937

    
    return current_packet



def test_packets():
    current_packet = test_fog_color()

    writer = ByteWriter()
    current_packet.write(writer)
    print("Raw output:")
    print(str(writer))
    print("Hex output:")
    print(toHex(str(writer)))
    # Remove first byte from the writer (packet ID)
    writer_data = str(writer)
    if len(writer_data) > 1:
        writer_data = writer_data[1:]  # Skip the first byte (packet ID)
    reader = ByteReader(writer_data)
    current_packet = packet.FogColor(reader)
    print("Raw object output:")
    
    # Dump all attributes of the object
    print("\nComplete object dump:")
    
    # Get all attributes using dir()
    all_attrs = dir(current_packet)
    for attr in all_attrs:
        # Skip private attributes and methods
        if not attr.startswith('_'):
            try:
                value = getattr(current_packet, attr)
                # Skip methods and only print data attributes
                if not callable(value):
                    print("{}: {}".format(attr, value))
            except:
                print("{}: <error retrieving value>".format(attr))

test_packets()
# 88/125