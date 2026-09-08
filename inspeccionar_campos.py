import sys
sys.path.insert(0, '.')
from pymira import spatialgraph

g = spatialgraph.SpatialGraph()
g.read('/home/gio/retinasim/salida/retina_full/cco/retina_cco_vorcap_reanimate.am')

for f in g.fields:
    print(f['name'], '-> shape:', f['data'].shape if hasattr(f['data'],'shape') else len(f['data']))

