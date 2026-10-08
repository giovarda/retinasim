import sys, os
sys.path.insert(0, '.')
import numpy as np
np.random.seed(42)

from os.path import join
from retinasim.main import get_eye, generate_lsystem, vascular_upper_lower
from retinasim.capillary_bed import voronoi_capillary_bed
from retinasim.utility import reanimate_sim, create_directories

path = 'salida/retina_full_test2'
lpath, cco_path, dataPath, surfacePath, embedPath, concPath = create_directories(path, '', overwrite_existing=False)

geometry_file = join(dataPath, "retina_geometry.p")
eye = get_eye(geometry_file, create_new_geometry=True)

# --- L-system seed ---
combined_graph, mfiles = generate_lsystem(opath=dataPath, lpath=lpath, gfile='retina_lsystem.am', eye=eye)

# --- RetinaGen: optimizacion vascular real ---
cco_ofile = 'retina_cco.am'
res, amfiles, _, graph = vascular_upper_lower(lpath=lpath, convert_to_json=True, opath=cco_path,
                                                join_feeding=True, eye=eye, quiet=True, macula_fraction=0.2)

# --- Lecho capilar Voronoi ---
graph = voronoi_capillary_bed(cco_path, cco_ofile, write=False, plot=False, displace_degen=True,
                                geometry_file=geometry_file, eye=eye)
cap_file = os.path.join(cco_path, cco_ofile.replace('.am', '_vorcap.am'))
graph.write(cap_file)

# --- Reanimate (SIN el paso de crawl) ---
cap_file_r = cap_file.replace('.am', '_reanimate.am')
graph = reanimate_sim(graph, opath=cco_path, ofile=os.path.basename(cap_file_r), a_pressure=52., v_pressure=20.)

print("Pipeline completo (sin crawl). Archivo final:", cap_file_r)
