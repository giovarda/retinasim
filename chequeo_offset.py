# chequeo_offset.py
import sys
sys.path.insert(0, '.')
import numpy as np
import open3d as o3d
import pymira.spatialgraph as sp

AM = sys.argv[1] if len(sys.argv) > 1 else \
    'salida/retina_full_test2/cco/retina_cco_vorcap_reanimate_projected.am'
PLY = 'salida/retina_full_test2/surface/retina_surface_vessels.ply'

g = sp.SpatialGraph()
g.read(AM)
pts = np.asarray(g.get_data('EdgePointCoordinates'), dtype=float)
nep = np.asarray(g.get_data('NumEdgePoints')).astype(int)
tv = np.asarray(g.get_data('VesselType')).astype(int).ravel()
if len(tv) == len(pts):
    tipo = tv
elif len(tv) == len(nep):
    tipo = np.repeat(tv, nep)
else:
    sys.exit(f'VesselType={len(tv)}, puntos={len(pts)}, aristas={len(nep)}')

ok = np.isfinite(pts).all(axis=1)
print(f'Archivo: {AM}')
print(f'Puntos: {len(pts)}, no finitos descartados: {(~ok).sum()}')
pts, tipo = pts[ok], tipo[ok]

mesh = o3d.io.read_triangle_mesh(PLY)
scene = o3d.t.geometry.RaycastingScene()
scene.add_triangles(o3d.t.geometry.TriangleMesh.from_legacy(mesh))

d = np.empty(len(pts))
step = 500000
for i in range(0, len(pts), step):
    q = o3d.core.Tensor(pts[i:i + step].astype(np.float32))
    cp = scene.compute_closest_points(q)['points'].numpy()
    d[i:i + step] = np.linalg.norm(pts[i:i + step] - cp, axis=1)

print('\ntipo | n puntos | distancia a la malla de vasos: mediana (p25-p75)')
for t in np.unique(tipo):
    m = tipo == t
    print(f'{t:4d} | {m.sum():8d} | {np.median(d[m]):7.1f} '
          f'({np.percentile(d[m], 25):.1f}-{np.percentile(d[m], 75):.1f})')
