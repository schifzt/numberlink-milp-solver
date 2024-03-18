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

