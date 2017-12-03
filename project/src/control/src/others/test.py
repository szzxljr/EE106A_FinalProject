import numpy as np
def split_moves(moves):
    splitmovs = []
    factor = 10
    for mov in moves:
        piece, p0, pd = mov[0], mov[1], mov[2]
        x0, y0 = p0
        xd, yd = pd
        xs = np.linspace(x0, xd, factor)
        ys = np.linspace(y0, yd, factor)
        ps = np.dstack((xs, ys))[0]
        for p in ps:
            splitmovs.append([piece, p[0], p[1]])
    return splitmovs

moves = [['empty', (2, 3), (2, 2)], ['box1', (2, 2), (1, 2)], ['box1', (1, 2), (1, 1)], ['empty', (1, 1), (1, 2)], ['empty', (1, 2), (2, 2)], ['empty', (2, 2), (2, 3)], ['empty', (2, 3), (2, 2)], ['empty', (2, 2), (0, 2)], ['box2', (0, 2), (3, 2)], ['empty', (3, 2), (3, 2)], ['empty', (3, 2), (1, 2)], ['empty', (1, 2), (1, 1)], ['box1', (1, 1), (1, 2)], ['box1', (1, 2), (0, 2)], ['box1', (0, 2), (0, 3)], ['empty', (0, 3), (0, 3)]]

print split_moves(moves)