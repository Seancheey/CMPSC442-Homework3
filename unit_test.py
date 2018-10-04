from qxs20 import *


def test_tile_puzzle():
    b = [[1, 2, 3], [4, 0, 5], [6, 7, 8]]
    p = TilePuzzle(b)
    print p.calc_distance()
    print "length of solution(a*): {}".format(len(p.find_solution_a_star()))
    print list(p.find_solutions_iddfs())


def test_disk_puzzle():
    p = create_disk_puzzle(7, 6)
    print p
    for move in p.solve():
        p.move(move[0], move[1])
        print p


if __name__ == "__main__":
    # TODO test solve when a puzzle is already solved
    test_tile_puzzle()
