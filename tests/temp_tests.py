def test_blockmanagerstate():
    current_packet = packet.BlockManagerState()
    return current_packet

def test_changeentity():
    current_packet = packet.ChangeEntity()
    current_packet.entity_id = 1
    current_packet.fuse = 0
    current_packet.player_id = 1
    current_packet.state = 0
    current_packet.type = 1
    return current_packet

def test_createentity():
    current_packet = packet.CreateEntity()
    current_packet.entity = {}
    current_packet.set_entity = 0
    return current_packet

def test_entityupdates():
    current_packet = packet.EntityUpdates()
    return current_packet

def test_eraseprefabaction():
    current_packet = packet.ErasePrefabAction()
    current_packet.from_block_index = 0
    current_packet.loop_count = 0
    current_packet.player_id = 1
    current_packet.prefab_name = "test"
    current_packet.to_block_index = 0
    return current_packet

def test_initialugcbatch():
    current_packet = packet.InitialUGCBatch()
    return current_packet

def test_mapsyncchunk():
    current_packet = packet.MapSyncChunk()
    current_packet.data = b""
    current_packet.percent_complete = 0
    return current_packet

def test_mapsyncend():
    current_packet = packet.MapSyncEnd()
    return current_packet

def test_mapsyncstart():
    current_packet = packet.MapSyncStart()
    return current_packet

def test_packchunk():
    current_packet = packet.PackChunk()
    current_packet.data = b""
    return current_packet

def test_serverblockaction():
    current_packet = packet.ServerBlockAction()
    current_packet.items = []
    return current_packet

