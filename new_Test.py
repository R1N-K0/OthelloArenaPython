import OthelloLogic
import OthelloAction
import random

def create_initial_board(size=8):
    """Othelloの初期盤面を作成"""
    board = [[0 for _ in range(size)] for _ in range(size)]
    mid = size // 2
    board[mid - 1][mid - 1] = -1  # 黒
    board[mid - 1][mid] = 1       # 白
    board[mid][mid - 1] = 1       # 白
    board[mid][mid] = -1          # 黒
    return board


def check_game_over(board, moves, opponent_moves):
    """
    ゲーム終了の条件を判定する
    """
    # 双方とも合法手がない場合ゲーム終了
    if not moves and not opponent_moves:

        ai_stones = sum(row.count(-1) for row in board)
        opponent_stones = sum(row.count(1) for row in board)
        if ai_stones > opponent_stones:
            return True, 1  # 勝利
        elif ai_stones < opponent_stones:
            return True, -1  # 敗北
        else:
            return True, 0  # 引き分け

    return False, 0  # ゲーム続行


def update_weights_func(reward, next_board, ai):
    # aiの次の合法手を取得
    next_moves = OthelloLogic.getMoves(next_board, -1, 8)
    next_board_feature = ai.get_feature(next_board)
    # 重みの更新
    ai.update_weights(reward, next_board_feature, next_moves)    

def main():
    size = 8  # 標準の8x8盤面
    board = create_initial_board(size)
    player = -1  # 黒 (-1) から開始

    ai  = OthelloAction.OthelloQLearning()
    
    # 初期盤面表示
    print("初期盤面")
    OthelloLogic.printBoard(board)

    while True:
        print(f"現在のプレイヤー: {'黒' if player == -1 else '白'}")
        input()
        
        # 合法手を取得
        
        # aiが-1(黒●)
        if player == -1:
            moves = OthelloLogic.getMoves(board, player, size)
            # if not moves:
            #     print(f"{'黒' if player == -1 else '白'}に合法手がないため、パスします。")
                
            #     # 相手にも合法手がない場合は終了
            #     opponent_moves = OthelloLogic.getMoves(board, -player, size)
            #     if not opponent_moves:
            #         print("両者に合法手がないため、ゲーム終了")
            #         break
                
            #     # 自分には合法手がないため、プレイヤー交代
            #     player *= -1  # プレイヤー交代
            #     # これ以降の処理をスキップ
            #     continue

            print(f"合法手: {moves}")
            action = ai.get_action(board, moves)  # 合法手から選択

            # passの処理(Q値も計算済み)
            if action == "pass":
                print(f"{'黒' if player == -1 else '白'}がパスしました。\n")
                player *= -1  # プレイヤー交代
                continue

            if action not in moves:
                print("合法手ではない手が選択されました。")
                exit()

            # 石を置く("execute"は盤面を更新する)
            board = OthelloLogic.execute(board, action, player, size)
            print(f"{'黒' if player == -1 else '白'}が{action}に置きました。\n")
        


        # 学習相手が1(白〇)
        # Q値の更新処理が必要
        else:
            moves = OthelloLogic.getMoves(board, player, size)

            if not moves:
                print(f"{'黒' if player == -1 else '白'}に合法手がないため、パスします。")
                # 相手にも合法手がない場合は終了
                opponent_moves = OthelloLogic.getMoves(board, -player, size)
                if not opponent_moves:

                    game_over, reward = check_game_over(board, moves, opponent_moves)
                    if game_over:
                        if reward == 1:
                            print("黒の勝利")                           
                        elif reward == -1:
                            print("白の勝利")
                        else:
                            print("引き分け")
                            
                        update_weights_func(reward, board, ai)
                        break
                   
                
                # 学習相手には合法手がないため、プレイヤー交代
                # これ以降の処理をスキップ
                # 更新処理必須
                update_weights_func(0, board, ai)
                player *= -1  # プレイヤー交代
                continue
            
            # 合法手がある場合
            # プレイヤーの手を決定（簡易AIとしてランダム選択）
            print(f"合法手: {moves}")
            action = random.choice(moves)  # 合法手から選択

            if action not in moves:
                print("合法手ではない手が選択されました。")
                exit()

            # 石を置く("execute"は盤面を更新する)
            board = OthelloLogic.execute(board, action, player, size)
            print(f"{'黒' if player == -1 else '白'}が{action}に置きました。\n")
            
            # 更新処理
            update_weights_func(0, board, ai)


        # ここから下は共通処理
        # 盤面表示
        OthelloLogic.printBoard(board)

        # プレイヤー交代
        player *= -1

    print("ゲーム終了")
    OthelloLogic.printBoard(board)

    # 重みの確認
    print("学習後の重み:")
    print(ai.weights)

if __name__ == "__main__":
    main()
