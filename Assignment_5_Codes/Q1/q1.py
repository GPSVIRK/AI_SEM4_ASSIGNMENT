import math
import random

# tictactoe

class TicTacToe:
    def __init__(self):
        self.board = [" "] * 9
        self.current_player = "X"

    def clone(self):
        new_game = TicTacToe()
        new_game.board = self.board[:]
        new_game.current_player = self.current_player
        return new_game

    def available_moves(self):
        return [i for i in range(9) if self.board[i] == " "]

    def make_move(self, move):
        if self.board[move] == " ":
            self.board[move] = self.current_player
            self.current_player = "O" if self.current_player == "X" else "X"
            return True
        return False

    def winner(self):
        wins = [
            [0,1,2],[3,4,5],[6,7,8],
            [0,3,6],[1,4,7],[2,5,8],
            [0,4,8],[2,4,6]
        ]

        for combo in wins:
            a,b,c = combo
            if self.board[a] == self.board[b] == self.board[c] != " ":
                return self.board[a]

        if " " not in self.board:
            return "Draw"

        return None

    def is_terminal(self):
        return self.winner() is not None

    def print_board(self):
        for i in range(0,9,3):
            print(self.board[i:i+3])
        print()


# minimax

def minimax(game, maximizing_player):

    result = game.winner()

    if result == "X":
        return 1
    elif result == "O":
        return -1
    elif result == "Draw":
        return 0

    if maximizing_player:
        best = -math.inf

        for move in game.available_moves():
            child = game.clone()
            child.make_move(move)
            best = max(best, minimax(child, False))

        return best

    else:
        best = math.inf

        for move in game.available_moves():
            child = game.clone()
            child.make_move(move)
            best = min(best, minimax(child, True))

        return best


def minimax_best_move(game):

    best_score = -math.inf
    best_move = None

    for move in game.available_moves():
        child = game.clone()
        child.make_move(move)

        score = minimax(child, False)

        if score > best_score:
            best_score = score
            best_move = move

    return best_move


# abpruninig

def alpha_beta(game, alpha, beta, maximizing_player):

    result = game.winner()

    if result == "X":
        return 1
    elif result == "O":
        return -1
    elif result == "Draw":
        return 0

    if maximizing_player:

        value = -math.inf

        for move in game.available_moves():
            child = game.clone()
            child.make_move(move)

            value = max(
                value,
                alpha_beta(child, alpha, beta, False)
            )

            alpha = max(alpha, value)

            if alpha >= beta:
                break

        return value

    else:

        value = math.inf

        for move in game.available_moves():
            child = game.clone()
            child.make_move(move)

            value = min(
                value,
                alpha_beta(child, alpha, beta, True)
            )

            beta = min(beta, value)

            if alpha >= beta:
                break

        return value


def alpha_beta_best_move(game):

    best_score = -math.inf
    best_move = None

    for move in game.available_moves():
        child = game.clone()
        child.make_move(move)

        score = alpha_beta(
            child,
            -math.inf,
            math.inf,
            False
        )

        if score > best_score:
            best_score = score
            best_move = move

    return best_move


# heuristic ab

def heuristic_evaluation(game):

    winner = game.winner()

    if winner == "X":
        return 100

    if winner == "O":
        return -100

    lines = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]

    score = 0

    for line in lines:
        values = [game.board[i] for i in line]

        if values.count("X") == 2 and values.count(" ") == 1:
            score += 10

        if values.count("O") == 2 and values.count(" ") == 1:
            score -= 10

        if values.count("X") == 1 and values.count(" ") == 2:
            score += 1

        if values.count("O") == 1 and values.count(" ") == 2:
            score -= 1

    return score


def heuristic_alpha_beta(game, depth, alpha, beta, maximizing):

    if depth == 0 or game.is_terminal():
        return heuristic_evaluation(game)

    if maximizing:

        value = -math.inf

        for move in game.available_moves():
            child = game.clone()
            child.make_move(move)

            value = max(
                value,
                heuristic_alpha_beta(
                    child,
                    depth - 1,
                    alpha,
                    beta,
                    False
                )
            )

            alpha = max(alpha, value)

            if alpha >= beta:
                break

        return value

    else:

        value = math.inf

        for move in game.available_moves():
            child = game.clone()
            child.make_move(move)

            value = min(
                value,
                heuristic_alpha_beta(
                    child,
                    depth - 1,
                    alpha,
                    beta,
                    True
                )
            )

            beta = min(beta, value)

            if alpha >= beta:
                break

        return value


def heuristic_best_move(game, depth=4):

    best_move = None
    best_score = -math.inf

    for move in game.available_moves():
        child = game.clone()
        child.make_move(move)

        score = heuristic_alpha_beta(
            child,
            depth - 1,
            -math.inf,
            math.inf,
            False
        )

        if score > best_score:
            best_score = score
            best_move = move

    return best_move


# monte carlo

class MCTSNode:

    def __init__(self, game, parent=None, move=None):
        self.game = game
        self.parent = parent
        self.move = move

        self.children = []
        self.visits = 0
        self.wins = 0

    def is_fully_expanded(self):
        return len(self.children) == len(
            self.game.available_moves()
        )

    def best_child(self, c=1.414):

        best_score = -math.inf
        best_node = None

        for child in self.children:

            exploit = child.wins / child.visits
            explore = c * math.sqrt(
                math.log(self.visits) / child.visits
            )

            score = exploit + explore

            if score > best_score:
                best_score = score
                best_node = child

        return best_node


def rollout(game):

    sim = game.clone()

    while not sim.is_terminal():
        move = random.choice(sim.available_moves())
        sim.make_move(move)

    result = sim.winner()

    if result == "X":
        return 1

    if result == "O":
        return -1

    return 0


def mcts(root_game, iterations=1000):

    root = MCTSNode(root_game)

    for _ in range(iterations):

        node = root

        # Selection
        while node.children and node.is_fully_expanded():
            node = node.best_child()

        # Expansion
        if not node.game.is_terminal():

            tried = {c.move for c in node.children}

            untried = [
                m for m in node.game.available_moves()
                if m not in tried
            ]

            if untried:
                move = random.choice(untried)

                new_game = node.game.clone()
                new_game.make_move(move)

                child = MCTSNode(
                    new_game,
                    parent=node,
                    move=move
                )

                node.children.append(child)
                node = child

        # Simulation
        reward = rollout(node.game)

        # Backpropagation
        while node:

            node.visits += 1

            if reward == 1:
                node.wins += 1
            elif reward == 0:
                node.wins += 0.5

            node = node.parent

    best = max(root.children, key=lambda c: c.visits)

    return best.move


# test cases

def run_tests():

    game = TicTacToe()

    game.board = [
        "X","O","X",
        " ","O"," ",
        " "," "," "
    ]

    game.current_player = "X"

    print("Current Board:")
    game.print_board()

    print("Minimax Move:",
          minimax_best_move(game))

    print("Alpha-Beta Move:",
          alpha_beta_best_move(game))

    print("Heuristic Alpha-Beta Move:",
          heuristic_best_move(game))

    print("MCTS Move:",
          mcts(game, iterations=2000))


if __name__ == "__main__":
    run_tests()
