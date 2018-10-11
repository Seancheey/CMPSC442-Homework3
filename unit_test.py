from qxs20 import *

timing_test = False


def test_tile_puzzle():
    p1 = TilePuzzle([[4, 1, 2], [0, 5, 3], [7, 8, 6]])
    sol = list(p1.find_solutions_iddfs())
    assert sol == [['up', 'right', 'right', 'down', 'down']]
    print "iddfs(1):\n", sol
    p2 = TilePuzzle([[1, 2, 3], [4, 0, 8], [7, 6, 5]])
    sol = list(p2.find_solutions_iddfs())
    print "iddfs(2):\n", sol
    assert sol == [['down', 'right', 'up', 'left', 'down',
                    'right'], ['right', 'down', 'left',
                               'up', 'right', 'down']]
    p3 = TilePuzzle([[1, 2, 3], [4, 0, 5], [6, 7, 8]])
    sol = p1.find_solution_a_star()
    print "a-star(1):\n", sol
    assert sol == ['up', 'right', 'right', 'down', 'down']
    sol = p3.find_solution_a_star()
    print "a-star(2):\n", sol
    assert sol == ['right', 'down', 'left', 'left', 'up',
                   'right', 'down', 'right', 'up', 'left',
                   'left', 'down', 'right', 'right']
    p_solved = create_tile_puzzle(5, 5)
    assert p_solved.find_solution_a_star() == []
    assert list(p_solved.find_solutions_iddfs()) == [[]]


def test_grid_navigation():
    scene = [[False] * 3 for _ in range(3)]
    sol = find_path((0, 0), (2, 1), scene)
    print "path from (0,0) to (2,1):\n", sol
    assert sol == [(0, 0), (1, 0), (2, 1)]
    scene2 = [[False, True, False] for _ in range(3)]
    print "path should be None here:\n", sol
    sol = find_path((0, 0), (0, 2), scene2)
    print sol
    assert sol is None
    sol = find_path((0, 0), (0, 0), scene)
    assert sol == []


def test_disk_puzzle():
    p = create_disk_puzzle(7, 6)
    print p
    for move in p.solve():
        p.move(move[0], move[1])
        print p
    assert p.solved()
    assert p.solve() == []


def test_dominos():
    b = [[False] * 3 for _ in range(3)]
    g = DominoesGame(b)
    print g
    print g.get_best_move(True, 1)
    print g.get_best_move(True, 2)
    g.perform_move(0, 1, True)
    print g
    print g.get_best_move(False, 1)
    print g.get_best_move(False, 2)
    g.perform_move(2, 1, False)
    print g
    print g.get_best_move(True, 2)
    g.perform_move(0, 0, True)
    print g
    print g.get_best_move(False, 2)
    test_big = [[False] * 5 for _ in range(5)]
    print DominoesGame(test_big).get_best_move(True, 7)


if __name__ == "__main__":
    test_tile_puzzle()
    test_grid_navigation()
    test_disk_puzzle()
    test_dominos()
