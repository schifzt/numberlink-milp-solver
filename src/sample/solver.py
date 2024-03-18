from mip import *
import numpy as np
import sys


def create_mip_model(board_org: np.ndarray) -> object:
    I,J = board_org.shape
    N = np.max(board_org)

    working_board: np.ndarray = np.copy(board_org)

    # replace zero to -1 (to avoid confusion)
    working_board[working_board == 0] = -1

    # add sentinel points to a board
    working_board = np.insert(working_board, [0, J], np.full((I,1), -2), axis=1)
    working_board = np.insert(working_board, [0, I], np.full(J+2, -2), axis=0)

    print(board_org)
    print(working_board)

    model = Model(sense=MINIMIZE, solver_name=CBC)

    # define variables
    x = {}
    n_adjacent = {}
    for i in range(I+2):
        for j in range(J+2):
            for n in range(1,N+1):
                x[f"x_{i}_{j}_{n}"] = model.add_var(var_type=BINARY, name=f"x_{i}_{j}_{n}")
                n_adjacent[f"n_adjacent_{i}_{j}_{n}"] = model.add_var(var_type=INTEGER, name=f"n_adjacent_{i}_{j}_{n}")


    # define constraints & objective
    for i in range(I+2):
        for j in range(J+2):
            v = working_board[(i,j)]

            if v == -2:
                # (i,j) is a sentinel point

                # C1: if a point (i,j) is a sentinel point, x_{i,j,n}=0
                for n in range(1,N+1):
                    model.add_constr(x[f"x_{i}_{j}_{n}"] == 0, f"c1_{i}_{j}_{n}")
                    # model.add_constr(n_adjacent[f"n_adjacent_{i}_{j}_{n}"] == 0, f"adj_{i}_{j}_{n}")
            else:
                # (i,j) on a board

                # C2: define n_adjacent
                for n in range(1,N+1):
                    model.add_constr(n_adjacent[f"n_adjacent_{i}_{j}_{n}"] == x[f"x_{i-1}_{j}_{n}"] + x[f"x_{i+1}_{j}_{n}"] + x[f"x_{i}_{j-1}_{n}"] + x[f"x_{i}_{j+1}_{n}"], f"c2_{i}_{j}_{n}")

                # C3: For all points (i,j) on a board, $\sum_n x_{i,j,n} <= 1$
                model.add_constr(xsum(x[f"x_{i}_{j}_{n}"] for n in range(1,N+1)) <= 1, f"c3_{i}_{j}_{n}")

                if v > 0:
                    # (i,j) is a start/end point
                    n = v
                    # C4: if a point (i,j) is a n-th start/end point, x_{i,j,n}=1
                    model.add_constr(x[f"x_{i}_{j}_{n}"] == 1, f"c4_{i}_{j}_{n}")

                    # C5: if a point $(i,j)$ is a $n$-th start/end point, n_adjacent_{i,j,n}=1
                    model.add_constr(n_adjacent[f"n_adjacent_{i}_{j}_{n}"] == 1, f"c5_{i}_{j}_{n}")

                elif v == -1:
                    # (i,j) is a path candidate point

                    # C6: For all paths and points(i,j) on a candidate points, x_{i,j,n}=1 implies n_adjacent_{i,j,n}=2
                    for n in range(1,N+1):
                        # For all paths and points(i,j) on a candidate points, 2*x_{i,j,n} <= n_adjacent_{i,j,n}.
                        model.add_constr(2*x[f"x_{i}_{j}_{n}"] <= n_adjacent[f"n_adjacent_{i}_{j}_{n}"], f"c6#1_{i}_{j}_{n}")

                        # For all paths and points(i,j) on a candidate points, n_adjacent_{i,j,n} <= 4-2*x_{i,j,n}.
                        model.add_constr(n_adjacent[f"n_adjacent_{i}_{j}_{n}"] <= 4 - 2*x[f"x_{i}_{j}_{n}"], f"c6#2_{i}_{j}_{n}")

    # model.objective = minimize(xsum(x[f"x_{i}_{j}_{n}"] for i in range(1,I+1) for j in range(1,J+1) for n in range(1,N+1)))
    model.objective = maximize(xsum(x[f"x_{i}_{j}_{n}"] for i in range(1,I+1) for j in range(1,J+1) for n in range(1,N+1)))

    model.write("model.lp")

    return model


def solve(board_org: np.ndarray) -> Optional[np.ndarray]:
    I,J = board_org.shape
    N = np.max(board_org)

    model = create_mip_model(board_org)
    status = model.optimize()
    # print(model.search_progress_log.write("model.plog"))

    if status == OptimizationStatus.OPTIMAL:
        print(f"optimal solution cost {model.objective_value} found")
    elif status == OptimizationStatus.FEASIBLE:
        print(f"sol.cost {model.objective_value} found, best possible: {model.objective_bound}")
    elif status == OptimizationStatus.NO_SOLUTION_FOUND:
        print(f"no feasible solution found, lower bound is: {model.objective_bound}")

    if status == OptimizationStatus.OPTIMAL or status == OptimizationStatus.FEASIBLE:
        answer_board = np.full(board_org.shape, -2)
        debug_board= np.full((board_org.shape[0]+2,board_org.shape[1]+2), -2)

        for i in range(I+2):
            for j in range(J+2):
                if i in range(1,I+1) and j in range(1,J+1):
                    n_candidate = [n for n in range(1,N+1) if int(model.vars[f"x_{i}_{j}_{n}"].x) == 1]
                    if len(n_candidate) == 0:
                        n = 0
                    elif len(n_candidate) == 1:
                        n = n_candidate[0]
                    else:
                        print("constraint is not satisfied for some reason.")
                        sys.exit(1)

                    answer_board[i-1,j-1] = n
                    debug_board[i,j] = n

        for i in range(I+2):
            for j in range(J+2):
                for n in range(1,N+1):
                    n_adjacent = int(model.vars[f"n_adjacent_{i}_{j}_{n}"].x)
                    if n_adjacent > 0:
                        print(f"({i},{j}) -> {n_adjacent}")

        print(debug_board)
        return answer_board

    return None

