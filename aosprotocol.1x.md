# Ace of Spades 1.x Protocol Documentation (Work in progress)

This page documents the Ace of Spades 1.x protocol.

## Table of Contents
- [Data Types](#data-types)
- [Packets](#packets)
  - [Clock Sync (0)](#clock-sync)
  - [World Update (1)](#world-update)
  - [Place Dynamite (2) (work in progress)](#place-dynamite)
  - [Entity Updates (3) (work in progress)](#entity-updates)
  - [Client Data (4)](#client-data)
  - [Set HP (5)](#set-hp)
  - [Shoot Packet (6)](#shoot-packet)
  - [Paint Block (7)](#paint-block)
  - [Shoot Feedback (8)](#shoot-feedback)
  - [Shoot Response (9)](#shoot-response)
  - [Use Oriented Item (10)](#use-oriented-item)
  - [Set Color (11)](#set-color)
  - [Set UGC Edit Mode (12)](#set-ugc-edit-mode)
  - [Set Class Loadout (13)](#set-class-loadout)
  - [Existing Player (14)](#existing-player)
  - [New Player Connection (15)](#new-player-connection)
  - [Change Entity (16) (work in progress)](#change-entity)
  - [Change Player (17)](#change-player)
  - [POI Focus (18)](#poi-focus)
  - [Destroy Entity (19)](#destroy-entity)
  - [Hit Entity (20)](#hit-entity)
  - [Create Entity (21) (work in progress)](#create-entity)
  - [Create Ambient Sound (22)](#create-ambient-sound)
  - [Play Sound (23)](#play-sound)
  - [Play Ambient Sound (24)](#play-ambient-sound)
  - [Stop Sound (25)](#stop-sound)
  - [Play Music (26)](#play-music)
  - [Stop Music (27)](#stop-music)
  - [Create Player (28)](#create-player)
  - [Prefab Complete (29)](#prefab-complete)
  - [Build Prefab Action (30)](#build-prefab-action)
  - [Erase Prefab Action (31) (work in progress)](#erase-prefab-action)
  - [Block Build (32)](#block-build)
  - [Block Build Colored (33)](#block-build-colored)
  - [Block Occupy (34)](#block-occupy)
  - [Block Liberate (35)](#block-liberate)
  - [Explode Corpse (36)](#explode-corpse)
  - [Damage (37)](#damage)
  - [Block Manager State (38) (work in progress)](#block-manager-state)
  - [ServerBlockAction (39) (work in progress)](#server-block-action)
  - [Block Line (40)](#block-line)
  - [Minimap Billboard (41)](#minimap-billboard)
  - [Minimap Billboard Clear (42)](#minimap-billboard-clear)
  - [Minimap Zone (43)](#minimap-zone)
  - [Minimap Zone Clear (44)](#minimap-zone-clear)
  - [State Data (45)](#state-data)
  - [Kill Action (46)](#kill-action)
  - [Instantiate Kick Message (48)](#instantiate-kick-message)
  - [Chat Message (49)](#chat-message)
  - [Localised Message (50)](#localised-message)
  - [SkyBox Data (51)](#skybox-data)
  - [Show Game Stats (53)](#show-game-stats)
  - [Map Data Start (54)](#map-data-start)
  - [Map Sync Start (55)](#map-sync-start)
  - [Map Data Chunk (56)](#map-data-chunk)
  - [Map Sync Chunk (57)](#map-sync-chunk)
  - [Map Data End (58)](#map-data-end)
  - [Map Sync End (59)](#map-sync-end)
  - [Map Data Validation (60)](#map-data-validation)
  - [Pack Start (61)](#pack-start)
  - [Pack Response (62)](#pack-response)
  - [Pack Chunk (63)](#pack-chunk)
  - [Player Left (64)](#player-left)
  - [Progress Bar (65)](#progress-bar)
  - [Rank Ups (66)](#rank-ups)
  - [Game Stats (67)](#game-stats)
  - [UGC Objectives (68)](#ugc-objectives)
  - [Restock (69)](#restock)
  - [Pick Pickup (70)](#pick-pickup)
  - [Drop Pickup (71)](#drop-pickup)
  - [Force Show Scores (72)](#force-show-scores)
  - [Show Text Message (73)](#show-text-message)
  - [Fog Color (74)](#fog-color)
  - [Time Scale (75)](#time-scale)
  - [Weapon Reload (76)](#weapon-reload)
  - [Change Team (77)](#change-team)
  - [Change Class (78)](#change-class)
  - [Lock Team (79)](#lock-team)
  - [Team Lock Class (80)](#team-lock-class)
  - [Team Lock Score (81)](#team-lock-score)
  - [Team Infinite Blocks (82)](#team-infinite-blocks)
  - [Team Map Visibility (83)](#team-map-visibility)
  - [Display Countdown (84)](#display-countdown)
  - [Set Score (85)](#set-score)
  - [Use Command (86)](#use-command)
  - [Place MG (87)](#place-mg)
  - [Place Rocket Turret (88)](#place-rocket-turret)
  - [Place Landmine (89)](#place-landmine)
  - [Place Medpack (90)](#place-medpack)
  - [Place Radar Station (91)](#place-radar-station)
  - [Place C4 (92)](#place-c4)
  - [Detonate C4 (93)](#detonate-c4)
  - [Block Sucker (94)](#block-sucker)
  - [Disguise (95)](#disguise)
  - [Disable Entity (96)](#disable-entity)
  - [Place UGC (97)](#place-ugc)
  - [Initial UGC Batch (98) (work in progress)](#initial-ugc-batch)
  - [Request UGC Entities (99)](#request-ugc-entities)
  - [UGC Message (100)](#ugc-message)
  - [UGC Map Loading From Host (101)](#ugc-map-loading-from-host)
  - [UGC Map Info (102)](#ugc-map-info)
  - [Voice Data (103)](#voice-data)
  - [Place Flare Block (104)](#place-flare-block)
  - [Steam Session Ticket (105)](#steam-session-ticket)
  - [Territory Base State (106)](#territory-base-state)
  - [Debug Draw (107)](#debug-draw)
  - [Lock To Zone (108)](#lock-to-zone)
  - [Generic Vote Message (109)](#generic-vote-message)
  - [Help Message (109)](#help-message)
  - [Client In Menu (110)](#client-in-menu)
  - [Password (111)](#password)
  - [Password Needed (112)](#password-needed)
  - [Password Provided (113)](#password-provided)
  - [Initial Info (114)](#initial-info)
  - [Force Team Join (115)](#force-team-join)
  - [Position Data (116) (work in progress)](#position-data)
  - [Team Progress (117)](#team-progress)
  - [Set Ground Colors (118)](#set-ground-colors)

## Data Types

The protocol uses various data types for field values:

| Type | Description |
|------|-------------|
| byte | Unsigned 8-bit integer (0-255) |
| short | Signed 16-bit integer (-32,768 to 32,767) |
| int | Signed 32-bit integer (-2,147,483,648 to 2,147,483,647) |
| float | 32-bit floating point number |
| string | Text string, prefixed with length |
| fixed | Fixed-point number, stored as a short (value/64.0) |
| color | RGB color value, stored as 3 bytes or as a tuple (r,g,b) |
| orientation | Special fixed-point representation for angles |
| boolean | Stored as a byte (0 = false, 1 = true) |
| byte_float | 1-byte fixed-point float where each bit represents 0.25 |
| position | Tuple of 3 coordinate values (x, y, z) |
| uint64 | Unsigned 64-bit integer (for Steam IDs) |

## Packets

### Clock Sync
| Property | Value |
|-----------|-------|
| Packet ID | 0 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| client_time | int | Current client timestamp |
| server_loop_count | int | Server loop count for synchronization |

### Place Dynamite
| Property | Value |
|-----------|-------|
| Packet ID | 1 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| loop_count | int | Current game loop count |
| x | short | X coordinate of dynamite placement |
| y | short | Y coordinate of dynamite placement |
| z | short | Z coordinate of dynamite placement |
| face | byte | Face of the block where dynamite is placed |

### Client Data
| Property | Value |
|-----------|-------|
| Packet ID | 4 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| loop_count | int | Current game loop count |
| player_id | byte | ID of the player (high bit = palette_enabled) |
| tool_id | byte | Currently selected tool ID |
| o_x | orientation | X orientation (pitch) |
| o_y | orientation | Y orientation (yaw) |
| o_z | orientation | Z orientation (roll) |
| ooo | byte | Unknown purpose |
| up | boolean | Movement key: up pressed |
| down | boolean | Movement key: down pressed |
| left | boolean | Movement key: left pressed |
| right | boolean | Movement key: right pressed |
| jump | boolean | Jump key pressed |
| crouch | boolean | Crouch key pressed |
| sneak | boolean | Sneak key pressed |
| sprint | boolean | Sprint key pressed |
| primary | boolean | Primary action button pressed |
| secondary | boolean | Secondary action button pressed |
| zoom | boolean | Zoom key pressed |
| can_pickup | boolean | Whether player can pickup items |
| can_display_weapon | boolean | Whether weapon can be displayed |
| is_on_fire | boolean | Whether player is on fire |
| is_weapon_deployed | boolean | Whether weapon is deployed |
| hover | boolean | Whether player is hovering |
| weapon_deployment_yaw | orientation | Yaw angle of deployed weapon |

### Set HP
| Property | Value |
|-----------|-------|
| Packet ID | 5 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| hp | byte | Current health points |
| damage_type | byte | Type of damage received |
| source_x | fixed | X coordinate of damage source |
| source_y | fixed | Y coordinate of damage source |
| source_z | fixed | Z coordinate of damage source |

### Shoot Packet
| Property | Value |
|-----------|-------|
| Packet ID | 6 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| loop_count | int | Current game loop count |
| shooter_id | byte | ID of the player shooting |
| shot_on_world_update | int | World update number when shot occurred |
| x | float | X coordinate of shot origin |
| y | float | Y coordinate of shot origin |
| z | float | Z coordinate of shot origin |
| ori_x | float | X direction of shot |
| ori_y | float | Y direction of shot |
| ori_z | float | Z direction of shot |
| damage | short | Damage value of the shot |
| penetration | short | Penetration value of the shot |
| secondary | byte | Whether it's a secondary fire mode |
| seed | byte | Random seed for shot effects |

### Paint Block
| Property | Value |
|-----------|-------|
| Packet ID | 7 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| loop_count | int | Current game loop count |
| x | short | X coordinate of block |
| y | short | Y coordinate of block |
| z | short | Z coordinate of block |
| color | color | RGB color to paint the block |

### Shoot Feedback
| Property | Value |
|-----------|-------|
| Packet ID | 8 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| loop_count | int | Current game loop count |
| shooter_id | byte | ID of the player shooting |
| tool_id | byte | Tool used for shooting |
| shot_on_world_update | int | World update number when shot occurred |
| seed | byte | Random seed for shot effects |

### Shoot Response
| Property | Value |
|-----------|-------|
| Packet ID | 9 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| damage_by | byte | ID of player causing damage |
| damaged | byte | ID of player receiving damage |
| blood | byte | Amount of blood to show |
| position_x | fixed | X position of hit effect |
| position_y | fixed | Y position of hit effect |
| position_z | fixed | Z position of hit effect |

### Use Oriented Item
| Property | Value |
|-----------|-------|
| Packet ID | 10 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| loop_count | int | Current game loop count |
| player_id | byte | ID of the player using the item |
| tool | byte | Tool ID being used |
| value | fixed | Tool-specific value |
| position | position | Position (x,y,z) where item is used |
| velocity | position | Velocity (x,y,z) of the used item |

### Set Color
| Property | Value |
|-----------|-------|
| Packet ID | 11 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| player_id | byte | ID of the player |
| value | color | RGB color value for the player |

### Set UGC Edit Mode
| Property | Value |
|-----------|-------|
| Packet ID | 12 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| mode | byte | UGC edit mode value |

### Set Class Loadout
| Property | Value |
|-----------|-------|
| Packet ID | 13 |
| Compression | Yes |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| player_id | byte | ID of the player |
| class_id | byte | Class ID being set |
| instant | byte | Whether change is immediate |
| loadout | list[byte] | List of loadout items |
| prefabs | list[string] | List of available prefabs |
| ugc_tools | list[byte] | List of UGC tools |

### Existing Player
| Property | Value |
|-----------|-------|
| Packet ID | 14 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| player_id | byte | ID of the player |
| demo_player | byte | Whether player is a demo player |
| team | byte | Team ID (0=spectator, 1=blue, 2=green) |
| class_id | byte | Player's class ID |
| tool | byte | Currently equipped tool |
| pickup | byte | Currently held pickup |
| dead | byte | Whether player is dead |
| score | int | Player's score |
| forced_team | byte | Whether team was forced |
| local_language | byte | Player's language ID |
| color | color | Player's color (RGB) |
| name | string | Player's name |
| loadout | list[byte] | List of player's loadout items |
| prefabs | list[string] | List of player's available prefabs |

### New Player Connection
| Property | Value |
|-----------|-------|
| Packet ID | 15 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| team | byte | Team ID (0=spectator, 1=blue, 2=green) |
| class_id | byte | Player's class ID |
| forced_team | byte | Whether team was forced |
| local_language | byte | Player's language ID |
| name | string | Player's name |

### Change Player
| Property | Value |
|-----------|-------|
| Packet ID | 17 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| player_id | short | ID of the player to change |
| type | byte | Type of change to apply |
| high_minimap_visibility | byte | Minimap visibility level (only if type=8) |
| chase_cam | byte | Enable chase camera (only if type=9) |

### POI Focus
| Property | Value |
|-----------|-------|
| Packet ID | 18 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| target_x | fixed | X coordinate to focus on |
| target_y | fixed | Y coordinate to focus on |
| target_z | fixed | Z coordinate to focus on |

### Destroy Entity
| Property | Value |
|-----------|-------|
| Packet ID | 19 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| entity_id | short | ID of the entity to destroy |

### Hit Entity
| Property | Value |
|-----------|-------|
| Packet ID | 20 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| entity_id | short | ID of the entity being hit |
| x | fixed | X coordinate of hit position |
| y | fixed | Y coordinate of hit position |
| z | fixed | Z coordinate of hit position |
| type | byte | Type of hit |

### Create Ambient Sound
| Property | Value |
|-----------|-------|
| Packet ID | 22 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| name | string | Name of the ambient sound |
| loop_id | int | ID for the sound loop |
| points | list[(short,short,short)] | List of 3D coordinates for sound points |

### Play Sound
| Property | Value |
|-----------|-------|
| Packet ID | 23 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| sound_id | byte | ID of the sound to play |
| looping | boolean | Whether sound loops |
| positioned | boolean | Whether sound is positioned in 3D space |
| volume | fixed | Volume level |
| time | fixed | Playback time |
| loop_id | byte | ID for the sound loop (if looping) |
| x | fixed | X coordinate of sound (if positioned) |
| y | fixed | Y coordinate of sound (if positioned) |
| z | fixed | Z coordinate of sound (if positioned) |
| attenuation | fixed | Sound attenuation (if positioned) |

### Play Ambient Sound
| Property | Value |
|-----------|-------|
| Packet ID | 24 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| name | string | Name of the ambient sound |
| looping | boolean | Whether sound loops |
| positioned | boolean | Whether sound is positioned in 3D space |
| volume | fixed | Volume level |
| time | fixed | Playback time |
| loop_id | byte | ID for the sound loop (if looping) |
| x | fixed | X coordinate of sound (if positioned) |
| y | fixed | Y coordinate of sound (if positioned) |
| z | fixed | Z coordinate of sound (if positioned) |
| attenuation | fixed | Sound attenuation (if positioned) |

### Stop Sound
| Property | Value |
|-----------|-------|
| Packet ID | 25 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| loop_id | byte | ID of the sound loop to stop |

### Play Music
| Property | Value |
|-----------|-------|
| Packet ID | 26 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| name | string | Name of the music track |
| seconds_played | fixed | Seconds into the track to start playing |

### Stop Music
| Property | Value |
|-----------|-------|
| Packet ID | 27 |
| Compression | No |

No fields for this packet.

### Create Player
| Property | Value |
|-----------|-------|
| Packet ID | 28 |
| Compression | Yes |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| player_id | byte | ID of the player |
| demo_player | byte | Whether player is a demo player |
| class_id | byte | Player's class ID |
| team | byte | Team ID (0=spectator, 1=blue, 2=green) |
| dead | byte | Whether player is dead |
| local_language | byte | Player's language ID |
| x | fixed | X coordinate of player |
| y | fixed | Y coordinate of player |
| z | fixed | Z coordinate of player |
| ori_x | fixed | X orientation (pitch) |
| ori_y | fixed | Y orientation (yaw) |
| ori_z | fixed | Z orientation (roll) |
| name | string | Player's name |
| loadout | list[byte] | List of player's loadout items |
| prefabs | list[string] | List of player's available prefabs |

### Prefab Complete
| Property | Value |
|-----------|-------|
| Packet ID | 29 |
| Compression | No |

No fields for this packet.

### Build Prefab Action
| Property | Value |
|-----------|-------|
| Packet ID | 30 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| loop_count | int | Current game loop count |
| prefab_name | string | Name of the prefab |
| player_id | byte | ID of the player building |
| prefab_yaw | byte | Yaw rotation of prefab |
| prefab_pitch | byte | Pitch rotation of prefab |
| prefab_roll | byte | Roll rotation of prefab |
| from_block_index | int | Starting block index |
| to_block_index | int | Ending block index |
| position | (short,short,short) | Position coordinates (x,y,z) |
| color | color | RGB color for the prefab |
| add_to_user_blocks | boolean | Whether to add to user blocks |

### Block Build
| Property | Value |
|-----------|-------|
| Packet ID | 32 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| loop_count | int | Current game loop count |
| player_id | byte | ID of the player building |
| x | short | X coordinate of block |
| y | short | Y coordinate of block |
| z | short | Z coordinate of block |
| block_type | byte | Type of block being built |

### Block Build Colored
| Property | Value |
|-----------|-------|
| Packet ID | 33 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| loop_count | int | Current game loop count |
| player_id | byte | ID of the player building |
| x | short | X coordinate of block |
| y | short | Y coordinate of block |
| z | short | Z coordinate of block |
| color | color | RGB color of the block |

### Block Occupy
| Property | Value |
|-----------|-------|
| Packet ID | 34 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| loop_count | int | Current game loop count |
| player_id | byte | ID of the player |
| x | short | X coordinate of block |
| y | short | Y coordinate of block |
| z | short | Z coordinate of block |

### Block Liberate
| Property | Value |
|-----------|-------|
| Packet ID | 35 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| loop_count | int | Current game loop count |
| player_id | byte | ID of the player |
| x | short | X coordinate of block |
| y | short | Y coordinate of block |
| z | short | Z coordinate of block |

### Explode Corpse
| Property | Value |
|-----------|-------|
| Packet ID | 36 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| player_id | byte | ID of the player whose corpse explodes |
| show_explosion_effect | byte | Whether to show explosion effect |

### Damage
| Property | Value |
|-----------|-------|
| Packet ID | 37 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| player_id | byte | ID of the player being damaged |
| type | byte | Type of damage |
| damage | byte_float | Amount of damage (1-byte fixed point) |
| face | byte | Face where damage originated |
| chunk_check | byte | Chunk validation value |
| seed | byte | Random seed for damage effects |
| causer_id | short | ID of the entity causing damage |
| position | (float,float,float) | Position where damage occurred |

### Block Line
| Property | Value |
|-----------|-------|
| Packet ID | 40 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| loop_count | int | Current game loop count |
| player_id | byte | ID of the player creating the line |
| x1 | short | Start X coordinate |
| y1 | short | Start Y coordinate |
| z1 | short | Start Z coordinate |
| x2 | short | End X coordinate |
| y2 | short | End Y coordinate |
| z2 | short | End Z coordinate |

### Minimap Billboard
| Property | Value |
|-----------|-------|
| Packet ID | 41 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| entity_id | byte | Entity ID to attach billboard to |
| key | byte | Unique key for this billboard |
| color | color | RGB color of the billboard |
| x | fixed | X coordinate |
| y | fixed | Y coordinate |
| z | fixed | Z coordinate |
| icon_name | string | Name of the icon to display |
| tracking | byte | Whether billboard tracks movement |

### Minimap Billboard Clear
| Property | Value |
|-----------|-------|
| Packet ID | 42 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| entity_id | short | Entity ID whose billboard to clear |

### Minimap Zone
| Property | Value |
|-----------|-------|
| Packet ID | 43 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| key | byte | Unique key for this zone |
| color | color | RGB color of the zone |
| A2018 | short | X min coordinate |
| A2020 | short | Y min coordinate |
| A2022 | short | Z min coordinate |
| A2019 | short | X max coordinate |
| A2021 | short | Y max coordinate |
| A2023 | short | Z max coordinate |
| icon_scale | fixed | Scale of the zone icon |
| icon_id | byte | ID of the icon to display |
| locked_in_zone | byte | Whether player is locked in this zone |

### Minimap Zone Clear
| Property | Value |
|-----------|-------|
| A2018 | short | X min coordinate |
| A2020 | short | Y min coordinate |
| A2022 | short | Z min coordinate |
| A2019 | short | X max coordinate |
| A2021 | short | Y max coordinate |
| A2023 | short | Z max coordinate |

### State Data
| Property | Value |
|-----------|-------|
| Packet ID | 45 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| player_id | byte | ID of the player |
| fog_color | color | RGB color of fog |
| gravity | fixed | Gravity value |
| light_color | color | RGB color of main light |
| light_direction | (fixed,fixed,fixed) | Direction of main light |
| back_light_color | color | RGB color of back light |
| back_light_direction | (fixed,fixed,fixed) | Direction of back light |
| ambient_light_color | color | RGB color of ambient light |
| ambient_light_intensity | fixed | Intensity of ambient light |
| time_scale | fixed | Game time scale |
| score_limit | byte | Current score limit |
| mode_type | byte | Current game mode type |
| team_headcount_type | byte | Team headcount type |
| team1_name | string | Name of team 1 |
| team1_color | color | RGB color of team 1 |
| team1_score | int | Score of team 1 |
| team1_locked | boolean | Whether team 1 is locked |
| team1_classes | list[byte] | Available classes for team 1 |
| team2_name | string | Name of team 2 |
| team2_color | color | RGB color of team 2 |
| team2_score | int | Score of team 2 |
| team2_locked | boolean | Whether team 2 is locked |
| team2_classes | list[byte] | Available classes for team 2 |
| lock_team_swap | boolean | Whether team swapping is locked |
| lock_spectator_swap | boolean | Whether spectator swapping is locked |
| team1_can_see_team2 | boolean | Whether team 1 can see team 2 |
| team2_can_see_team1 | boolean | Whether team 2 can see team 1 |
| team1_show_score | boolean | Whether to show team 1 score |
| team1_show_max_score | boolean | Whether to show team 1 max score |
| team2_show_score | boolean | Whether to show team 2 score |
| team2_show_max_score | boolean | Whether to show team 2 max score |
| team1_locked_class | boolean | Whether team 1 class is locked |
| team1_locked_score | boolean | Whether team 1 score is locked |
| team2_locked_class | boolean | Whether team 2 class is locked |
| team2_locked_score | boolean | Whether team 2 score is locked |
| team1_infinite_blocks | boolean | Whether team 1 has infinite blocks |
| team2_infinite_blocks | boolean | Whether team 2 has infinite blocks |
| has_map_ended | boolean | Whether the map has ended |
| prefabs | list[string] | Available prefabs |
| entities | list[Entity] | List of game entities |
| screenshot_cameras_points | list[(fixed,fixed,fixed)] | Camera positions for screenshots |
| screenshot_cameras_rotations | list[(fixed,fixed,fixed)] | Camera rotations for screenshots |

### Kill Action
| Property | Value |
|-----------|-------|
| Packet ID | 46 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| player_id | byte | ID of the player who died |
| killer_id | byte | ID of the player who made the kill |
| kill_type | byte | Type of kill |
| respawn_time | byte | Time until respawn |
| kill_count | byte | Number of kills in streak |
| isDominationKill | boolean | Whether it's a domination kill |
| isRevengeKill | boolean | Whether it's a revenge kill |

### Instantiate Kick Message
| Property | Value |
|-----------|-------|
| Packet ID | 48 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| player_id | byte | ID of the player initiating kick |
| target_id | byte | ID of the player being kicked |
| reason | byte | Reason code for the kick |

### Chat Message
| Property | Value |
|-----------|-------|
| Packet ID | 49 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| player_id | byte | ID of the player sending message |
| chat_type | byte | Type of chat (global, team, etc.) |
| value | string | Message content |

### Localised Message
| Property | Value |
|-----------|-------|
| Packet ID | 50 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| chat_type | byte | Type of chat message |
| localise_parameters | byte | Whether to localize parameters |
| string_id | string | ID of the localized string |
| parameters | list[string] | Paramaters to insert into the message |
| override_previous_message | byte | Whether to override previous message |

### SkyBox Data
| Property | Value |
|-----------|-------|
| Packet ID | 51 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| value | string | Skybox configuration data |

### Show Game Stats
| Property | Value |
|-----------|-------|
| Packet ID | 118 |
| Compression | No |

No fields for this packet.

### Map Data Start
| Property | Value |
|-----------|-------|
| Packet ID | 54 |
| Compression | Yes |

No fields for this packet.

### Map Sync Start
| Property | Value |
|-----------|-------|
| Packet ID | 55 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| size | int | Size of the map sync data |

### Map Data Chunk
| Property | Value |
|-----------|-------|
| Packet ID | 56 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| percent_complete | byte | Percentage of map data transferred |
| data | bytes | Chunk of map data |

### Map Sync Chunk
| Property | Value |
|-----------|-------|
| Packet ID | 57 |
| Compression | Yes |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| percent_complete | byte | Percentage of sync data transferred |
| data | bytes | Chunk of sync data |

### Map Data End
| Property | Value |
|-----------|-------|
| Packet ID | 58 |
| Compression | Yes |

No fields for this packet.

### Map Sync End
| Property | Value |
|-----------|-------|
| Packet ID | 59 |
| Compression | No |

No fields for this packet.

### Map Data Validation
| Property | Value |
|-----------|-------|
| Packet ID | 60 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| crc | int | CRC checksum for map data validation |

### Pack Start
| Property | Value |
|-----------|-------|
| Packet ID | 61 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| size | int | Size of the pack data |
| checksum | int | Checksum for pack validation |

### Pack Response
| Property | Value |
|-----------|-------|
| Packet ID | 62 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| value | byte | Response code for pack operation |

### Pack Chunk
| Property | Value |
|-----------|-------|
| Packet ID | 63 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| data | bytes | Chunk of pack data |

### Player Left
| Property | Value |
|-----------|-------|
| Packet ID | 64 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| player_id | byte | ID of the player who left |

### Progress Bar
| Property | Value |
|-----------|-------|
| Packet ID | 65 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| progress | fixed | Progress value (0.0 to 1.0) |
| rate | fixed | Rate of progress change |
| color1 | color | Start color of progress bar |
| color2 | color | End color of progress bar |

### Rank Ups
| Property | Value |
|-----------|-------|
| Packet ID | 66 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| noOfRankUps | int | Number of rank up events |
| score_reasons | list[int] | Reasons for each score change |
| old_scores | list[int] | Previous scores (as strings converted to int) |
| new_scores | list[int] | New scores (as strings converted to int) |

### Game Stats
| Property | Value |
|-----------|-------|
| Packet ID | 67 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| noOfStats | int | Number of statistics entries |
| team_id | int | Team ID the stats apply to |
| player_ids | list[int] | Player IDs for the statistics |
| types | list[int] | Types of statistics |

### UGC Objectives
| Property | Value |
|-----------|-------|
| Packet ID | 68 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| mode | byte | Game mode |
| noOfObjectives | int | Number of objectives |
| objective_ids | list[string] | Objective identifiers |
| objective_values | list[int] | Objective values |

### Restock
| Property | Value |
|-----------|-------|
| Packet ID | 69 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| player_id | byte | ID of the player |
| type | byte | Type of restock |

### Pick Pickup
| Property | Value |
|-----------|-------|
| Packet ID | 70 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| player_id | byte | ID of the player |
| pickup_id | byte | ID of the pickup item |
| burdensome | byte | Whether pickup is burdensome |

### Drop Pickup
| Property | Value |
|-----------|-------|
| Packet ID | 71 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| loop_count | int | Current game loop count |
| player_id | byte | ID of the player |
| pickup_id | byte | ID of the pickup item |
| position | (fixed,fixed,fixed) | Position where item is dropped |
| velocity | (fixed,fixed,fixed) | Velocity of the dropped item |

### Force Show Scores
| Property | Value |
|-----------|-------|
| Packet ID | 72 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| forced | byte | Whether to force score display |

### Show Text Message
| Property | Value |
|-----------|-------|
| Packet ID | 73 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| message_id | byte | ID of the message to show |
| duration | fixed | Duration to display message |

### Fog Color
| Property | Value |
|-----------|-------|
| Packet ID | 74 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| color | color | RGB color of the fog |

### Time Scale
| Property | Value |
|-----------|-------|
| Packet ID | 75 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| scale | fixed | Game time scale factor |

### Weapon Reload
| Property | Value |
|-----------|-------|
| Packet ID | 76 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| player_id | byte | ID of the player |
| tool_id | byte | ID of the weapon tool |
| is_done | boolean | Whether reload is complete |

### Change Team
| Property | Value |
|-----------|-------|
| Packet ID | 77 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| player_id | byte | ID of the player |
| team | byte | New team ID |

### Change Class
| Property | Value |
|-----------|-------|
| Packet ID | 78 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| player_id | byte | ID of the player |
| class_id | byte | New class ID |

### Lock Team
| Property | Value |
|-----------|-------|
| Packet ID | 79 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| team_id | byte | ID of the team |
| locked | byte | Whether team is locked |

### Team Lock Class
| Property | Value |
|-----------|-------|
| Packet ID | 80 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| team_id | byte | ID of the team |
| locked | byte | Whether class selection is locked |

### Team Lock Score
| Property | Value |
|-----------|-------|
| Packet ID | 81 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| team_id | byte | ID of the team |
| locked | byte | Whether team score is locked |

### Team Infinite Blocks
| Property | Value |
|-----------|-------|
| Packet ID | 82 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| team_id | byte | ID of the team |
| infinite_blocks | byte | Whether team has infinite blocks |

### Team Map Visibility
| Property | Value |
|-----------|-------|
| Packet ID | 83 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| team_id | byte | ID of the team |
| visible | byte | Whether team is visible on map |

### Display Countdown
| Property | Value |
|-----------|-------|
| Packet ID | 84 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| timer | float | Countdown timer value |

### Set Score
| Property | Value |
|-----------|-------|
| Packet ID | 85 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| type | byte | Type of score |
| reason | byte | Reason for score change |
| specifier | byte | Additional score specifier |
| value | int | Score value |

### Use Command
| Property | Value |
|-----------|-------|
| Packet ID | 86 |
| Compression | No |

No fields for this packet.

### Place MG
| Property | Value |
|-----------|-------|
| Packet ID | 87 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| loop_count | int | Current game loop count |
| player_id | byte | ID of the player |
| x | short | X coordinate |
| y | short | Y coordinate |
| z | short | Z coordinate |
| yaw | fixed | Yaw rotation angle |

### Place Rocket Turret
| Property | Value |
|-----------|-------|
| Packet ID | 88 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| loop_count | int | Current game loop count |
| player_id | byte | ID of the player |
| x | short | X coordinate |
| y | short | Y coordinate |
| z | short | Z coordinate |
| yaw | fixed | Yaw rotation angle |

### Place Landmine
| Property | Value |
|-----------|-------|
| Packet ID | 89 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| loop_count | int | Current game loop count |
| player_id | byte | ID of the player |
| x | short | X coordinate |
| y | short | Y coordinate |
| z | short | Z coordinate |

### Place Medpack
| Property | Value |
|-----------|-------|
| Packet ID | 90 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| loop_count | int | Current game loop count |
| player_id | byte | ID of the player |
| x | short | X coordinate |
| y | short | Y coordinate |
| z | short | Z coordinate |
| face | byte | Face where medpack is placed |

### Place Radar Station
| Property | Value |
|-----------|-------|
| Packet ID | 91 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| loop_count | int | Current game loop count |
| player_id | byte | ID of the player |
| x | short | X coordinate |
| y | short | Y coordinate |
| z | short | Z coordinate |

### Place C4
| Property | Value |
|-----------|-------|
| Packet ID | 92 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| loop_count | int | Current game loop count |
| x | short | X coordinate |
| y | short | Y coordinate |
| z | short | Z coordinate |
| face | byte | Face where C4 is placed |

### Detonate C4
| Property | Value |
|-----------|-------|
| Packet ID | 93 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| loop_count | int | Current game loop count |

### Block Sucker
| Property | Value |
|-----------|-------|
| Packet ID | 94 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| loop_count | int | Current game loop count |
| shooter_id | byte | ID of the player using block sucker |
| state | byte | State of the block sucker |
| shot | byte | Whether a shot was fired |

### Disguise
| Property | Value |
|-----------|-------|
| Packet ID | 95 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| loop_count | int | Current game loop count |
| active | byte | Whether disguise is active |

### Disable Entity
| Property | Value |
|-----------|-------|
| Packet ID | 96 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| entity_id | short | ID of the entity to disable |

### Place UGC
| Property | Value |
|-----------|-------|
| Packet ID | 97 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| loop_count | int | Current game loop count |
| x | short | X coordinate |
| y | short | Y coordinate |
| z | short | Z coordinate |
| ugc_item_id | byte | ID of the UGC item |
| placing | byte | Whether item is being placed |

### Request UGC Entities
| Property | Value |
|-----------|-------|
| Packet ID | 99 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| game_mode | byte | Game mode ID |
| in_ugc_mode | byte | Whether in UGC mode |

### UGC Message
| Property | Value |
|-----------|-------|
| Packet ID | 100 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| message_id | byte | ID of the UGC message |

### UGC Map Loading From Host
| Property | Value |
|-----------|-------|
| Packet ID | 101 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| percent_complete | byte | Percentage of map loaded |

### UGC Map Info
| Property | Value |
|-----------|-------|
| Packet ID | 102 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| png_data | bytes | PNG image data of the map |

### Voice Data
| Property | Value |
|-----------|-------|
| Packet ID | 103 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| player_id | byte | ID of the player speaking |
| data_size | short | Size of voice data |
| data | string | Voice data |

### Place Flare Block
| Property | Value |
|-----------|-------|
| Packet ID | 104 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| loop_count | int | Current game loop count |
| x | short | X coordinate |
| y | short | Y coordinate |
| z | short | Z coordinate |

### Steam Session Ticket
| Property | Value |
|-----------|-------|
| Packet ID | 105 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| ticket_size | int | Size of Steam session ticket |
| ticket | bytes | Steam session ticket data |

### Territory Base State
| Property | Value |
|-----------|-------|
| Packet ID | 106 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| base_index | byte | Index of the territory base |
| action | byte | Action being performed |
| controlled_by | byte | Team controlling the base |
| attacked_by | byte | Team attacking the base |
| capture_amount | fixed | Amount of capture progress |

### Debug Draw
| Property | Value |
|-----------|-------|
| Packet ID | 107 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| type | byte | Type of debug drawing |
| colour | int | Color of the debug drawing |
| frames | int | Number of frames to display |
| size | float | Size of the debug object (type 1) |
| x | float | X coordinate (types 0, 1) |
| y | float | Y coordinate (types 0, 1) |
| z | float | Z coordinate (types 0, 1) |
| x2 | float | Second X coordinate (type 0) |
| y2 | float | Second Y coordinate (type 0) |
| z2 | float | Second Z coordinate (type 0) |

### Lock To Zone
| Property | Value |
|-----------|-------|
| Packet ID | 108 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| A2018 | short | X min coordinate |
| A2020 | short | Y min coordinate |
| A2022 | short | Z min coordinate |
| A2019 | short | X max coordinate |
| A2021 | short | Y max coordinate |
| A2023 | short | Z max coordinate |

### Generic Vote Message
| Property | Value |
|-----------|-------|
| Packet ID | 109 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| player_id | byte | ID of the player initiating vote |
| message_type | byte | Type of vote message |
| candidates | list[{name: string, votes: byte}] | Vote candidates and vote counts |
| title | string | Title of the vote |
| description | string | Description of the vote |
| can_vote | boolean | Whether player can vote |
| allow_revote | boolean | Whether revoting is allowed |
| hide_after_vote | boolean | Whether to hide after voting |

### Help Message
| Property | Value |
|-----------|-------|
| Packet ID | 109 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| delay | float | Delay before showing message |
| message_ids | list[string] | IDs of messages to display |

### Client In Menu
| Property | Value |
|-----------|-------|
| Packet ID | 110 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| in_menu | byte | Whether client is in menu |

### Password
| Property | Value |
|-----------|-------|
| Packet ID | 111 |
| Compression | Yes |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| password | string | Server password |

### Password Needed
| Property | Value |
|-----------|-------|
| Packet ID | 112 |
| Compression | No |

No fields for this packet.

### Password Provided
| Property | Value |
|-----------|-------|
| Packet ID | 113 |
| Compression | Yes |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| password | string | Provided password |

### Initial Info
| Property | Value |
|-----------|-------|
| Packet ID | 114 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| server_steam_id | uint64 | Steam ID of the server |
| server_ip | int | IP address of the server |
| server_port | int | Port of the server |
| mode_name | string | Name of the game mode |
| mode_description | string | Description of the game mode |
| mode_infographic_text1 | string | Mode infographic text 1 |
| mode_infographic_text2 | string | Mode infographic text 2 |
| mode_infographic_text3 | string | Mode infographic text 3 |
| map_name | string | Name of the map |
| filename | string | Filename of the map |
| checksum | int | Checksum of the map |
| mode_key | byte | Key of the game mode |
| map_is_ugc | byte | Whether map is user-generated |
| query_port | short | Query port (unsigned) |
| classic | byte | Whether classic mode is enabled |
| enable_minimap | byte | Whether minimap is enabled |
| same_team_collision | byte | Whether same team collision is enabled |
| max_draw_distance | byte | Maximum draw distance |
| enable_colour_picker | byte | Whether color picker is enabled |
| enable_colour_palette | byte | Whether color palette is enabled |
| enable_deathcam | byte | Whether death camera is enabled |
| enable_sniper_beam | byte | Whether sniper beam is enabled |
| enable_spectator | byte | Whether spectator mode is enabled |
| exposed_teams_always_on_minimap | byte | Whether exposed teams show on minimap |
| enable_numeric_hp | byte | Whether numeric HP display is enabled |
| texture_skin | string | Texture skin name |
| beach_z_modifiable | byte | Whether beach Z is modifiable |
| enable_minimap_height_icons | byte | Whether minimap height icons are enabled |
| enable_fall_on_water_damage | byte | Whether falling on water causes damage |
| block_wallet_multiplier | fixed | Block wallet multiplier |
| block_health_multiplier | fixed | Block health multiplier |
| disabled_tools | list[byte] | List of disabled tools |
| disabled_classes | list[byte] | List of disabled classes |
| movement_speed_multipliers | list[fixed] | List of movement speed multipliers |
| ugc_prefab_sets | list[string] | List of UGC prefab sets |
| enable_player_score | byte | Whether player score is enabled |
| server_name | string | Name of the server |
| ground_colors | list[byte] | List of ground colors |
| allow_shooting_holding_intel | byte | Whether shooting while holding intel is allowed |
| friendly_fire | byte | Whether friendly fire is enabled |
| custom_game_rules | list[string] | List of custom game rules |
| enable_corpse_explosion | byte | Whether corpse explosion is enabled |
| ugc_mode | byte | UGC mode setting |

### Force Team Join
| Property | Value |
|-----------|-------|
| Packet ID | 115 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| team_id | byte | ID of the team to join |
| instant | byte | Whether join is instant |

### Team Progress
| Property | Value |
|-----------|-------|
| Packet ID | 117 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| team_id | byte | ID of the team |
| visible | boolean | Whether progress is visible |
| show_particle | boolean | Whether to show particle effects |
| show_previous | boolean | Whether to show previous progress |
| show_as_percent | boolean | Whether to show as percentage |
| percent | fixed | Progress percentage (if show_as_percent) |
| numerator | int | Progress numerator (if not show_as_percent) |
| denominator | int | Progress denominator (if not show_as_percent) |
| icon_id | byte | ID of the icon to display |

### Set Ground Colors
| Property | Value |
|-----------|-------|
| Packet ID | 118 |
| Compression | No |

| Field Name | Field Type | Notes |
|------------|------------|-------|
| ground_colors | list[(byte,byte,byte,byte)] | List of RGBA ground colors |


## Disclaimer

This documentation is based on reverse engineering work of the Ace of Spades 1.x protocol. Some packet IDs might appear multiple times as they can be reused for different purposes depending on context. Packet fields and structures are documented as accurately as possible based on the decompilation of the original game.

This documentation is part of the Ace Of Spades Library Reverse Engineering Project, which aims to recreate a compatible server implementation. The structure and field names might not match the original implementation's internal names, but they reflect the same functionality.

Some fields with unclear purpose are labeled with placeholder names (e.g., A2018, A2019) until their exact purpose is determined. 

Some packets might be missing, to be added!