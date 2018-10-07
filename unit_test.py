from qxs20 import *

timing_test = False


def test_tile_puzzle():
    if timing_test:
        p_timing = TilePuzzle([[3, 8, 2], [1, 5, 4], [0, 7, 6]])
        print list(p_timing.find_solutions_iddfs())
        print "length of solution(a*): {}".format(len(p_timing.find_solution_a_star()))
    p0 = TilePuzzle([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
    print list(p0.find_solutions_iddfs())
    p1 = TilePuzzle([[4, 1, 2], [0, 5, 3], [7, 8, 6]])
    sol = list(p1.find_solutions_iddfs())
    print sol
    assert sol == [['up', 'right', 'right', 'down', 'down']]


def test_disk_puzzle():
    p = create_disk_puzzle(7, 6)
    print p
    for move in p.solve():
        p.move(move[0], move[1])
        print p


def test_dominos():
    b = [[False] * 3 for i in range(3)]
    g = DominoesGame(b)
    print g.get_best_move(True, 1)
    print g.get_best_move(True, 2)


if __name__ == "__main__":
    # TODO test solve when a puzzle is already solved
    test_dominos()
