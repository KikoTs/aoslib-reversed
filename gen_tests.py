import sys
sys.path.insert(0, '')
import shared.packet as pkt

classes_to_test = [
    'BlockManagerState', 'ChangeEntity', 'CreateEntity', 'EntityUpdates', 'ErasePrefabAction',
    'InitialUGCBatch', 'MapSyncChunk', 'MapSyncEnd', 'MapSyncStart', 'PackChunk', 'ServerBlockAction'
]

with open('temp_tests.py', 'w') as f:
    for name in classes_to_test:
        c = getattr(pkt, name)
        f.write(f'def test_{name.lower()}():\n')
        f.write(f'    current_packet = packet.{name}()\n')
        
        props = [p for p in dir(c) if not p.startswith('_') and p not in ('id', 'compress_packet', 'read', 'write')]
        for p in props:
            val = '0'
            if p == 'name': val = '"test"'
            elif p in ('entity', 'player_updates'): val = '{}'
            elif p in ('data', 'items', 'content'): val = 'b""'
            elif p == 'tiles': val = '[]'
            elif 'id' in p: val = '1'
            elif p == 'color': val = '(255, 0, 0)'
            elif p == 'orientation': val = '(0.0, 0.0, 0.0)'
            elif p == 'position': val = '(0.0, 0.0, 0.0)'
            elif p == 'velocity': val = '(0.0, 0.0, 0.0)'
            elif p == 'flags': val = '1'
            elif p == 'type': val = '1'
            f.write(f'    current_packet.{p} = {val}\n')
            
        f.write('    return current_packet\n\n')
