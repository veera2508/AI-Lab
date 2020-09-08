'''
State: Point coordinates in a 10x10 grid
Actions: Move the center up, down, left, right
Cost Function (Minimize): Sum of the Manhatten distances between the points and the center
'''
import random
actions = [[0, 1], [0, -1], [1, 0], [-1, 0]]

def cost(points, center):
    cost = 0
    x, y = center
    for i, j in points:
        cost += abs(x-i) + abs(y-j)
    return cost


def hillClimb(points, start = None, gridsize = (10, 10)):
    if start:
        x, y = start
    else:
        m, n = gridsize
        x = random.randrange(0, m)
        y = random.randrange(0, n)

        while (x,y) not in points:
            x = random.randrange(0, m)
            y = random.randrange(0, n)

    i = 0
    mini = 2**31
    prevmini = mini
    minx = x
    miny = y
    while True:    
        for action in actions:
            x = minx
            y = miny
            dx, dy = action
            x+= dx
            y+= dy
            if x>=0 and y>=0:
                cst = cost(points, (x, y))
                #print(cst, x, y)
                if cst < mini:
                    mini = cst
                    minx = x
                    miny = y
        if prevmini <= mini:
            break
        else:
            prevmini = mini
        i += 1
        print("Center for iteration ", i, " : ", minx, miny, " Cost: ", mini)
    return (minx, miny)

points = [(1, 1), (5, 2), (6, 4), (7, 7), (4, 9)]
print(hillClimb(points, start = (0, 9), gridsize = (10, 10)))
            



        
