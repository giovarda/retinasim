import open3d as o3d
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

mesh = o3d.io.read_triangle_mesh("salida/retina_full_test2/surface/retina_surface_vessels.ply")
verts = np.asarray(mesh.vertices)

fovea_centre = np.array([5445.99, 0., 0.])
fovea_radius = 223.5
occular_centre = np.array([0., 0., 24000.])

dist_xy = np.sqrt((verts[:,0]-fovea_centre[0])**2 + (verts[:,1]-fovea_centre[1])**2)
mask = dist_xy < fovea_radius * 6
sub = verts[mask]

dist_to_centre = np.sqrt((sub[:,0]-occular_centre[0])**2 +
                          (sub[:,1]-occular_centre[1])**2 +
                          (sub[:,2]-occular_centre[2])**2)

desviacion = dist_to_centre - np.mean(dist_to_centre)

plt.figure(figsize=(8,6))
plt.scatter(sub[:,0]-fovea_centre[0], desviacion, s=4)
plt.xlabel('Distancia en x desde centro de fovea (um)')
plt.ylabel('Desviacion radial local (um)')
plt.title('Depresion local en la fovea (curvatura global removida)')
plt.grid(True)
plt.savefig('salida/retina_full_test2/surface/corte_fovea_local.png', dpi=150)
print("Guardado. Puntos:", sub.shape[0])
