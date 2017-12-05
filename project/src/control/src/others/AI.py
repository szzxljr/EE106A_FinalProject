import numpy as np
from map_to_matrix import mapTomatrix



"""
b = [['.1', '#', '-', '.2'],
     ['-', '-', '-', '@'],
     ['#', '#', '-', '#'],
     ['$2', '-', '-', '$1']]
"""
b = [['#', '#', '-', '#'],
    ['#', '#', '$1', '.2'],
    ['.1', '$2', '@', '#'],
    ['#', '-', '-', '#']]

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
BOXS = [BOX1, BOX2]
DESS = [DES1, DES2]
dic = {'BOX1': BOX1, 'BOX2': BOX2, 'DES1': DES1, 'DES2':DES2}
tolit = {BOX1 : 'box1', BOX2 : 'box2'}
PAIRS = list(zip(BOXS, DESS))

undolist = []

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
           and WAL not in b[x][y] and BOX not in b[x][y]
            and not BOX1 == b[x][y] and not BOX2 == b[x][y]);

def adj(x, y):
    #assert '$' in b[x][y], 'Wall or Empty do not have adj.'
    return [[p[0], p[1]]
          for p in [[x - 1, y], [x + 1, y], [x, y - 1], [x, y + 1]]
          if valid(p[0], p[1])]

def sortedadj(x, y, xd, yd):
    return sorted(adj(x, y), key=lambda p: (p[0] - xd)**2 + (p[1] - yd)**2)


def printboard():
    for r in b:
        print(r)
    print('\n')

def printboard2(board):
    for r in board:
        print(r)
    print('\n')

def suppress():
    i = 0
    while i < len(paths) - 1:
        if paths[i][1][0] == paths[i + 1][2][0] or paths[i][1][1] == paths[i + 1][2][1]:
            paths[i][2] = paths[i + 1][2]
            paths.pop(i + 1)
            continue
        i += 1


def havepath(board, x0, y0, xd, yd):
    find(board, x0, y0, xd, yd)
    return not len(paths) == 0

def havep(board, p0, pd):
    return havepath(board, p0[0], p0[1], pd[0], pd[1])

def find(board, x0, y0, xd, yd):
    init()
    distTo[x0][y0] = 0
    findpath(board, x0, y0, xd, yd)
    paths.reverse()
    #suppress()
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

def findposition(piece):
    for x in range(lenx):
        for y in range(leny):
            if b[x][y] == piece:
                return (x, y)

def findposition2(b, piece):
    for x in range(lenx):
        for y in range(leny):
            if piece in b[x][y]:
                return (x, y)

def findallposition(piece):
    ps = []
    for x in range(lenx):
        for y in range(leny):
            if b[x][y] == piece:
                ps.append((x, y))
    return ps

def findallposition2(board, piece):
    ps = []
    for x in range(lenx):
        for y in range(leny):
            if board[x][y] == piece:
                ps.append((x, y))
    return ps
def move(x0, y0, xd, yd):
    """destination is illegal"""
    undolist.append((x0, y0, xd, yd))
    b[x0][y0], b[xd][yd] = b[xd][yd], b[x0][y0]

def movep(p0, pd):
    move(p0[0], p0[1], pd[0], pd[1])

def move2(board, x0, y0, xd, yd):
    """destination is illegal"""
    curP, desP = b[x0][y0], board[xd][yd]
    if isinstance(curP, list):
        if DES in desP:
            board[x0][y0], board[xd][yd] = EMP, board[x0][y0]
        elif EMP in desP:
            board[x0][y0], board[xd][yd] = curP[1], curP[0]
    elif BOX in desP or DES in desP:
        board[x0][y0], board[xd][yd] = EMP, [board[x0][y0], board[xd][yd]]
    undolist.append((x0, y0, xd, yd))


def movep2(board, p0, pd):
    move2(board, p0[0], p0[1], pd[0], pd[1])

def undomove():
    xd, yd, x0, y0 = undolist.pop()
    move(x0, y0, xd, yd)

def findmanTobox(pair):
    p0, pd = findposition(MAN), findposition(pair[0])
    b[pd[0]][pd[1]] = EMP
    ps = findp(b, p0, pd)
    b[pd[0]][pd[1]] = pair[0]
    return ps


def findbridge():
    def otherpair(pair):
        if pair[0] == BOX1:
            return (BOX2, DES2)
        return (BOX1, DES1)
    for pair in PAIRS:
        for pd in findallposition(EMP):
            p0 = findposition(pair[0])
            movep(p0, pd)
            p20, p2d = findposition(otherpair(pair)[0]), findposition(otherpair(pair)[1])
            if havep(b, p20, p2d):
                undomove()
                pman = findposition(MAN)
                ps = findmanTobox(pair)
                for p in ps:
                    p[0] = 'empty'
                pss = findp(b, p0, pd)
                for p in pss:
                    p[0] = tolit[pair[0]]
                ps += pss
                movep(p0, pd)
                """
                b[p20[0]][p20[1]] = EMP
                pss = findp(b, pd, p20)
                b[p20[0]][p20[1]] = otherpair(pair)[0]
                """
                pss = findp(b, pd, pman)
                for p in pss:
                    p[0] = 'empty'
                ps += pss
                return ps
            undomove()
    return False



def validbox():
    global paths, PAIRS
    for pair in PAIRS:
        p0, pd = findposition(pair[0]), findposition(pair[1])
        if havep(b, p0, pd):
            PAIRS.remove(pair)
            return pair
    return False

def findall():
    """
    allpaths = findstart1() + findbox1() + findstart2() + findbox2()
    end = ['empty', allpaths[-1][1], allpaths[-1][1]]
    allpaths.append(end)
    print(allpaths)
    for p in allpaths:
        print(p)
    """
    return findwholeall()

"""
def translate(ps):
    trans = {'empty': EMP, 'box1': BOX1, 'box2': BOX2}
    return map(lambda p : p[0] = trans[p[0]], ps)
"""

def findwholeall():
    global paths, PAIRS
    ps = []
    while len(PAIRS) > 0:
        pair = validbox()
        if not pair:
            ps += findbridge()
            pair = validbox()
        if len(PAIRS) == 1:
            start = MAN
        p0, pd = findposition(start), findposition(pair[0])
        start = pair[0]
        b[pd[0]][pd[1]] = EMP
        findp(b, p0, pd)
        b[pd[0]][pd[1]] = pair[0]
        for path in paths:
            path[0] = 'empty'
        ps += paths
        p0, pd = findposition(pair[0]), findposition(pair[1])
        findp(b, p0, pd)
        movep(p0, pd)
        for path in paths:
            path[0] = tolit[pair[0]]
        ps += paths
        end = ['empty', ps[-1][2], ps[-1][2]]
        ps.append(end)
        paths = ps
    start = ps[0]
    ps.insert(0, [start[0], start[1], start[1]])
    return ps

def split_moves(moves, factor=3):
    splitmovs = []
    for mov in moves:
        piece, p0, pd = mov[0], mov[1], mov[2]
        x0, y0 = p0
        xd, yd = pd
        xs = np.linspace(x0, xd, factor)
        ys = np.linspace(y0, yd, factor)
        ps = np.dstack((xs, ys))[0]
        for i in range(len(ps) - 1):
            splitmovs.append([piece, (ps[i][0], ps[i][1]), (ps[i + 1][0], ps[i + 1][1])])
    return splitmovs



"""
printboard()
print(findbridge())
printboard()
"""
#print(findwholeall())


#print(findall())



def search():
    global b
    b = mapTomatrix()
    print "The original board is: "
    printboard()
    ps = findall()
    print "The planning paths is: "
    for p in ps:
        print p
    print ""
    #ps = split_moves(ps, 3)
    return ps

# search()

"""
['#', '#', '-', '.1']
['#', '-', '$2', '#']
['$1', '-', '#', '@']
['#', '-', '.2', '#']

#print(find(b, 1, 2, 1, 1))
#findall()
#print search()

#[['empty', (1, 3), (1, 2)], ['empty', (1, 2), (3, 2)], ['empty', (3, 2), (3, 3)], ['box1', (3, 3), (3, 2)], ['box1', (3, 2), (1, 2)], ['box1', (1, 2), (1, 0)], ['box1', (1, 0), (0, 0)], ['empty', (0, 0), (1, 0)], ['empty', (1, 0), (1, 2)], ['empty', (1, 2), (3, 2)], ['empty', (3, 2), (3, 0)], ['box2', (3, 0), (3, 2)], ['box2', (3, 2), (0, 2)], ['box2', (0, 2), (0, 3)]]

#print(sortedadj(1, 1, 0, 3))
#print(find(b, 0, 0, 0, 3))

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
"""
# print search()