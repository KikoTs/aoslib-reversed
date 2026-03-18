"""
Compare raw packet bytes between py2 and py3.
Run with: py2 compare_packets.py > py2_hex.txt
          py  compare_packets.py > py3_hex.txt
Then diff the two files.
"""
import sys, os

if sys.version_info[0] < 3:
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'aosdump'))
else:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import shared.packet as packet
from shared.bytes import ByteWriter, ByteReader

def to_hex(data):
    if sys.version_info[0] < 3:
        return ' '.join(['%02x' % ord(b) for b in str(data)])
    else:
        return ' '.join(['%02x' % b for b in bytes(data)])

def write_packet(p):
    w = ByteWriter()
    p.write(w)
    return w

def test_and_print(name, setup_fn):
    try:
        p = setup_fn()
        w = write_packet(p)
        raw = str(w) if sys.version_info[0] < 3 else bytes(w)
        print("%s|%d|%s" % (name, len(raw), to_hex(raw)))
    except Exception as e:
        print("%s|ERROR|%s" % (name, str(e)))

# SetHP
def s_set_hp():
    p = packet.SetHP()
    p.source_x = 1.1
    p.source_y = 1.2
    p.source_z = 1.3
    p.hit_type = 1
    p.value = 2
    p.player_id = 3
    return p

# HitEntity
def s_hit_entity():
    p = packet.HitEntity()
    p.entity_id = 1
    p.value = 2
    return p

# HelpMessage
def s_help_message():
    p = packet.HelpMessage()
    p.message = "Test Help"
    p.big = True
    p.duration = 5.0
    return p

# GenericVoteMessage
def s_generic_vote_message():
    p = packet.GenericVoteMessage()
    p.vote_type = 1
    p.vote_value = 2
    p.vote = 3
    p.player_id = 4
    return p

# InitiateKickMessage
def s_initiate_kick_message():
    p = packet.InitiateKickMessage()
    p.player_id = 1
    p.value = 2
    return p

# KillAction
def s_kill_action():
    p = packet.KillAction()
    p.player_id = 1
    p.killer_id = 2
    p.kill_type = 3
    p.respawn_time = 4
    return p

# LockTeam
def s_lock_team():
    p = packet.LockTeam()
    p.team_id = 1
    p.locked = True
    return p

# LockToZone
def s_lock_to_zone():
    p = packet.LockToZone()
    p.zone_id = 1
    p.locked = True
    return p

# ForceTeamJoin
def s_force_team_join():
    p = packet.ForceTeamJoin()
    p.team_id = 1
    return p

# ForceShowScores
def s_force_show_scores():
    p = packet.ForceShowScores()
    p.show = True
    return p

# Restock
def s_restock():
    p = packet.Restock()
    p.player_id = 1
    return p

# ReqestUGCEntities
def s_reqest_ugc_entities():
    p = packet.ReqestUGCEntities()
    return p

# PrefabComplete
def s_prefab_complete():
    p = packet.PrefabComplete()
    p.player_id = 1
    return p

# PlayerLeft
def s_player_left():
    p = packet.PlayerLeft()
    p.player_id = 1
    return p

# ChangeClass
def s_change_class():
    p = packet.ChangeClass()
    p.player_id = 1
    p.class_id = 2
    return p

# ChangeTeam
def s_change_team():
    p = packet.ChangeTeam()
    p.player_id = 1
    p.team_id = 2
    return p

# ChatMessage
def s_chat_message():
    p = packet.ChatMessage()
    p.chat_type = 1
    p.player_id = 2
    p.value = "Test Chat"
    return p

# SkyboxData
def s_skybox_data():
    p = packet.SkyboxData()
    p.filename = "sky.png"
    return p

# ShowTextMessage
def s_show_text_message():
    p = packet.ShowTextMessage()
    p.message = "Test Message"
    p.big = True
    p.duration = 5.0
    return p

# StopMusic
def s_stop_music():
    p = packet.StopMusic()
    return p

# StopSound
def s_stop_sound():
    p = packet.StopSound()
    p.name = "test_sound"
    return p

# TeamInfiniteBlocks
def s_team_infinite_blocks():
    p = packet.TeamInfiniteBlocks()
    p.team_id = 1
    p.infinite = True
    return p

# TeamLockClass
def s_team_lock_class():
    p = packet.TeamLockClass()
    p.team_id = 1
    p.locked = True
    return p

# TeamLockScore
def s_team_lock_score():
    p = packet.TeamLockScore()
    p.team_id = 1
    p.locked = True
    return p

# TeamMapVisibility
def s_team_map_visibility():
    p = packet.TeamMapVisibility()
    p.team_id = 1
    p.visible = True
    return p

# UseCommand
def s_use_command():
    p = packet.UseCommand()
    p.player_id = 1
    p.value = 2
    return p

# WeaponReload
def s_weapon_reload():
    p = packet.WeaponReload()
    p.player_id = 1
    p.clip_ammo = 2
    p.reserve_ammo = 3
    return p

# SetScore
def s_set_score():
    p = packet.SetScore()
    p.team_id = 1
    p.score = 2
    return p

# Password
def s_password():
    p = packet.Password()
    p.password = "test"
    return p

# PasswordNeeded
def s_password_needed():
    p = packet.PasswordNeeded()
    return p

# PasswordProvided
def s_password_provided():
    p = packet.PasswordProvided()
    p.password = "test"
    return p

# TimeScale
def s_time_scale():
    p = packet.TimeScale()
    p.value = 1.5
    return p

# SetClassLoadout
def s_set_class_loadout():
    p = packet.SetClassLoadout()
    p.player_id = 1
    p.class_id = 2
    p.items = [1, 2, 3]
    return p

# ClockSync
def s_clock_sync():
    p = packet.ClockSync()
    p.value = 1
    return p

# DestroyEntity
def s_destroy_entity():
    p = packet.DestroyEntity()
    p.entity_id = 1
    return p

# DisableEntity
def s_disable_entity():
    p = packet.DisableEntity()
    p.entity_id = 1
    return p

# ExplodeCorpse
def s_explode_corpse():
    p = packet.ExplodeCorpse()
    p.player_id = 1
    return p

# DisplayCountdown
def s_display_countdown():
    p = packet.DisplayCountdown()
    p.value = "5"
    return p

# PlaceMG
def s_place_mg():
    p = packet.PlaceMG()
    p.loop_count = 1
    p.x = 2
    p.y = 3
    p.z = 4
    p.yaw = 5.0
    return p

# PlaceMedPack
def s_place_med_pack():
    p = packet.PlaceMedPack()
    p.loop_count = 1
    p.x = 2
    p.y = 3
    p.z = 4
    return p

# PlaceRadarStation
def s_place_radar_station():
    p = packet.PlaceRadarStation()
    p.loop_count = 1
    p.x = 2
    p.y = 3
    p.z = 4
    return p

# PlaceRocketTurret
def s_place_rocket_turret():
    p = packet.PlaceRocketTurret()
    p.loop_count = 1
    p.x = 2
    p.y = 3
    p.z = 4
    p.yaw = 5.0
    return p

# PlaceUGC
def s_place_ugc():
    p = packet.PlaceUGC()
    p.loop_count = 1
    p.player_id = 2
    p.ugc_item_id = 3
    p.x = 4
    p.y = 5
    p.z = 6
    return p

# PickPickup
def s_pick_pickup():
    p = packet.PickPickup()
    p.loop_count = 1
    return p

# PlaceC4
def s_place_c4():
    p = packet.PlaceC4()
    p.loop_count = 1
    p.x = 2
    p.y = 3
    p.z = 4
    return p

# PlaceDynamite
def s_place_dynamite():
    p = packet.PlaceDynamite()
    p.loop_count = 1
    p.x = 2
    p.y = 3
    p.z = 4
    return p

# PlaceFlareBlock
def s_place_flare_block():
    p = packet.PlaceFlareBlock()
    p.loop_count = 1
    p.x = 2
    p.y = 3
    p.z = 4
    return p

# PlaceLandmine
def s_place_landmine():
    p = packet.PlaceLandmine()
    p.loop_count = 1
    p.player_id = 2
    p.x = 3
    p.y = 4
    p.z = 5
    return p

# PlayAmbientSound
def s_play_ambient_sound():
    p = packet.PlayAmbientSound()
    p.name = "ambient1"
    p.loop_id = 1
    p.looping = True
    p.positioned = True
    p.volume = 1.0
    p.time = 2.0
    p.attenuation = 3.0
    p.x = 4.0
    p.y = 5.0
    p.z = 6.0
    return p

# PlayMusic
def s_play_music():
    p = packet.PlayMusic()
    p.name = "music1"
    p.loop = True
    return p

# PlaySound
def s_play_sound():
    p = packet.PlaySound()
    p.name = "sound1"
    p.looping = True
    p.positioned = True
    p.volume = 1.0
    p.x = 2.0
    p.y = 3.0
    p.z = 4.0
    return p

# UGCMessage
def s_ugc_message():
    p = packet.UGCMessage()
    p.message_id = 1
    return p

# UGCMapInfo
def s_ugc_map_info():
    p = packet.UGCMapInfo()
    p.png_data = b"test_png_data"
    return p

# UGCMapLoadingFromHost
def s_ugc_map_loading_from_host():
    p = packet.UGCMapLoadingFromHost()
    p.percent_complete = 50
    return p

# UGCObjectives
def s_ugc_objectives():
    p = packet.UGCObjectives()
    p.data = "objective data"
    return p

# TeamProgress
def s_team_progress():
    p = packet.TeamProgress()
    p.team1_progress = 0.5
    p.team2_progress = 0.75
    return p

# AddServer
def s_add_server():
    p = packet.AddServer()
    p.count = 1
    return p

# BlockBuild
def s_block_build():
    p = packet.BlockBuild()
    p.player_id = 1
    p.x = 2
    p.y = 3
    p.z = 4
    return p

# BlockLine
def s_block_line():
    p = packet.BlockLine()
    p.player_id = 1
    p.x1 = 2
    p.y1 = 3
    p.z1 = 4
    p.x2 = 5
    p.y2 = 6
    p.z2 = 7
    return p

# BlockLiberate
def s_block_liberate():
    p = packet.BlockLiberate()
    p.loop_count = 1
    p.x = 2
    p.y = 3
    p.z = 4
    return p

# BlockOccupy
def s_block_occupy():
    p = packet.BlockOccupy()
    p.loop_count = 1
    p.x = 2
    p.y = 3
    p.z = 4
    return p

# BlockSuckerPacket
def s_block_sucker_packet():
    p = packet.BlockSuckerPacket()
    p.loop_count = 1
    p.x = 2
    p.y = 3
    p.z = 4
    return p

# ChangePlayer
def s_change_player():
    p = packet.ChangePlayer()
    p.player_id = 1
    p.team_id = 2
    p.weapon_id = 3
    return p

# ClientInMenu
def s_client_in_menu():
    p = packet.ClientInMenu()
    p.value = True
    return p

# DetonateC4
def s_detonate_c4():
    p = packet.DetonateC4()
    p.loop_count = 1
    return p

# DisguisePacket
def s_disguise_packet():
    p = packet.DisguisePacket()
    p.player_id = 1
    p.other_id = 2
    return p

# POIFocus
def s_poifocus():
    p = packet.POIFocus()
    p.entity_id = 1
    p.player_id = 2
    return p

# DropPickup
def s_drop_pickup():
    p = packet.DropPickup()
    p.loop_count = 1
    p.player_id = 2
    return p

# DebugDraw
def s_debug_draw():
    p = packet.DebugDraw()
    p.type = 1
    p.x = 2.0
    p.y = 3.0
    p.z = 4.0
    p.x2 = 5.0
    p.y2 = 6.0
    p.z2 = 7.0
    p.color = (255, 0, 0)
    p.size = 8.0
    p.duration = 9.0
    return p

# VoiceData
def s_voice_data():
    p = packet.VoiceData()
    p.player_id = 1
    p.data = b"voice_data"
    return p

# SteamSessionTicket
def s_steam_session_ticket():
    p = packet.SteamSessionTicket()
    p.data = b"ticket_data"
    return p

# RankUps
def s_rank_ups():
    p = packet.RankUps()
    p.player_id = 1
    p.rank = 2
    p.xp = 3
    return p

# ShowGameStats
def s_show_game_stats():
    p = packet.ShowGameStats()
    return p

# ShootResponse
def s_shoot_response():
    p = packet.ShootResponse()
    p.player_id = 1
    p.value = 2
    p.x = 3.0
    p.y = 4.0
    p.z = 5.0
    return p

# ShootPacket
def s_shoot_packet():
    p = packet.ShootPacket()
    p.shooter_id = 1
    p.shot_on_world_update = 2
    p.ori_x = 3.0
    p.ori_y = 4.0
    p.ori_z = 5.0
    p.dir_x = 6.0
    p.dir_y = 7.0
    p.dir_z = 8.0
    p.penetration = 9
    p.secondary = 10
    p.seed = 11
    return p  

# SetUGCEditMode
def s_set_ugc_edit_mode():
    p = packet.SetUGCEditMode()
    p.mode = 1
    return p

# ShootFeedbackPacket
def s_shoot_feedback_packet():
    p = packet.ShootFeedbackPacket()
    p.hit_type = 1
    p.value = 2
    return p

# PackResponse
def s_pack_response():
    p = packet.PackResponse()
    p.status = 1
    return p

# PackStart
def s_pack_start():
    p = packet.PackStart()
    p.data = b"pack_data"
    return p

# MinimapBillboard
def s_minimap_billboard():
    p = packet.MinimapBillboard()
    p.billboard_id = 1
    p.x = 2
    p.y = 3
    p.color = (255, 0, 0)
    return p

# MinimapBillboardClear
def s_minimap_billboard_clear():
    p = packet.MinimapBillboardClear()
    p.billboard_id = 1
    return p

# MinimapZone
def s_minimap_zone():
    p = packet.MinimapZone()
    p.zone_id = 1
    p.x = 2
    p.y = 3
    p.width = 4
    p.height = 5
    p.color = (255, 0, 0)
    return p

# MinimapZoneClear
def s_minimap_zone_clear():
    p = packet.MinimapZoneClear()
    p.zone_id = 1
    return p

# MapEnded
def s_map_ended():
    p = packet.MapEnded()
    p.value = 1
    return p

# CreateAmbientSound
def s_create_ambient_sound():
    p = packet.CreateAmbientSound()
    p.name = "amb1"
    p.x = 1.0
    p.y = 2.0
    p.z = 3.0
    p.volume = 4.0
    p.attenuation = 5.0
    return p

# FogColor
def s_fog_color():
    p = packet.FogColor()
    p.color = (255, 128, 0)
    return p

# BlockBuildColored
def s_block_build_colored():
    p = packet.BlockBuildColored()
    p.player_id = 1
    p.x = 2
    p.y = 3
    p.z = 4
    p.color = (255, 128, 64)
    return p

# UseOrientedItem
def s_use_oriented_item():
    p = packet.UseOrientedItem()
    p.player_id = 1
    p.tool = 2
    p.value = 3
    p.x = 4.0
    p.y = 5.0
    p.z = 6.0
    p.ori_x = 7.0
    p.ori_y = 8.0
    p.ori_z = 9.0
    return p

# TerritoryBaseState
def s_territory_base_state():
    p = packet.TerritoryBaseState()
    p.entity_id = 1
    p.team = 2
    p.capturing_team = 3
    p.capture_progress = 0.5
    return p

# SetColor
def s_set_color():
    p = packet.SetColor()
    p.player_id = 1
    p.color = (255, 128, 64)
    return p

# SetGroundColors
def s_set_ground_colors():
    p = packet.SetGroundColors()
    p.color1 = (255, 0, 0)
    p.color2 = (0, 255, 0)
    p.color3 = (0, 0, 255)
    p.color4 = (255, 255, 0)
    return p

# Damage
def s_damage():
    p = packet.Damage()
    p.player_id = 1
    p.value = 2
    p.kill_type = 3
    p.killer_id = 4
    return p

# ProgressBar
def s_progress_bar():
    p = packet.ProgressBar()
    p.progress = 1.0
    p.rate = 1.0
    p.color1 = (1, 2, 3)
    p.color2 = (4, 5, 6)
    p.stopped = True
    return p

# MapDataValidation
def s_map_data_validation():
    try:
        p = packet.MapDataValidation()
    except AttributeError:
        p = packet.AosMapValidation()
    p.crc = 12345
    return p

# CreatePlayer
def s_create_player():
    p = packet.CreatePlayer()
    p.player_id = 1
    p.name = "TestPlayer"
    p.team_id = 2
    return p

# PaintBlockPacket
def s_paint_block():
    p = packet.PaintBlockPacket()
    p.player_id = 1
    p.x = 2
    p.y = 3
    p.z = 4
    p.color = (255, 128, 64)
    return p

# LocalisedMessage
def s_localised_message():
    p = packet.LocalisedMessage()
    p.message_id = 1
    p.args = ["arg1", "arg2"]
    return p

# BuildPrefabAction
def s_build_prefab_action():
    p = packet.BuildPrefabAction()
    p.loop_count = 1
    p.player_id = 2
    p.prefab_name = "test_prefab"
    p.x = 3
    p.y = 4
    p.z = 5
    p.yaw = 6
    return p

# MapDataChunk
def s_map_data_chunk():
    try:
        p = packet.MapDataChunk()
    except Exception:
        p = packet.AosMapChunk()
    p.data = b"test"
    p.percent_complete = 1
    return p

# MapDataEnd
def s_map_data_end():
    try:
        p = packet.MapDataEnd()
    except Exception:
        p = packet.AosMapEnd()
    return p

# MapDataStart
def s_map_data_start():
    try:
        p = packet.MapDataStart()
    except Exception:
        p = packet.AosMapStart()
    return p

# ExistingPlayer
def s_existing_player():
    p = packet.ExistingPlayer()
    p.player_id = 1
    p.name = "TestPlayer"
    p.team_id = 2
    p.weapon_id = 3
    p.loadout = [1, 2, 3]
    p.kills = 4
    p.deaths = 5
    p.class_id = 6
    return p

# NewPlayerConnection
def s_new_player_connection():
    p = packet.NewPlayerConnection()
    p.player_id = 1
    p.name = "NewPlayer"
    p.version = 314
    return p

# GameStats
def s_game_stats():
    p = packet.GameStats()
    return p

# ClientData
def s_client_data():
    p = packet.ClientData()
    p.player_id = 1
    p.x = 2.0
    p.y = 3.0
    p.z = 4.0
    p.ori_x = 5.0
    p.ori_y = 6.0
    p.ori_z = 7.0
    p.up = True
    p.down = False
    p.left = True
    p.right = False
    p.jump = True
    p.crouch = False
    p.sneak = True
    p.sprint = False
    return p

# StateData - simple version with minimal fields
def s_state_data():
    p = packet.StateData()
    p.player_id = 1
    p.fog_color = (128, 128, 128)
    p.team1_color = (255, 0, 0)
    p.team2_color = (0, 0, 255)
    p.team1_name = "Team1"
    p.team2_name = "Team2"
    p.gravity = 9.8
    p.time_scale = 1.0
    p.score_limit = 100
    p.mode_type = 1
    return p

all_packets = [
    ("SetHP", s_set_hp),
    ("HitEntity", s_hit_entity),
    ("HelpMessage", s_help_message),
    ("GenericVoteMessage", s_generic_vote_message),
    ("InitiateKickMessage", s_initiate_kick_message),
    ("KillAction", s_kill_action),
    ("LockTeam", s_lock_team),
    ("LockToZone", s_lock_to_zone),
    ("ForceTeamJoin", s_force_team_join),
    ("ForceShowScores", s_force_show_scores),
    ("Restock", s_restock),
    ("ReqestUGCEntities", s_reqest_ugc_entities),
    ("PrefabComplete", s_prefab_complete),
    ("PlayerLeft", s_player_left),
    ("ChangeClass", s_change_class),
    ("ChangeTeam", s_change_team),
    ("ChatMessage", s_chat_message),
    ("SkyboxData", s_skybox_data),
    ("ShowTextMessage", s_show_text_message),
    ("StopMusic", s_stop_music),
    ("StopSound", s_stop_sound),
    ("TeamInfiniteBlocks", s_team_infinite_blocks),
    ("TeamLockClass", s_team_lock_class),
    ("TeamLockScore", s_team_lock_score),
    ("TeamMapVisibility", s_team_map_visibility),
    ("UseCommand", s_use_command),
    ("WeaponReload", s_weapon_reload),
    ("SetScore", s_set_score),
    ("Password", s_password),
    ("PasswordNeeded", s_password_needed),
    ("PasswordProvided", s_password_provided),
    ("TimeScale", s_time_scale),
    ("SetClassLoadout", s_set_class_loadout),
    ("ClockSync", s_clock_sync),
    ("DestroyEntity", s_destroy_entity),
    ("DisableEntity", s_disable_entity),
    ("ExplodeCorpse", s_explode_corpse),
    ("DisplayCountdown", s_display_countdown),
    ("PlaceMG", s_place_mg),
    ("PlaceMedPack", s_place_med_pack),
    ("PlaceRadarStation", s_place_radar_station),
    ("PlaceRocketTurret", s_place_rocket_turret),
    ("PlaceUGC", s_place_ugc),
    ("PickPickup", s_pick_pickup),
    ("PlaceC4", s_place_c4),
    ("PlaceDynamite", s_place_dynamite),
    ("PlaceFlareBlock", s_place_flare_block),
    ("PlaceLandmine", s_place_landmine),
    ("PlayAmbientSound", s_play_ambient_sound),
    ("PlayMusic", s_play_music),
    ("PlaySound", s_play_sound),
    ("UGCMessage", s_ugc_message),
    ("UGCMapInfo", s_ugc_map_info),
    ("UGCMapLoadingFromHost", s_ugc_map_loading_from_host),
    ("UGCObjectives", s_ugc_objectives),
    ("TeamProgress", s_team_progress),
    ("AddServer", s_add_server),
    ("BlockBuild", s_block_build),
    ("BlockLine", s_block_line),
    ("BlockLiberate", s_block_liberate),
    ("BlockOccupy", s_block_occupy),
    ("BlockSuckerPacket", s_block_sucker_packet),
    ("ChangePlayer", s_change_player),
    ("ClientInMenu", s_client_in_menu),
    ("DetonateC4", s_detonate_c4),
    ("DisguisePacket", s_disguise_packet),
    ("POIFocus", s_poifocus),
    ("DropPickup", s_drop_pickup),
    ("DebugDraw", s_debug_draw),
    ("VoiceData", s_voice_data),
    ("SteamSessionTicket", s_steam_session_ticket),
    ("RankUps", s_rank_ups),
    ("ShowGameStats", s_show_game_stats),
    ("ShootResponse", s_shoot_response),
    ("ShootPacket", s_shoot_packet),
    ("SetUGCEditMode", s_set_ugc_edit_mode),
    ("ShootFeedbackPacket", s_shoot_feedback_packet),
    ("PackResponse", s_pack_response),
    ("PackStart", s_pack_start),
    ("MinimapBillboard", s_minimap_billboard),
    ("MinimapBillboardClear", s_minimap_billboard_clear),
    ("MinimapZone", s_minimap_zone),
    ("MinimapZoneClear", s_minimap_zone_clear),
    ("MapEnded", s_map_ended),
    ("CreateAmbientSound", s_create_ambient_sound),
    ("FogColor", s_fog_color),
    ("BlockBuildColored", s_block_build_colored),
    ("UseOrientedItem", s_use_oriented_item),
    ("TerritoryBaseState", s_territory_base_state),
    ("SetColor", s_set_color),
    ("SetGroundColors", s_set_ground_colors),
    ("Damage", s_damage),
    ("ProgressBar", s_progress_bar),
    ("MapDataValidation", s_map_data_validation),
    ("CreatePlayer", s_create_player),
    ("PaintBlockPacket", s_paint_block),
    ("LocalisedMessage", s_localised_message),
    ("BuildPrefabAction", s_build_prefab_action),
    ("MapDataChunk", s_map_data_chunk),
    ("MapDataEnd", s_map_data_end),
    ("MapDataStart", s_map_data_start),
    ("ExistingPlayer", s_existing_player),
    ("NewPlayerConnection", s_new_player_connection),
    ("GameStats", s_game_stats),
    ("ClientData", s_client_data),
]

for name, fn in all_packets:
    test_and_print(name, fn)
