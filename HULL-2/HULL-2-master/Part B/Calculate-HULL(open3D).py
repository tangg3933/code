"""
Author: Fulin Kuang & Gordon Tang
Function: Hull calculation and aggregation

This code is based on open3D library, the computing is based on 3D
This code was originally a demo for part B, now only for examination purposes because we have moved to 2D, see other py files

DO NOT RUN part A and part B together
"""

import open3d as o3d
from os import listdir
from os.path import isfile, join

# DO NOT RUN part A and part B together, we have not split it yet

# Part A, read a single obj and calculate its hulls
textured_mesh = o3d.io.read_triangle_mesh("../TestData/Model/440/A_1_440_B01_P01.obj")
# calculate hull
hull, _ = textured_mesh.compute_convex_hull()
hull_ls = o3d.geometry.LineSet.create_from_triangle_mesh(hull)
hull_ls.paint_uniform_color((1, 0, 0))
# remove textured_mesh if you only want
o3d.visualization.draw_geometries([textured_mesh,hull_ls])


# Part B, calculate hull of all obj in a directory and aggregate them
def readObj(path):
    textured_mesh = o3d.io.read_triangle_mesh(path)
    # calculate hull
    hull, _ = textured_mesh.compute_convex_hull()
    hull_ls = o3d.geometry.LineSet.create_from_triangle_mesh(hull)
    hull_ls.paint_uniform_color((1, 0, 0))
    # o3d.visualization.draw_geometries([textured_mesh, hull_ls])
    return textured_mesh, hull_ls


# if __name__ == '__main__':
#     folder = '/Users/fulin/PycharmProjects/HULL-2/TestData/Model/410'
#     mesh_hulls = []
#     for f in listdir(folder):
#         file_path = join(folder, f)
#         if isfile(file_path):
#             textured_mesh, hull_ls = readObj(file_path)
#             mesh_hulls.append(textured_mesh)
#             mesh_hulls.append(hull_ls)
#
#     print(mesh_hulls)
#     o3d.visualization.draw_geometries(mesh_hulls)
#     o3d.visualization.draw_geometries(mesh_hulls[::2])
