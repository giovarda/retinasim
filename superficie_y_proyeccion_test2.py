# superficie_y_proyeccion_test2.py
import sys, os
sys.path.insert(0, '.')
from os.path import join

from retinasim.main import get_eye
from retinasim.scripts.create_surface import create_surface
from retinasim.scripts.project_graph_to_surface import project_to_surface
import pymira.spatialgraph as sp

path = 'salida/retina_full_test2'
lpath = join(path, 'lsystem')
cco_path = join(path, 'cco')
dataPath = join(path, 'data')
surfacePath = join(path, 'surface')
os.makedirs(surfacePath, exist_ok=True)

geometry_file = join(lpath, 'retina_geometry.p')
eye = get_eye(geometry_file, create_new_geometry=False)

# --- Cargar el grafo ya resuelto por Reanimate ---
cap_file_r_c = join(cco_path, 'retina_cco_vorcap_reanimate.am')
graph = sp.SpatialGraph()
graph.read(cap_file_r_c)

# --- Crear las 14 superficies de capa retinal ---
ofile = join(surfacePath, 'retina_surface.ply')
plot_file = ofile.replace('.ply', '_profile.png')
create_surface(path=cco_path, ofile=ofile, plot=True, plot_file=plot_file,
               add_simplex_noise=True, eye=eye, project=True)
print("Superficies creadas en:", surfacePath)

# --- Proyectar la vasculatura sobre la malla de vasos ---
vfile = join(surfacePath, 'retina_surface_vessels.ply')
ofile_proj = cap_file_r_c.replace('.am', '_projected.am')
project_to_surface(graph=graph, eye=eye, vfile=vfile, plot=False,
                    interpolate=False, ofile=ofile_proj, write_mesh=True,
                    iterp_resolution=10., filter=False)
print("Vasculatura proyectada:", ofile_proj)
