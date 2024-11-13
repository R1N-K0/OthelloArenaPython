import random
import copy
import OthelloLogic
import numpy as np

# Qテーブル
q_table = {}

alpha = 0.1   # 学習率
gamma = 0.9   # 割引率
epsilon = 0.2 # 探索率

def getAction(board, moves):
    print("現在の盤面")
    print(board)

    print("自分が石を置ける場所のリスト")
    print(moves)

    # Q-Learningに基づいて次の手を選択
    next_move = select_move(board, moves)
    print("次に石を置く予定の場所")
    print(next_move)

    # next_moveに石を置いた場合の次の盤面を取得する
    # OthelloLogic.executeの第1引数は現在の盤面、第2引数はこれから石を置く場所、第3引数は石を置く人が自分のAIなら1で、対戦相手なら-1に設定、第4引数は盤面の大きさで8×8なら8を設定
    next_board = OthelloLogic.execute(copy.deepcopy(board), next_move, 1, 8)
    opponent_moves = OthelloLogic.getMoves(next_board, -1, 8)
    print("次の盤面")
    print(next_board)

    print("相手が石を置ける場所のリスト")
    print(opponent_moves)
    # 報酬を取得
    reward = get_reward(next_board)
    print("報酬")
    print(reward)

    update_table(board, next_move, next_board, reward, opponent_moves)

    print("Qテーブル")
    print(q_table)

    return list(next_move)

def select_move(board, moves):
    if random.random() < epsilon:
        move = random.choice(moves)
        return  tuple(move)
    else:
        #  Q値が最大となる手を選択
        q_list = [q_table.get((tuple(map(tuple, board)), tuple(move)), 0) for move in moves]
        move = moves[np.argmax(q_list)]
        return tuple(move)    


def update_table(board, move, next_board, reward, opponent_moves):
    
    board_state = tuple(map(tuple, board))
    next_board_state = tuple(map(tuple, next_board))

    current_q = q_table.get((board_state, move), 0)

    # 相手が次に打つ手の中で最大のQ値を取得
    if len(opponent_moves) == 0:
        next_q = 0
    else:
        next_q_list = [q_table.get((tuple(map(tuple, board)), tuple(opponent_move)), 0) for opponent_move in opponent_moves]
        next_q = max(next_q_list)
    
    # Q値を更新
    # Q学習の更新式
    new_q = current_q + alpha * (reward + gamma * next_q - current_q)
    q_table[(board_state, move)] = new_q


# この報酬を変更することで、AIの学習方法を変更できる
def get_reward(board):
    # 例：勝利なら+1、敗北なら-1、引き分けまたは中間状態なら0
    if is_winning_state(board):
        return 1
    elif is_losing_state(board):
        return -1
    else:
        return 0

# 勝利と敗北の状態を確認するための関数（例）
def is_winning_state(next_board):
    # 勝利条件を定義
    my_stones = sum(row.count(1) for row in next_board)
    
    
    return my_stones > 32

def is_losing_state(next_board):
    # 敗北条件を定義
 
    opponent_stones = sum(row.count(-1) for row in next_board)

    return opponent_stones > 32