# # This is an atternative way to display the 3d model
# # Especially for who cannot build the VS project (C#) on their local computer

# #see http://www.open3d.org/docs/release/index.html
# import open3d as o3d
# import numpy as np

# textured_mesh = o3d.io.read_triangle_mesh("./TestData/Model/440/A_1_440_01.obj")
# print(textured_mesh)
# # print(np.array(textured_mesh.points))
# # o3d.visualization.draw_geometries([textured_mesh])

# #A way to make it denser, if u use below, comment the line #11, you can change the number of points in any value you want
# # pcd = textured_mesh.sample_points_poisson_disk(5000)
# # o3d.visualization.draw_geometries([pcd])

class ObjLoader(object):
    def __init__(self, fileName):
        self.vertices = []
        self.faces = []
        ##
        try:
            f = open(fileName)
            for line in f:
                if line[:2] == "v ":
                    index1 = line.find(" ") + 1
                    index2 = line.find(" ", index1 + 1)
                    index3 = line.find(" ", index2 + 1)

                    vertex = (float(line[index1:index2]), float(line[index2:index3]), float(line[index3:-1]))
                    vertex = (round(vertex[0], 2), round(vertex[1], 2), round(vertex[2], 2))
                    self.vertices.append(vertex)

                elif line[0] == "f":
                    string = line.replace("//", "/")
                    ##
                    i = string.find(" ") + 1
                    face = []
                    for item in range(string.count(" ")):
                        if string.find(" ", i) == -1:
                            face.append(string[i:-1])
                            break
                        face.append(string[i:string.find(" ", i)])
                        i = string.find(" ", i) + 1
                    ##
                    self.faces.append(tuple(face))

            f.close()
        except IOError:
            print(".obj file not found.")