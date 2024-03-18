import numpy as np

def asciify(board_org: np.array):
    I,J = board_org.shape

    ascii_board_4d: np.ndarray = np.full(board_org.shape, '', dtype=object)

    for i in range(I):
        for j in range(J):

            v = board_org[i,j]

            # check adjacency
            adj_top, adj_bottom, adj_left, adj_right = False, False, False, False
            try:
                adj_top = (0 < i) and (board_org[i-1,j] == v) and (v > 0)
                adj_bottom = (i < I-1) and (board_org[i+1,j] == v) and (v > 0)
                adj_left = (0 < j) and (board_org[i,j-1] == v) and (v > 0)
                adj_right = (j < J-1) and (board_org[i,j+1] == v) and (v > 0)
            except:
                pass

            t = '┃' if adj_top else '─'
            b = '┃' if adj_bottom else '─'
            l = '━' if adj_left else '│'
            r = '━' if adj_right else '│'

            cl = '━' if adj_left else ' '
            cr = '━' if adj_right else ' '

            c = f'{v}'
            if (not adj_top) and (not adj_bottom) and (not adj_left) and (not adj_right): c = ' '
            elif adj_top & adj_bottom: c = '┃'
            elif adj_top & adj_left: c = '┛'
            elif adj_top & adj_right: c = '┗'
            elif adj_left & adj_right: c = '━'
            elif adj_bottom & adj_left: c = '┓'
            elif adj_bottom & adj_right: c = '┏'

            # default
            ascii_board_4d[(i,j)] = np.array([
                ['┼', '─', t, '─', '┼'],
                [ l , cl , c,  cr,  r ],
                ['┼', '─', b, '─', '┼'],
            ])


            # post-processing for **edge**
            if i == 0:
                # top edge
                ascii_board_4d[(i,j)][0] = np.array(['┳', '━', '━', '━', '┳'])
            if i == I-1:
                # bottom edge
                ascii_board_4d[(i,j)][2] = np.array(['┻', '━', '━', '━', '┻'])
            if j == 0:
                # left edge
                ascii_board_4d[(i,j)][0,0] = '┣'
                ascii_board_4d[(i,j)][1,0] = '┃'
                ascii_board_4d[(i,j)][2,0] = '┣'
            if j == J-1:
                # right edge
                ascii_board_4d[(i,j)][0,-1] = '┫'
                ascii_board_4d[(i,j)][1,-1] = '┃'
                ascii_board_4d[(i,j)][2,-1] = '┫'

            # post-processing for **corner**
            if (i,j) == (0,0):
                # top-left corner
                ascii_board_4d[(i,j)][0,0] = '┏'
            elif (i,j) == (0,J-1):
                # top-right corner
                ascii_board_4d[(i,j)][0,-1] = '┓'
            elif (i,j) == (I-1,0):
                # bottom-left corner
                ascii_board_4d[(i,j)][-1,0] = '┗'
            elif (i,j) == (I-1,J-1):
                # bottom-right corner
                ascii_board_4d[(i,j)][-1,4] = '┛'

            # print(ascii_board_4d[(i,j)])


    # flatten 4d array to 2d array
    ascii_board_2d: np.ndarray = np.full((I*3,J*5), '', dtype=object)
    for i in range(I):
        for j in range(J):
            for k in range(ascii_board_4d[(i,j)].shape[0]):
                for l in range(ascii_board_4d[(i,j)].shape[1]):
                    ascii_board_2d[(3*i+k,5*j+l)] = ascii_board_4d[(i,j)][k,l]

    # eliminate duplicate row
    ascii_board_2d = np.delete(ascii_board_2d, [3*i for i in range(1,I)], axis=0)
    # eliminate duplicate column
    ascii_board_2d = np.delete(ascii_board_2d, [5*j for j in range(1,J)], axis=1)

    # to string
    ascii_board_str: str = '\n'.join(''.join(f'{e}' for e in row) for row in ascii_board_2d)

    return ascii_board_str

