import open3d as o3d
from os import listdir
from os.path import isfile, join
from classes.Read_data import *
import numpy as np
import pygame
import math


if __name__ == '__main__':
    Path = 'TestData/Model/440/A_1_440_B01_P01.obj'
    data = ObjLoader(Path)
    '''
        Program below is about finding projected 2D points along z axis
    '''
    # projection matrix along z axis
    projection_matrix = np.matrix([
                                    [1, 0, 0],
                                    [0, 1, 0],
                                             ])                                     
    # variable to contain all 2D projected points
    points = []
    # convert tuple point to matrix
    for Dim3 in data.vertices:
        Dim3 = np.matrix(np.asarray(Dim3))
        points.append(Dim3)
        
    for point in points:
        projected2d = np.dot(projection_matrix,point.reshape((3, 1)))
        print(projected2d)
