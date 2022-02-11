

"""
Author: Fulin Kuang & Gordon Tang
Function: HULL Aggregation

The code is based on Weizhen Fang's Part A group's implementation of 3D to 2D
The code directly continue development on their code and uses their result (a set of 2D coordinates) as input
The idea of this implementation is divide and conquer, for the theory, refer to:
https://github.cs.adelaide.edu.au/a1788528/HULL-2/blob/master/Documentations/WEEK%204/Week%204%20research%20-%20Hull%20Aggregation.pdf

Weizhen Fang's Part A group's implementation of 3D to 2D's results has been examined
A: We first used open3D's Qhull function to calculate the convex hull of the original obj file (based on 3D)
B: We then used our implementation to calculate the convex hull using Weizhen Fang's Part A group's result (based on 2D)
We then compared A and B, the result shows exactly the same, which proves the correctness of both part A and part B..
"""


import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from classes.Read_data import *
import numpy as np
import pygame
import math
from os import listdir
from os.path import isfile, join

draw_line_lists = []


# Calculate the area of the triangle based on the coordinates of the three vertices of the triangle
def calc_area(a, b, c):
    x1, y1 = a
    x2, y2 = b
    x3, y3 = c
    return x1 * y2 + x3 * y1 + x2 * y3 - x3 * y2 - x2 * y1 - x1 * y3

def Up(left, right, points, borders):
    """
    Find the boundary point of the upper half
    :param left: tuple, Leftmost point
    :param right: tuple, Rightmost point
    :param points: All points set
    :param borders: Boundary point set
    :return:
    """

    # For drawing, record processing steps
    draw_line_lists.append(left)
    draw_line_lists.append(right)

    # The two points left and right_point form a straight line, and now I want to find a point on this straight line, and the triangle area required to form is the largest
    area_max = 0  # Record the area of the largest triangle

    for item in points:
        if item == left or item == right:  # The two points that make up a straight line are also in the lists collection, but they are not on the straight line, so they are not calculated.
            continue
        else:
            temp = calc_area(left, right, item)  # Temporarily store the area formed by the point and the straight line for comparison in the next iteration
            if temp > area_max:
                max_point = item  # Record the point that currently constitutes the largest triangle
                area_max = temp  # Record the current largest triangle area

    if area_max != 0:  # When a line is no longer tentative, it stops, returns to the previous level, and processes the subtree of its sibling node.
        borders.append(max_point)
        Up(left, max_point, points, borders)  # The original left boundary point remains unchanged, the point just found to form the largest triangle is used as the right boundary point, and the recursion continues
        Up(max_point, right, points, borders)  # The original right boundary point remains unchanged, the point just found to form the largest triangle is used as the left boundary point, and the recursion continues


def Down(left, right, points, borders):
    """
    Same as parameters in above
    """
    draw_line_lists.append(left)
    draw_line_lists.append(right)

    area_max = 0

    for item in points:
        if item == left or item == right:
            continue
        else:
            temp = calc_area(left, right, item)
            if temp < area_max:
                max_point = item
                area_max = temp

    if area_max != 0:
        borders.append(max_point)
        Down(left, max_point, points, borders)
        Down(max_point, right, points, borders)


# Combine steps. When the execution reaches this point, the divide and conquer has ended, and the answer has been generated. The function of this function is to sort the unordered answers in a clockwise order
def order_border(points):
    """
    :param points: Unordered boundary point set
    :return: list [( , )...( , )]
    """
    points.sort()  # Sort first in the order of the x-axis to find the leftmost and rightmost points
    first_x, first_y = points[0]  # Leftmost point
    last_x, last_y = points[-1]  # Rightmost point
    up_borders = []  # Upper boundary
    dowm_borders = []  # Lower boundary
    # Analyze every point
    for item in points:
        x, y = item
        if y > max(first_y, last_y):  # If it is greater than the y value of the leftmost and rightmost points, it must be in the upper half.
            up_borders.append(item)
        elif min(first_y, last_y) < y < max(first_y,
                                            last_y):  # If it is between the y values of the leftmost and rightmost points, the area of the triangle should be used to make the judgment. If the area is negative, it means that it is an inverted triangle, that is, the third point is below the line, which is the lower half; otherwise, it is the upper half.
            if calc_area(points[0], points[-1], item) > 0:
                up_borders.append(item)
            else:
                dowm_borders.append(item)
        else:  # If it is smaller than the y value of the leftmost and rightmost points, it must be in the lower half.
            dowm_borders.append(item)

    list_end = up_borders + dowm_borders[::-1]  # The boundary point of the final clockwise output
    return list_end


def draws(points, list_frames, gif_name="save.gif"):
    """
    Generate gif and save
    :param points: All points set
    :param list_frames:
    :param gif_name:
    :return: .gif
    """
    min_value = 0
    max_value = 100

    all_x = []
    all_y = []
    for item in points:
        a, b = item
        all_x.append(a)
        all_y.append(b)

    fig, ax = plt.subplots()  # Generate axes and figs, iterable objects
    x, y = [], []  # Used to update data after acceptance
    line, = plt.plot([], [], color="red")  # Draw a line object, plot return value type

    def init():
        # The initialization function is used to draw a clean canvas to prepare for subsequent drawing
        ax.set_xlim(min_value - abs(min_value * 0.1), max_value + abs(max_value * 0.1))  # Initial function, set the drawing range
        ax.set_ylim(min_value - abs(min_value * 0.1), max_value + abs(max_value * 0.1))
        return line

    def update(points):
        a, b = points
        x.append(a)
        y.append(b)
        line.set_data(x, y)
        return line

    plt.scatter(all_x, all_y)  # Draw all the scattered points
    ani = animation.FuncAnimation(fig, update, frames=list_frames, init_func=init,
                                  interval=1500)  # interval represents the speed of drawing the connection, the larger the value, the slower the speed
    ani.save(gif_name, writer='pillow')


def show_result(points, results):
    """
    draw
    :param points: All points set
    :param results: All edge sets
    :return: picture
    """
    all_x = []
    all_y = []
    for item in points:
        a, b = item
        all_x.append(a)
        all_y.append(b)

    for i in range(len(results) - 1):
        item_1 = results[i]
        item_2 = results[i + 1]
        # Abscissa, ordinate
        one_, oneI = item_1
        two_, twoI = item_2
        plt.plot([one_, two_], [oneI, twoI])
    plt.scatter(all_x, all_y)
    plt.show()


def get_2D_points(Path):
    data = ObjLoader(Path)
    '''
        Program below is about finding projected 2D points along z axis
    '''

    # projection matrix along z axis
    projection_matrix = np.matrix([
        [1, 0, 0],
        [0, 1, 0],
    ])

    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    BLACK = (0, 0, 0)

    WIDTH, HEIGHT = 2000, 2000
    pygame.display.set_caption("3D projection!")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    scale = 100
    circle_pos = [WIDTH / 2, HEIGHT / 2]  # x, y

    # variable to contain all 2D projected points
    points = []
    # convert tuple point to matrix
    for Dim3 in data.vertices:
        Dim3 = np.matrix(np.asarray(Dim3))
        points.append(Dim3)

    single_points2D = []
    # for loop to find all 2d projected points
    for point in points:
        projected2d = np.dot(projection_matrix, point.reshape((3, 1)))
        print(projected2d)

        x = int(projected2d[0][0] * scale) + circle_pos[0]
        y = int(projected2d[1][0] * scale) + circle_pos[1]
        single_points2D.append((x, y))
    return single_points2D


if __name__ == "__main__":
    folder = '../TestData/Model/410'
    points2D = []
    for f in listdir(folder):
        file_path = join(folder, f)
        if isfile(file_path):
            single_points2D = get_2D_points(file_path)
            for sin in single_points2D:
                points2D.append(sin)
    # First sort by the x-axis to find the leftmost and rightmost points
    points2D.sort()
    # Boundary point set
    borders = []
    Up(points2D[0], points2D[-1], points2D, borders)  # Upper boundary point set
    Down(points2D[0], points2D[-1], points2D, borders)  # Lower boundary point set
    borders.append(points2D[0])
    borders.append(points2D[-1])  # Add the first and last points to the boundary point set
    results = order_border(borders)  # Clockwise boundary point
    # print(results)  # Output the answer clockwise
    results.append(results[0])  # Connect the last point to the source point and draw a closed line

    # Draw edges only
    show_result([], results)  # Show static results
    print("boundary: ", results)
    # If you want to show all points
    show_result(points2D, results)  # Show static results

    # draws(points2D, results, "result.gif")  # Plot dynamic results
    # draws(points2D, draw_line_lists, "process.gif")  # Draw dynamic process
