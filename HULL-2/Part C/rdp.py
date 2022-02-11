# Ramer–Douglas–Peucker algorithm
# by Nivin Jose Kovukunnel

def calculate_distance(point_1, point_2):
    return  sqrt((point_1[0] - point_2[0]) ** 2 + (point_1[1] - point_2[1]) ** 2)


def point_line_distance(point, start, end):
    if (start == end):
        return calculate_distance(point, start)
    else:
        n = abs((end[0] - start[0]) * (start[1] - point[1]) - (start[0] - point[0]) * (end[1] - start[1]))
        d = sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
        return n / d


def Ramer_Douglas_Peucker_Algorithm(points, epsilon):
       
    distance_max = 0.0
    index = 0
    for i in range(1, len(points) - 1):
        d = point_line_distance(points[i], points[0], points[-1])
        if d > distance_max:
            index = i
            distance_max = d

    if distance_max >= epsilon:
        output = Ramer_Douglas_Peucker_Algorithm(points[:index+1], epsilon)[:-1] + Ramer_Douglas_Peucker_Algorithm(points[index:], epsilon)
        
    else:
        output = [points[0], points[-1]]

    return output
