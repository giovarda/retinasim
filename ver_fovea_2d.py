import open3d as o3d
import numpy as np
import matplotlib
matplotlib.use('Agg')  # backend sin pantalla
import matplotlib.pyplot as plt

mesh = o3d.io.read_triangle_mesh("salida/retina_full_test2/surface/retina_surface_vessels.ply")
verts = np.asarray(mesh.vertices)

fovea_centre = np.array([5445.99, 0., 0.])
fovea_radius = 223.5

# Filtrar vertices cerca de la fovea (radio 5x mas grande para ver contexto)
dist_xy = np.sqrt((verts[:,0]-fovea_centre[0])**2 + (verts[:,1]-fovea_centre[1])**2)
mask = dist_xy < fovea_radius * 6

sub = verts[mask]

plt.figure(figsize=(8,6))
plt.scatter(sub[:,0]-fovea_centre[0], sub[:,2], s=2)
plt.xlabel('Distancia en x desde centro de fovea (um)')
plt.ylabel('Profundidad z (um)')
plt.title('Corte cerca de la fovea')
plt.grid(True)
plt.savefig('salida/retina_full_test2/surface/corte_fovea.png', dpi=150)
print("Guardado. Puntos usados:", sub.shape[0])
