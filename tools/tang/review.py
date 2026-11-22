import sys; sys.path.insert(0,'.')
from zy import zy_line
import importlib
mod = importlib.import_module(sys.argv[1])
for p in mod.POEMS:
    print(p['n'], p['t'])
    for l in p['lines']:
        z = zy_line(l, p.get('zy', {}))
        print('  ' + ' '.join(f"{c}{zz}" for c, zz in zip(l, z) if zz))
