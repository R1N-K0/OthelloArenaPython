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
            return True, 1,0.5+0.5* (ai_stones/(ai_stones+opponent_stones))  # 勝利
        elif ai_stones < opponent_stones:
            return True, -1,-0.5-0.5*(opponent_stones/(ai_stones+opponent_stones))  # 敗北
        else:
            return True, 0,0.3  # 引き分け

    return False, 0  # ゲーム続行

def calculate_reward(board, ai_player):
    ai_stones = sum(row.count(ai_player) for row in board)
    opponent_stones = sum(row.count(-ai_player) for row in board)
    total_stones = ai_stones + opponent_stones

    # 石数差の正規化 [-0.5, 0.5]
    stone_diff = (ai_stones - opponent_stones) / total_stones if total_stones > 0 else 0
    stone_diff *= 0.5

    # 合法手の数をスコアに反映し [-0.5, 0.5] に収める
    ai_moves = len(OthelloLogic.getMoves(board, ai_player, len(board)))
    opponent_moves = len(OthelloLogic.getMoves(board, -ai_player, len(board)))
    move_diff = (ai_moves - opponent_moves) / (ai_moves + opponent_moves + 1)  # 正規化
    move_diff *= 0.5

    # 重み付き報酬の合算
    reward = stone_diff + move_diff

    # 最終的な報酬を [-0.5, 0.5] にクリッピング
    return max(-0.5, min(0.5, reward))



def update_weights_func(reward, next_board, ai):
    # aiの次の合法手を取得
    next_moves = OthelloLogic.getMoves(next_board, -1, 8)
    next_board_feature = ai.get_feature(next_board)
    # 重みの更新
    ai.update_weights(reward, next_board_feature, next_moves)    

def play_single_episode(ai, size):
   
    board = create_initial_board(size)
    player = -1  # 黒 (-1) から開始
    
    # 初期盤面表示
    # print("初期盤面")
    # OthelloLogic.printBoard(board)

    while True:
        print(f"現在のプレイヤー: {'黒' if player == -1 else '白'}")
        
        
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

            # print(f"合法手: {moves}")
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

                    game_over, result,reward = check_game_over(board, moves, opponent_moves)
                    if game_over:
                        if result == 1:
                            print("黒の勝利")                           
                        elif result == -1:
                            print("白の勝利")
                        else:
                            print("引き分け")
                            
                        update_weights_func(reward, board, ai)
                        # OthelloLogic.printBoard(board)
                        return result
                   
                
                # 学習相手には合法手がないため、プレイヤー交代
                # これ以降の処理をスキップ
                # 更新処理必須
                reward = calculate_reward(board, player)
                update_weights_func(reward, board, ai)
                player *= -1  # プレイヤー交代
                continue
            
            # 合法手がある場合
            # プレイヤーの手を決定（簡易AIとしてランダム選択）
            # print(f"合法手: {moves}")
            action = random.choice(moves)  # 合法手から選択

            if action not in moves:
                print("合法手ではない手が選択されました。")
                exit()

            # 石を置く("execute"は盤面を更新する)
            board = OthelloLogic.execute(board, action, player, size)
            print(f"{'黒' if player == -1 else '白'}が{action}に置きました。\n")
            
            # 置いた時に試合が終了しているか確認
            next_moves = OthelloLogic.getMoves(board, -player, size)
            if not next_moves:
                opponent_moves = OthelloLogic.getMoves(board, player, size)
                if not opponent_moves: 
                    game_over, result,reward = check_game_over(board, next_moves, opponent_moves)
                    if game_over:
                        if result == 1:
                            # OthelloLogic.printBoard(board)
                            print("黒の勝利")                           
                        elif result == -1:
                            # OthelloLogic.printBoard(board)
                            print("白の勝利")
                        else:
                            # OthelloLogic.printBoard(board)
                            print("引き分け")
                            
                        update_weights_func(reward, board, ai)
                        return result
                    
            
            # 更新処理
            reward = calculate_reward(board, player)
            update_weights_func(reward, board, ai)


        # ここから下は共通処理
        # 盤面表示
        # OthelloLogic.printBoard(board)

        # プレイヤー交代
        player *= -1

    print("ゲーム終了")
    OthelloLogic.printBoard(board)

    # 重みの確認
    print("学習後の重み:")
    print(ai.weights)
   



def main():
    size = 8  # ボードサイズ
    games_to_play = 3000  # 総ゲーム数
    report_interval = 100  # 勝率を報告する間隔
    win_count = 0  # 勝利数カウント
    draw_count = 0  # 引き分け数カウント
    initial_tmp = 0.5  # 初期値
    decay_rate = 0.995  # 減少率

    # 最後の100ゲームの勝率を計算するために
    final_win_count = 0
    final_draw_count = 0
    ai = OthelloAction.OthelloQLearning()
    for game_num in range(1, games_to_play + 1):
            
            if game_num <= game_num- 500:  
                tmp = max(initial_tmp * (decay_rate ** game_num), 0.01)
            else:  # それ以降は固定
                tmp = 0.01
            ai.temperature = tmp

            
            result = play_single_episode(ai, size)
            print("ゲーム結果")
            print(result)
            if result == 1:
                win_count += 1
            elif result == 0:
                draw_count += 1

              # 最後の100ゲームの結果を出力
            if game_num >= games_to_play - 100:
                if result == 1:
                    final_win_count += 1
                elif result == 0:
                    final_draw_count += 1

            # 指定の間隔で勝率を表示
            if game_num % report_interval == 0:
                print(f"ゲーム数: {game_num}, 勝率: {win_count / game_num:.2%}, 引き分け率: {draw_count / game_num:.2%}")

    # 最終結果
    print("全ゲーム終了")
    print(f"総ゲーム数: {games_to_play}")
    print(f"最終勝率: {win_count / games_to_play:.2%}")
    print(f"最終引き分け率: {draw_count / games_to_play:.2%}")
    print(f"最終勝利数: {win_count}")

     # 最後の100ゲームの結果を出力
    print("最後の100ゲーム結果")
    print(f"最後の100ゲーム勝率: {final_win_count / 100:.2%}")
    print(f"最後の100ゲーム引き分け率: {final_draw_count / 100:.2%}")
    
    print(f"学習後の重み:")
    print(ai.weights)


if __name__ == "__main__":
    main()

