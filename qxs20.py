############################################################
# CMPSC 442: Homework 3
############################################################

student_name = "Qiyi Shan"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
from random import choice
from Queue import PriorityQueue


class LinkedMoves:
    def __init__(self, move, last_move=None):
        self.move = move
        self.last_move = last_move

    def __str__(self):
        return str(self.list)

    @property
    def list(self):
        return list(self.iter_move())

    def __iter__(self):
        return iter(self.list)

    def iter_move(self):
        if self.last_move:
            for ele in self.last_move.iter_move():
                yield ele
        yield self.move


############################################################
# Section 1: Tile Puzzle
############################################################

def create_tile_puzzle(rows, cols):
    return TilePuzzle(
        [[(r * cols + c + 1) % (rows * cols) for c in range(cols)] for r in range(rows)]
    )


class TilePuzzle(object):
    __slots__ = "board", "zero_pos", "rnum", "cnum"
    moves = {
        "up": (0, -1),
        "down": (0, 1),
        "left": (-1, 0),
        "right": (1, 0)
    }

    # Required
    def __init__(self, board, zero_pos=None):
        self.board = board
        self.rnum = len(board)
        self.cnum = len(board[0])
        if zero_pos is None:
            for y in range(self.rnum):
                for x in range(self.cnum):
                    if self.board[x][y] == 0:
                        self.zero_pos = (y, x)
        else:
            self.zero_pos = zero_pos

    def __str__(self):
        return "\n".join([" ".join([str(i) for i in row]) for row in self.board]) + "\n"

    def get_board(self):
        return self.board

    def perform_move(self, direction):
        if direction in TilePuzzle.moves:
            dx, dy = TilePuzzle.moves[direction]
            x, y = self.zero_pos
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.cnum and 0 <= ny < self.rnum:
                self.board[ny][nx], self.board[y][x] = self.board[y][x], self.board[ny][nx]
                self.zero_pos = (nx, ny)
                return True
            else:
                return False
        else:
            raise AssertionError("direction illegal: %s with type %s" % (direction, type(direction)))

    def avaliable_moves(self):
        # uniform cost: down/right is better than up/left
        mvs = ["down", "right", "left", "up"]
        x, y = self.zero_pos
        if x == 0:
            mvs.remove("left")
        elif x == self.cnum - 1:
            mvs.remove("right")
        if y == 0:
            mvs.remove("up")
        elif y == self.rnum - 1:
            mvs.remove("down")
        return mvs

    def scramble(self, num_moves):
        for _ in range(num_moves):
            self.perform_move(choice(TilePuzzle.moves.keys()))

    def is_solved(self):
        grid_num = self.rnum * self.cnum
        for y in range(self.rnum):
            for x in range(self.cnum):
                if self.board[y][x] != (y * self.cnum + x + 1) % grid_num:
                    return False
        return True

    def copy(self):
        return TilePuzzle([[n for n in r] for r in self.board], self.zero_pos)

    def successors(self):
        for move in self.avaliable_moves():
            new = self.copy()
            new.perform_move(move)
            yield (move, new)

    def calc_distance(self):
        score = 0
        for y in range(self.rnum):
            for x in range(self.cnum):
                num = self.board[y][x]
                if num == 0:
                    continue
                target_x = (num - 1) % self.cnum
                target_y = (num - 1) // self.rnum
                score += abs(x - target_x) + abs(y - target_y)
        return score

    def target_pos(self, num):
        return (num - 1) % self.cnum, (num - 1) // self.rnum

    def calc_conflict(self):
        # test col conflicts
        cost = 0
        for x in range(self.cnum - 1):
            for y in range(self.rnum - 1):
                n_origin = self.board[y][x]
                if n_origin == 0:
                    continue
                xt, yt = self.target_pos(n_origin)
                if (xt == x and yt == y) or (xt != x and yt != y):
                    continue
                if xt == x:
                    cost += ((x, y) == self.target_pos(self.board[y + 1][x]))
                elif yt == y:
                    cost += ((x, y) == self.target_pos(self.board[y][x + 1]))
        return cost

    def calc_cost(self):
        return self.calc_distance() + self.calc_conflict() * 2

    # Required
    def find_solutions_iddfs(self):
        if self.is_solved():
            yield []
            return
        depth = 0
        solved = False
        while not solved:
            depth += 1
            print "testing depth = %d" % depth
            for sol in self.iddfs_helper(depth, None):
                yield sol
                solved = True

    def iddfs_helper(self, depth_limit, last_move):
        if depth_limit == 0:
            if self.is_solved():
                yield last_move.list
        else:
            for move, suc in self.successors():
                if not last_move or TilePuzzle.moves[move][0] != -TilePuzzle.moves[last_move.move][0] or \
                        TilePuzzle.moves[move][1] != -TilePuzzle.moves[last_move.move][1]:
                    for sol in suc.iddfs_helper(depth_limit - 1, LinkedMoves(move, last_move=last_move)):
                        yield sol

    # Required
    def find_solution_a_star(self):
        q = PriorityQueue()
        known_board = [self.board]
        # put self's score, move, board into queue
        q.put((self.calc_distance(), None, self))
        while not q.empty():
            _, last_move, puzzle = q.get()
            for move, suc in puzzle.successors():
                if suc.is_solved():
                    return LinkedMoves(move, last_move=last_move).list
                if suc.board not in known_board:
                    known_board.append(suc.board)
                    q.put((suc.calc_cost(), LinkedMoves(move, last_move=last_move), suc))


############################################################
# Section 2: Grid Navigation
############################################################
def _euclidean_dis(start, goal):
    return ((start[0] - goal[0]) ** 2 + (start[1] - goal[1]) ** 2) ** 0.5


def find_path(start, goal, scene):
    q = PriorityQueue()
    known_points = [start]
    # put (euc dis+travel cost, move list, cumulative travel cost)
    q.put((0, LinkedMoves(start), 0))
    while not q.empty():
        _, last_move, travel_cost = q.get()
        for ydiff in range(-1, 2):
            for xdiff in range(-1, 2):
                lastp = last_move.move
                newp = (lastp[0] + xdiff, lastp[1] + ydiff)
                if newp[1] < 0 or newp[1] >= len(scene[0]) or newp[0] < 0 or newp[0] >= len(scene):
                    continue
                if scene[newp[0]][newp[1]] or newp in known_points:
                    continue
                if newp == goal:
                    return LinkedMoves(newp, last_move=last_move).list
                known_points.append(newp)
                step_cost = abs(xdiff) + abs(ydiff)
                q.put((_euclidean_dis(newp, goal) + travel_cost + step_cost, LinkedMoves(newp, last_move=last_move),
                       travel_cost + step_cost))
    print("unsolvable")
    return []


############################################################
# Section 3: Linear Disk Movement, Revisited
############################################################

class DiskPuzzle(object):
    __slots__ = "board", "board_len", "disk_num"
    empty = -1
    NA = 10086

    def __init__(self, board, disk_num):
        self.disk_num = disk_num
        self.board = board
        self.board_len = len(self.board)

    def copy(self):
        return DiskPuzzle(self.board[:], self.disk_num)

    def __str__(self):
        return "".join(["(_)" if chess == DiskPuzzle.empty else "(%d)" % chess for chess in self.board])

    def solved(self):
        for i in range(1, self.disk_num + 1):
            if self.board[-i] != i - 1:
                return False
        return True

    def move(self, start, end):
        self.board[start], self.board[end] = self.board[end], self.board[start]
        return self

    def successors(self, iterated_board=None):
        if iterated_board is None:
            iterated_board = []
        for i, disk in enumerate(self.board):
            if disk == DiskPuzzle.empty:
                continue
            diffs = [2, 1, -1, -2]
            for diff in diffs:
                if self.get(i + diff) == DiskPuzzle.empty and (
                        (i + diff - 1) == i or (self.get(i + diff - 1) != DiskPuzzle.empty)):
                    new_puzzle = self.copy().move(i, i + diff)
                    if new_puzzle.board not in iterated_board:
                        yield ((i, i + diff), new_puzzle)

    def get(self, pos):
        return self.board[pos] if self.board_len > pos >= 0 else DiskPuzzle.NA

    def heuristic_cost(self):
        cost = 0
        for i, chess in enumerate(self.board):
            if chess == DiskPuzzle.empty:
                continue
            cost += abs((self.board_len - chess) - i)
        return cost

    def solve(self):
        q = PriorityQueue()
        q.put((self.heuristic_cost(), self, None))
        known = [self.board]
        while not q.empty():
            cost, puzzle, moves = q.get()
            if puzzle.solved():
                return moves
            for move, suc in puzzle.successors():
                if suc.solved():
                    return LinkedMoves(move, moves)
                if not move or not moves or (move[1], move[0]) != moves.move:
                    if suc.board not in known:
                        known.append(suc.board)
                        q.put((suc.heuristic_cost(), suc, LinkedMoves(move, moves)))


def create_disk_puzzle(length, n):
    return DiskPuzzle([i if i < n else DiskPuzzle.empty for i in range(length)], n)


def solve_distinct_disks(length, n):
    return create_disk_puzzle(length, n).solve()


############################################################
# Section 4: Dominoes Game
############################################################

def create_dominoes_game(rows, cols):
    return DominoesGame([[False for _ in range(cols)] for _ in range(rows)])


def _cover_pos(row, col, vertical):
    if vertical:
        return [(row, col), (row + 1, col)]
    else:
        return [(row, col), (row, col + 1)]


class DominoesGame(object):

    # Required
    def __init__(self, board):
        self.board = board
        self.rnum = len(self.board)
        self.cnum = len(self.board[0])

    def get_board(self):
        return self.board

    def reset(self):
        for row in self.board:
            for i in range(len(row)):
                row[i] = False

    def is_legal_move(self, row, col, vertical):
        if row >= self.rnum or col >= self.cnum or row < 0 or col < 0 or self.board[row][col]:
            return False
        if vertical:
            return row + 1 < self.rnum and not self.board[row + 1][col]
        else:
            return col + 1 < self.cnum and not self.board[row][col + 1]

    def legal_moves(self, vertical):
        moves = []
        for y in range(self.rnum - vertical):
            for x in range(self.cnum - (not vertical)):
                if self.is_legal_move(y, x, vertical):
                    moves.append((y, x))
        return moves

    def perform_move(self, row, col, vertical):
        if self.is_legal_move(row, col, vertical):
            self.board[row][col] = True
            self.board[row + vertical][col + (not vertical)] = True

    def game_over(self, vertical):
        return not len(self.legal_moves(vertical))

    def copy(self):
        return DominoesGame([[i for i in row] for row in self.board])

    def successors(self, vertical):
        for move in self.legal_moves(vertical):
            new = self.copy()
            new.perform_move(move[0], move[1], vertical)
            yield (move, new)

    def get_random_move(self, vertical):
        return choice(self.legal_moves(vertical))

    # Required
    def get_best_move(self, vertical, limit):
        return self.mm_value(max, vertical, limit, -1000, 1000)

    def score(self, vertical, is_max):
        if is_max:
            return len(self.legal_moves(vertical)) - len(self.legal_moves(not vertical))
        else:
            return len(self.legal_moves(not vertical)) - len(self.legal_moves(vertical))

    def mm_value(self, mm, vertical, limit, alpha, beta):
        print("{}(a={},b={})".format("max" if mm is max else "min", alpha, beta))
        # base case
        if limit == 1:
            # move, score, leaves visited
            successors = list(self.successors(vertical))
            if len(successors) == 0:
                return None, -1000, 0
            score, move = mm([(game.score(vertical, mm is max), move) for move, game in successors])
            return move, score, len(successors)
        best_move, v, leaves = None, -1000, 0
        # recursive part
        for move, game in self.successors(vertical):
            _, score, l = game.mm_value(max if mm is min else min, not vertical, limit - 1, alpha, beta)
            leaves += l
            v, best_move = mm((v, best_move), (score, move))
            if (mm is max and v >= beta) or (mm is min and v <= alpha):
                print "skip!"
                return move, v, leaves
            alpha = mm(alpha if mm is max else beta, v)
        return best_move, v, leaves


############################################################
# Section 5: Feedback
############################################################

feedback_question_1 = """
7 hours.
"""

feedback_question_2 = """
Optimizing efficiency of my code is the most challenging part.
I found it hard to think up a good heuristic cost for sliding tile puzzle.
"""

feedback_question_3 = """
I enjoyed writing the code although it took me so long.
"""
