import numpy as np

from solver import solve
from view import asciify

if __name__ == "__main__":
    testcase_1 = np.array([
        [2,1,0],
        [0,0,1],
        [0,0,2],
    ], np.int8)

    testcase_2 = np.array([
        [2,1,0,0],
        [0,0,0,1],
        [0,0,2,0],
    ], np.int8)

    testcase_3 = np.array([
        [0,0,0,3,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [1,0,2,0,1,0,2],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,3,0,0,0],
    ], np.int8)

    testcase_4 = np.array([
        [1,0,0,0,0],
        [2,0,0,0,0],
        [0,0,3,0,0],
        [0,0,0,0,0],
        [0,0,1,0,0],
        [0,0,0,0,2],
        [0,0,0,0,3],
    ], np.int8)

    testcase_5 = np.array([
        [0,0,0,0,0,0,0,8,0,0],
        [7,0,0,4,0,0,0,0,0,0],
        [0,0,6,0,0,0,0,0,7,0],
        [0,0,0,0,0,0,4,0,0,0],
        [0,0,6,1,0,0,0,0,8,3],
        [0,2,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,3,0,0],
        [0,0,0,0,2,0,0,5,0,0],
        [0,5,0,0,0,0,1,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
    ], np.int8)

    # input_board = testcase_1
    # input_board = testcase_2
    # input_board = testcase_3
    input_board = testcase_4

    # answer_board = solve(input_board, sense="minimize")
    answer_board = solve(input_board, sense="maximize")

    ascii_board = asciify(answer_board)
    print(ascii_board)
    with open("ascii_board.md", "w", encoding="utf-8") as text_file:
        text_file.write(ascii_board)