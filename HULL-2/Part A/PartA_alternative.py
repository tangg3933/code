# Part A Alternative Method:
'''
Author: Nivin Jose Kovukunnel
Instead of using a projection matrix, the 3rd dimension can simply be discarded/omitted to find the 2D projection.
This idea was suggested by the client company representative Luke Berry.
Note that this method also produces the exact same results as the results obtained when using a projection matrix.
This code was implemented as a means to double check the results as well.
'''

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


if __name__ == '__main__':
    # Path = 'A_1_440_B01_P01.obj'
    Path = 'C:/Users/nivin/Desktop/A_1_440_B01_P01.obj'
    data = ObjLoader(Path)

    # remove z-axis using list comprehension
    projected_data = []
    result = [(x[0],x[1]) for x in data.vertices]
    print(result)
