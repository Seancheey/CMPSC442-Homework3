from qxs20 import *

if __name__ == "__main__":
    b = [[1, 2, 3], [4, 0, 5], [6, 7, 8]]
    p = TilePuzzle(b)
    print p.calc_distance()
    print p.find_solution_a_star()
