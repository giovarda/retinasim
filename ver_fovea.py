import open3d as o3d
import numpy as np

mesh = o3d.io.read_triangle_mesh("salida/retina_full_test2/surface/retina_surface_vessels.ply")
mesh.compute_vertex_normals()

fovea_centre = np.array([5445.99, 0., 0.])

vis = o3d.visualization.Visualizer()
vis.create_window(visible=False, width=1200, height=900)
vis.add_geometry(mesh)

ctr = vis.get_view_control()
ctr.set_lookat(fovea_centre)
ctr.set_zoom(0.02)  # muy cercano

vis.poll_events()
vis.update_renderer()
vis.capture_screen_image("salida/retina_full_test2/surface/vista_fovea.png")
vis.destroy_window()
print("Imagen guardada.")
