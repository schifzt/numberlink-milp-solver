from mip import *
import numpy as np


def solve(board_org: np.ndarray):
    I,J = board_org.shape
    N = np.max(board_org)

    working_board: np.ndarray = np.copy(board_org)

    # add sentinel points to a board
    working_board = np.insert(working_board, [0, J], np.full((I,1), -1), axis=1)
    working_board = np.insert(working_board, [0, I], np.full(J+2, -1), axis=0)

    model = Model(sense=MINIMIZE, solver_name=CBC)

    # define variables
    x = {}
    for i in range(I+2):
        for j in range(J+2):
            for n in range(1,N+1):
                x[f"x_{i}_{j}_{n}"] = model.add_var(var_type=BINARY, name=f"x_{i}_{j}_{n}")

    # define constraints & objective
    for i in range(I+2):
        for j in range(J+2):
            v = working_board[(i,j)]
            if v == -1:
                # (i,j) is a sentinel point

                # if a point $(i,j)$ is a sentinel point, $x_{i,j,n}=0$
                for n in range(1,N+1):
                    model.add_constr(x[f"x_{i}_{j}_{n}"] == 0, f"c1_{i}_{j}_{n}")

            if v > 0:
                # (i,j) is a start/end point
                n = v

                # if a point $(i,j)$ is a $n$-th start/end point, $x_{i,j,n}=1$
                model.add_constr(x[f"x_{i}_{j}_{n}"] == 1, f"c2_{i}_{j}_{n}")

                # if a point $(i,j)$ is a $n$-th start/end point, $x_{i-1,j,n}+x_{i+1,j,n}+x_{i,j-1,n}+x_{i-1,j+1,n}=1$
                model.add_constr(x[f"x_{i-1}_{j}_{n}"] + x[f"x_{i+1}_{j}_{n}"] + x[f"x_{i}_{j-1}_{n}"] + x[f"x_{i}_{j+1}_{n}"] == 1, f"c3_{i}_{j}_{n}")

            if v != -1:
                # (i,j) is a path candidate point

                # $\forall i,j \sum_n x_{i,j,n}=1$
                model.add_constr(xsum(x[f"x_{i}_{j}_{n}"] for n in range(1,N+1)) <= 1, f"c4_{i}_{j}_{n}")

                for n in range(1,N+1):
                    # $\forall i,j,n 2*x_{i,j,n} <= x_{i-1,j,n}+x_{i+1,j,n}+x_{i,j-1,n}+x_{i-1,j+1,n}$
                    # model.add_constr(2*x[f"x_{i}_{j}_{n}"] <= x[f"x_{i-1}_{j}_{n}"] + x[f"x_{i+1}_{j}_{n}"] + x[f"x_{i}_{j-1}_{n}"] + x[f"x_{i}_{j+1}_{n}"], f"c5#1_{i}_{j}_{n}")

                    # $\forall i,j,n x_{i-1,j,n}+x_{i+1,j,n}+x_{i,j-1,n}+x_{i-1,j+1,n} <= 4 - 2*x_{i,j,n}$
                    model.add_constr(x[f"x_{i-1}_{j}_{n}"] + x[f"x_{i+1}_{j}_{n}"] + x[f"x_{i}_{j-1}_{n}"] + x[f"x_{i}_{j+1}_{n}"] <= 4 - 2*x[f"x_{i}_{j}_{n}"], f"c5#2_{i}_{j}_{n}")


    model.objective = minimize(xsum(x[f"x_{i}_{j}_{n}"] for i in range(1,I+1) for j in range(1,J+1) for n in range(1,N+1)))

    model.write("model.lp")
    status = model.optimize()
    # print(model.search_progress_log.write("model.plog"))

    if status == OptimizationStatus.OPTIMAL:
        print(f"optimal solution cost {model.objective_value} found")
    elif status == OptimizationStatus.FEASIBLE:
        print(f"sol.cost {model.objective_value} found, best possible: {model.objective_bound}")
    elif status == OptimizationStatus.NO_SOLUTION_FOUND:
        print(f"no feasible solution found, lower bound is: {model.objective_bound}")


    if status == OptimizationStatus.OPTIMAL or status == OptimizationStatus.FEASIBLE:
        answer_board = np.full(board_org.shape, 0)
        c = 0
        for v in model.vars:
            i,j,n = [int(e) for e in v.name.replace('x_', '').split('_')]
            if v.x == 1 and i in range(1,I+1) and j in range(1,J+1):
                answer_board[i-1,j-1] = n
                c+=1
                print(f"({i},{j})->{n}")

        print(c)
        return answer_board

    return None


def asciify(board_org: np.array):
    I,J = board_org.shape
    N = np.max(board_org)
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


if __name__ == "__main__":
    testcase_1 = np.array([
        [2,1,0],
        [0,0,1],
        [0,0,2],
    ], np.int8)

    testcase_2 = np.array([
        [0,0,0,3,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [1,0,2,0,1,0,2],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,3,0,0,0],
    ], np.int8)

    # board = testcase_1
    board = testcase_2

    answer_board = solve(board)
    print(answer_board)

    ascii_board = asciify(answer_board)
    print(ascii_board)
    with open("ascii_board.md", "w", encoding="utf-8") as text_file:
        text_file.write(ascii_board)