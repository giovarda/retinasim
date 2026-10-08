import sys, os
sys.path.insert(0, '.')
from pymira import spatialgraph
import numpy as np
import csv

carpeta_run = 'salida/retina_full_test2'
archivo_am = 'cco/retina_cco_vorcap_reanimate.am'

ruta_am = os.path.join(carpeta_run, archivo_am)
ruta_csv = os.path.join(carpeta_run, 'cco', 'vasculatura_reanimate_16sep.csv')

g = spatialgraph.SpatialGraph()
g.read(ruta_am)

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

with open(ruta_csv, 'w', newline='') as f:
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

print(f"Exportacion completa: {idx} puntos escritos en {ruta_csv}")
