# This is an atternative way to display the 3d model
# Especially for who cannot build the VS project (C#) on their local computer

#see http://www.open3d.org/docs/release/index.html
import open3d as o3d
import numpy as np

textured_mesh = o3d.io.read_triangle_mesh("./TestData/Model/440/A_1_440_01.obj")
print(textured_mesh)
# print(np.array(textured_mesh.points))
o3d.visualization.draw_geometries([textured_mesh])

#A way to make it denser, if u use below, comment the line #11, you can change the number of points in any value you want
# pcd = textured_mesh.sample_points_poisson_disk(5000)
# o3d.visualization.draw_geometries([pcd])
