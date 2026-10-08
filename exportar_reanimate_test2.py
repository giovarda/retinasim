import sys
sys.path.insert(0, '.')
from pymira import spatialgraph
import numpy as np
import csv

g = spatialgraph.SpatialGraph()
g.read('/home/gio/retinasim/salida/retina_full_test2/cco/retina_cco_vorcap_reanimate.am')  # AJUSTAR RUTA

def get_field(g, name):
    for f in g.fields:
        if f['name'] == name:
            return np.asarray(f['data'])
    return None

pts = get_field(g, 'EdgePointCoordinates')
radius = get_field(g, 'Radii')
nedgepoints = get_field(g, 'NumEdgePoints')
vtype = get_field(g, 'VesselType')
pressure = get_field(g, 'Pressure')
flow = get_field(g, 'Flow')

with open('salida/retina_full_test2/cco/vasculatura_reanimate.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['edge_id','point_index','x_um','y_um','z_um',
                      'radius_um','vessel_type','pressure','flow'])
    idx = 0
    for edge_id, n in enumerate(nedgepoints.flatten()):
        n = int(n)
        for j in range(n):
            x, y, z = pts[idx+j]
            r = radius[idx+j]
            vt = int(vtype[idx+j])
            p = pressure[idx+j]
            fl = flow[idx+j]
            writer.writerow([edge_id, j, x, y, z, r, vt, p, fl])
        idx += n

print("Exportacion completa:", idx, "puntos escritos.")
