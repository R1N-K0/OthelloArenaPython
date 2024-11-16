import random
import copy
import OthelloLogic
import numpy as np
import pickle


alpha = 0.3  # 学習率
gamma = 0.99   # 割引率
epsilon = 0.2 # 探索率


def get_random_action(board, moves):
    return random.choice(moves)

def getAction(board, moves, game_count, q_table):
    print(f"game_count: {game_count}")
    # print("現在の盤面")
    # print(board)

    # print("自分が石を置ける場所のリスト")
    # print(moves)

    # Q-Learningに基づいて次の手を選択
    next_move = select_move(board, moves, game_count, q_table)
    # print("次に石を置く予定の場所")
    # print(next_move)

    return list(next_move)

def select_move(board, moves, game_count, q_table):
    if random.random() < (epsilon / (game_count // 1000 + 1)):
        return random.choice(moves)
    else:
        q_values = [q_table.get((tuple(map(tuple, board)), tuple(move)), 0) for move in moves]
        max_q = max(q_values)
        best_moves = [move for i, move in enumerate(moves) if q_values[i] == max_q]
        return random.choice(best_moves)


def update_table(board, move, next_next_board, reward, opponent_move, q_table):
    
    board_state = tuple(map(tuple, board))
    next_board_state = tuple(map(tuple, next_next_board))

    move = tuple(move)

    # 現在のQ値を取得（なければ0）
    # ここでいう現在のQ値とは、AIが石を置いた後の盤面におけるQ値
    current_q = q_table.get((board_state, move), 0)

    # 相手が石を置ける場所がない場合、次のQ値は0
    if not opponent_move:
        next_q = 0
    
    # 相手が石を置いた場合、その次の最大のQ値
    else:
        next_next_moves = OthelloLogic.getMoves(next_next_board, 1, 8)
        next_q_list = [q_table.get((tuple(map(tuple, next_next_board)), tuple(next_next_move)), 0) for next_next_move in next_next_moves]
        
        if next_q_list:  # next_q_listが空でないことを確認
            next_q = max(next_q_list)
        else:
            next_q = 0  # next_q_listが空であれば0にする
    
    # Q値を更新
    # Q学習の更新式
    new_q = current_q + alpha * (reward + gamma * next_q - current_q)
    q_table[(board_state, move)] = new_q


# この報酬を変更することで、AIの学習方法を変更できる
def get_reward(board):
    # 勝利なら+1、敗北なら-1、引き分けまたは中間状態なら0
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