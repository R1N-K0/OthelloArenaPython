import random
import copy
import OthelloLogic

# 序盤、中盤、終盤の盤面の重み付け
early_weight = [
    [30, -12, 0, -1, -1, 0, -12, 30],
    [-12, -15, -3, -3, -3, -3, -15, -12],
    [0, -3, 0, -1, -1, 0, -3, 0],
    [-1, -3, -1, -1, -1, -1, -3, -1],
    [-1, -3, -1, -1, -1, -1, -3, -1],
    [0, -3, 0, -1, -1, 0, -3, 0],
    [-12, -15, -3, -3, -3, -3, -15, -12],
    [30, -12, 0, -1, -1, 0, -12, 30]
]

mid_weight = [
    [80, -22, 0, -1, -1, 0, -22, 80],
    [-22, -25, -3, -3, -3, -3, -25, -22],
    [0, -3, 0, -1, -1, 0, -3, 0],
    [-1, -3, -1, 0, 0, -1, -3, -1],
    [-1, -3, -1, 0, 0, -1, -3, -1],
    [0, -3, 0, -1, -1, 0, -3, 0],
    [-22, -25, -3, -3, -3, -3, -25, -22],
    [80, -22, 0, -1, -1, 0, -22, 80]
]

late_weight = [
    [15, -3, 1, 1, 1, 1, -3, 15],
    [-3, -3, 1, 1, 1, 1, -3, -3],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [-3, -3, 1, 1, 1, 1, -3, -3],
    [15, -3, 1, 1, 1, 1, -3, 15]
]

# 現在の局面を判定
def get_phase(board):
    empty_squares = sum(1 for row in board for cell in row if cell == 0)
    if empty_squares > 48:  # 序盤
        return "early"
    elif empty_squares > 16:  # 中盤
        return "mid"
    else:  # 終盤
        return "late"

# 局面に応じた重み付けを選択
def get_weight(phase):
    if phase == "early":
        return early_weight
    elif phase == "mid":
        return mid_weight
    else:
        return late_weight

# 評価関数
def evaluate_board(board, phase):
    board_weight = get_weight(phase)
    my_score = 0
    opponent_moves = len(OthelloLogic.getMoves(board, -1, 8))
    
    for x in range(8):
        for y in range(8):
            if board[x][y] == 1:  # 自分の石
                my_score += board_weight[x][y]
            elif board[x][y] == -1:  # 相手の石
                my_score -= board_weight[x][y]
    
    if phase == "early":
        return my_score - opponent_moves * 1.0
    elif phase == "mid":
        return my_score - opponent_moves * 0.5
    else:  # late
        my_count = sum(1 for row in board for cell in row if cell == 1)
        opponent_count = sum(1 for row in board for cell in row if cell == -1)
        return my_count - opponent_count - opponent_moves * 0.3

# Minimaxアルゴリズム
def minimax(board, depth, is_maximizing, alpha, beta, phase):
    if depth == 0:
        return evaluate_board(board, phase), None

    if is_maximizing:
        max_eval = -float('inf')
        best_move = None
        moves = OthelloLogic.getMoves(board, 1, 8)
        if not moves:
            return evaluate_board(board, phase), None
        for move in moves:
            next_board = OthelloLogic.execute(copy.deepcopy(board), move, 1, 8)
            eval, _ = minimax(next_board, depth - 1, False, alpha, beta, phase)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        moves = OthelloLogic.getMoves(board, -1, 8)
        if not moves:
            return evaluate_board(board, phase), None
        for move in moves:
            next_board = OthelloLogic.execute(copy.deepcopy(board), move, -1, 8)
            eval, _ = minimax(next_board, depth - 1, True, alpha, beta, phase)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move

# getAction関数
def getAction(board, moves):
    # print("現在の盤面")
    # print(board)
    # print("自分が石を置ける場所のリスト")
    # print(moves)

    if not moves:
        return None

    # 現在の局面を判定
    phase = get_phase(board)
    # print(f"現在の局面: {phase}")

    # Minimaxで最適な手を探索 (探索深さ2)
    _, best_move = minimax(board, depth=1, is_maximizing=True, alpha=-float('inf'), beta=float('inf'), phase=phase)

    # print("次に石を置く予定の場所")
    # print(best_move)

    return best_move