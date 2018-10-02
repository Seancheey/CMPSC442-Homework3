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


class LinkedMoves():
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
        if zero_pos == None:
            for y in range(self.rnum):
                for x in range(self.cnum):
                    if self.board[x][y] == 0:
                        self.zero_pos = (x, y)
        else:
            self.zero_pos = zero_pos

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

    # Required
    def find_solutions_iddfs(self):
        depth = 0
        last_move = None
        solutions = []
        while len(solutions) == 0:
            depth += 1
            self.dls(depth, None, solutions)
        for sol in solutions:
            yield sol

    def dls(self, depth_limit, last_move, solutions):
        if depth_limit == 0:
            if self.is_solved():
                solutions.append(last_move.list)
        else:
            for move, suc in self.successors():
                suc.dls(depth_limit - 1, LinkedMoves(move, last_move=last_move), solutions)

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
                    q.put((suc.calc_distance() + suc.calc_conflict() * 2, LinkedMoves(move, last_move=last_move), suc))


############################################################
# Section 2: Grid Navigation
############################################################

def find_path(start, goal, scene):
    pass


############################################################
# Section 3: Linear Disk Movement, Revisited
############################################################

def solve_distinct_disks(length, n):
    pass


############################################################
# Section 4: Dominoes Game
############################################################

def create_dominoes_game(rows, cols):
    pass


class DominoesGame(object):

    # Required
    def __init__(self, board):
        pass

    def get_board(self):
        pass

    def reset(self):
        pass

    def is_legal_move(self, row, col, vertical):
        pass

    def legal_moves(self, vertical):
        pass

    def perform_move(self, row, col, vertical):
        pass

    def game_over(self, vertical):
        pass

    def copy(self):
        pass

    def successors(self, vertical):
        pass

    def get_random_move(self, vertical):
        pass

    # Required
    def get_best_move(self, vertical, limit):
        pass


############################################################
# Section 5: Feedback
############################################################

feedback_question_1 = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""

feedback_question_2 = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""

feedback_question_3 = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""
