import sys, os
sys.path.insert(0, '.')
import numpy as np
from os.path import join
arr = np.asarray
from pymira import spatialgraph
from retinasim.main import get_eye
from retinasim.embed import embed

path = 'salida/retina_full_test2'
eye = get_eye(join(path, 'lsystem', 'retina_geometry.p'), create_new_geometry=False)

graph = spatialgraph.SpatialGraph()
graph.read(join(path, 'cco', 'retina_cco_vorcap_reanimate_projected.am'))

domain = arr([[-1000., 11000.], [-6000., 6000.], [-1000., 5000.]])
dim = [150, 150, 300]

embedObj = embed(graph=graph, eye=eye, filename=None, domain=domain, dim=dim,
                 surface_dir=join(path, 'surface'), output_path=join(path, 'embed'),
                 theta=0., phi=0., chi=0., write=False,
                 rotation_centre=arr([0., 0., 0.]))

os.makedirs(join(path, 'embed'), exist_ok=True)
labels = embedObj.label_grid
print('label_grid:', labels.shape, labels.dtype)
u, c = np.unique(labels, return_counts=True)
print(dict(zip(u.tolist(), c.tolist())))
print('voxeles de vaso:', int(np.count_nonzero(embedObj.vessel_grid)))
np.save(join(path, 'embed', 'label_grid_prueba.npy'), labels)
np.save(join(path, 'embed', 'vessel_grid_prueba.npy'), embedObj.vessel_grid)
print('Listo.')
