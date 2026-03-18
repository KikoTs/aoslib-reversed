import sys
sys.path.insert(0, '')
import shared.packet as pkt

py2_props = {}
with open('temp_attrs.txt') as f:
    for line in f:
        line = line.strip()
        if not line: continue
        d = line.split('|')
        py2_props[d[0]] = d[1].split(',') if len(d)>1 else []

with open('temp_tests.py', 'w') as f:
    for name, props in py2_props.items():
        c = getattr(pkt, name)
        py3_props = [p for p in dir(c) if not p.startswith('_') and p not in ('id', 'compress_packet', 'read', 'write', 'generate')]
        
        common_props = [p for p in props if p in py3_props and p != 'generate']
        
        f.write(f'def test_{name.lower()}():\n')
        f.write(f'    current_packet = packet.{name}()\n')
        for p in common_props:
            val = '0'
            if p in ('entity', 'player_updates', 'entities', 'updated_entities'): val = '{}'
            elif p in ('data', 'content'): val = 'b""'
            elif p in ('items', 'occupied_blocks', 'user_blocks', 'damaged_blocks', 'add_block', 'remove_block', 'reset', 'resetitems', 'tiles'): val = '[]'
            elif 'id' in p: val = '1'
            elif p == 'color': val = '(255, 0, 0)'
            elif p == 'orientation': val = '(0.0, 0.0, 0.0)'
            elif p == 'position': val = '(0.0, 0.0, 0.0)'
            elif p == 'velocity': val = '(0.0, 0.0, 0.0)'
            elif p == 'prefab_name': val = '"test"'
            elif p == 'type': val = '1'
            
            f.write(f'    current_packet.{p} = {val}\n')
            
        f.write('    return current_packet\n\n')
