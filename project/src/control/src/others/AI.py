import numpy as np

b = [['.1', '#', '-', '.2'],
     ['-', '-', '-', '@'],
     ['#', '#', '-', '#'],
     ['$2', '-', '-', '$1']]

lenx = len(b)
leny = len(b[0])

EMP = '-'
BOX = '$'
BOX1 = '$1'
BOX2 = '$2'
MAN = '@'
WAL = '#'
DES = '.'
DES1 = '.1'
DES2 = '.2'

def init():
    global marked, pathFound, distTo, paths
    marked = [[False, False, False, False],
              [False, False, False, False],
              [False, False, False, False],
              [False, False, False, False]]
    pathFound = False
    m = 100
    distTo = [[m, m, m, m],
              [m, m, m, m],
              [m, m, m, m],
              [m, m, m, m]]
    paths = []

def valid(x, y):
    return (x >= 0 and y >= 0 and x < lenx and y < leny
           and WAL not in b[x][y] and BOX not in b[x][y]);

def adj(x, y):
    #assert '$' in b[x][y], 'Wall or Empty do not have adj.'
    return [[p[0], p[1]]
          for p in [[x - 1, y], [x + 1, y], [x, y - 1], [x, y + 1]]
          if valid(p[0], p[1])]

def sortedadj(x, y, xd, yd):
    return sorted(adj(x, y), key=lambda p: (p[0] - xd)**2 + (p[1] - yd)**2)

def suppress():
    i = 0
    while i < len(paths) - 1:
        if paths[i][1][0] == paths[i + 1][2][0] or paths[i][1][1] == paths[i + 1][2][1]:
            paths[i][2] = paths[i + 1][2]
            paths.pop(i + 1)
            continue
        i += 1


def find(board, x0, y0, xd, yd):
    init()
    distTo[x0][y0] = 0
    findpath(board, x0, y0, xd, yd)
    paths.reverse()
    suppress()
    return paths

def findp(board, p0, pd):
    return find(board, p0[0], p0[1], pd[0], pd[1])

def findpath(board, x0, y0, xd, yd):
    marked[x0][y0] = True
    global pathFound, paths
    if (x0 == xd and y0 == yd and valid(x0, y0)):
        pathFound = True
        return
    for x, y in sortedadj(x0, y0, xd, yd):
        if not marked[x][y]:
            distTo[x][y] = distTo[x0][y0] + 1
            findpath(board, x, y, xd, yd)
            if pathFound:
                s = ['', (x0, y0), (x, y)]
                paths.append(s)
                break
    return paths



def findposition(pieces):
    for x in range(lenx):
        for y in range(leny):
            if b[x][y] == pieces:
                return (x, y)

def findall():
    allpaths = findstart1() + findbox1() + findstart2() + findbox2()
    print(allpaths)
    for p in allpaths:
        print(p)

def findbox1():
    global paths
    p0 = findposition(BOX1)
    pd = findposition(DES1)
    findp(b, p0, pd)
    for path in paths:
        path[0] = 'box1'
    ps = paths
    paths = []
    return ps

def findbox2():
    global paths
    p0 = findposition(BOX2)
    pd = findposition(DES2)
    findp(b, p0, pd)
    for path in paths:
        path[0] = 'box2'
    ps = paths
    paths = []
    return ps

def findstart1():
    global paths
    p0 = findposition(MAN)
    pd = findposition(BOX1)
    b[pd[0]][pd[1]] = EMP
    findp(b, p0, pd)
    for path in paths:
        path[0] = 'empty'
    ps = paths
    paths = []
    b[pd[0]][pd[1]] = BOX1
    return ps


def findstart2():
    global paths
    p0 = findposition(DES1)
    pd = findposition(BOX2)
    b[pd[0]][pd[1]] = EMP
    findp(b, p0, pd)
    for path in paths:
        path[0] = 'empty'
    ps = paths
    paths = []
    b[pd[0]][pd[1]] = BOX2
    return ps

#print(find(b, 1, 2, 1, 1))
findall()

#[['empty', (1, 3), (1, 2)], ['empty', (1, 2), (3, 2)], ['empty', (3, 2), (3, 3)], ['box1', (3, 3), (3, 2)], ['box1', (3, 2), (1, 2)], ['box1', (1, 2), (1, 0)], ['box1', (1, 0), (0, 0)], ['empty', (0, 0), (1, 0)], ['empty', (1, 0), (1, 2)], ['empty', (1, 2), (3, 2)], ['empty', (3, 2), (3, 0)], ['box2', (3, 0), (3, 2)], ['box2', (3, 2), (0, 2)], ['box2', (0, 2), (0, 3)]]

#print(sortedadj(1, 1, 0, 3))
#print(find(b, 0, 0, 0, 3))


