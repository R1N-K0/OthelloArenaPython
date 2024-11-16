import OthelloAction
import OthelloLogic
import copy
import pickle
import os




#sizeを変更することでテストプレイする盤面の大きさを変更できます。
#size = 4
#size = 6
size = 8
board = [[0 for i in range(size)] for j in range(size)]
board_temp = board
board[int(size/2)-1][int(size/2)-1] = 1;
board[int(size/2)][int(size/2)-1]=-1;
board[int(size/2)-1][int(size/2)]=-1;
board[int(size/2)][int(size/2)]=1;

# 学習の設定
total_games = 1000
record_interval = 100

# 勝敗記録用
wins = 0
losses = 0
draws = 0

# 勝率の記録
win_rates = []

for game in range(1, total_games + 1):
    board = [row[:] for row in board_temp]
    player = -1
    moves = OthelloLogic.getMoves(board,player,size)
    
    action = []
    while(True):
        
        if(player == -1):
            action = OthelloAction.getAction(OthelloLogic.getReverseboard(board),moves, game, q_table)
        else:
            # ランダムプレイヤーの手を取得
            opponent_move = OthelloAction.get_random_action(board,moves)
              # AIが選んだ手で次の盤面を計算(boardは更新されない)
            next_board = OthelloLogic.execute(copy.deepcopy(board), action, player, size)
            # 相手の手を計算
            next_next_board = OthelloLogic.execute(copy.deepcopy(next_board), opponent_move, -1, size)
            # 報酬を取得
            reward = OthelloAction.get_reward(next_board)
            
            # Qテーブルを更新
            OthelloAction.update_table(board, action, next_next_board, reward, opponent_move, q_table)

            action = opponent_move
        if(not (action in moves)):
            print(board)
            print('合法手ではない手が打たれました' + action)
            exit()
        
        # 盤面を更新
        board = OthelloLogic.execute(board,action,player,size)
        OthelloLogic.printBoard(board)
        print('現在の合法手一覧')
        print(moves)
        moves = OthelloLogic.getMoves(board,player*-1,size)
        if(len(moves) == 0):
            moves = OthelloLogic.getMoves(board,player,size)
            if(len(moves) == 0):
                break
        else:
            player = player * -1

    print('正常に終了しました。')		

    
      # 最終的な石の数を数えて勝敗を決定
    ai_stones = sum(row.count(1) for row in board)
    random_stones = sum(row.count(-1) for row in board)
    
    if ai_stones > random_stones:
        wins += 1
    elif ai_stones < random_stones:
        losses += 1
    else:
        draws += 1

    # 100ゲームごとに勝率を記録
    if game % record_interval == 0:
        win_rate = wins / game
        win_rates.append(win_rate)
        print(f'{game}ゲーム終了時点での勝率: {win_rate * 100:.2f}%')

# 最終的な勝率を表示
print("最終的な勝敗記録")
print("AIの勝利:", wins)
print("ランダムプレイヤーの勝利:", losses)
print("引き分け:", draws)
print("100ゲームごとの勝率:", win_rates)
