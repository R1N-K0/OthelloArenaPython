import OthelloLogic
import OthelloAction
import random
import numpy as np
import matplotlib.pyplot as plt
import math

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
            return True, 1,1
        elif ai_stones < opponent_stones:
            return True, -1,-1
        else:
            return True, 0,0  # 引き分け

    return False, 0  # ゲーム続行

def calculate_intermediate_reward(board, player):
    """中間報酬を計算: 石の数と合法手の数を考慮"""
    # 石の数の差を計算
    player_stones = sum(row.count(player) for row in board)
    opponent_stones = sum(row.count(-player) for row in board)
    stone_diff = (player_stones - opponent_stones) / (player_stones + opponent_stones + 1)  # 正規化

    # 合法手の数を計算
    player_moves = len(OthelloLogic.getMoves(board, player, len(board)))
    opponent_moves = len(OthelloLogic.getMoves(board, -player, len(board)))
    move_diff = (player_moves - opponent_moves) / (player_moves + opponent_moves + 1)  # 正規化

    # 中間報酬を合算
    return 0.5 * stone_diff + 0.5 * move_diff  # ウェイトを調整可能


def update_weights_func(reward, next_board, ai,loss_history):
    # aiの次の合法手を取得
    next_moves = OthelloLogic.getMoves(next_board, -1, 8)
    next_board_feature = ai.get_feature(next_board)
    # 重みの更新
    ai.update_weights(reward, next_board_feature, next_moves,loss_history) 

def update_weights_monte_carlo(ai):
    cumulative_reward = 0  # 累積報酬
    for state, action, reward in reversed(ai.episode_memory):
        cumulative_reward = reward + ai.gamma * cumulative_reward
        state_feature = ai.get_feature(state)
        # passにも対応(actionに値を入れるときにpassが返ってくるようにselected_actionしてる)
        action_index = ai.calc_action_index(action)

        # TD誤差を計算し重みを更新(次の状態に関しては累積報酬を使用)
        td_error = cumulative_reward - np.dot(ai.weights[action_index], state_feature)
        
        ai.weights[action_index] += ai.alpha * td_error * state_feature

        # print(f"更新前の重み: {ai.weights[action_index]}")
        # print(f"Q値: {np.dot(ai.weights[action_index], state_feature)}")
        # print(f"更新後の重み: {ai.weights[action_index]}")

    # エピソードメモリをリセット
    ai.episode_memory = []





def play_single_episode(ai, cpu1,cpu2,size,loss_history):
   
    board = create_initial_board(size)
    player = -1  # 黒 (-1) から開始
    
    # 初期盤面表示
    # print("初期盤面")
    # OthelloLogic.printBoard(board)

    while True:
        # print(f"現在のプレイヤー: {'黒' if player == -1 else '白'}")
        
        
        # 合法手を取得
        
        # aiが-1(黒●)
        if player == -1:
            moves = OthelloLogic.getMoves(board, player, size)
            
            action = ai.get_action(board, moves)  # 合法手から選択
            # ai.episode_memory.append((board, action, 0))  # 状態,行動,報酬を記録(状態は後でget_featureされるのでここではboardを入れる)

            # passの処理(Q値も計算済み)
            if action == "pass":
                print(f"{'黒' if player == -1 else '白'}がパスしました。\n")
                # 状態,行動,報酬を記録(状態は後でget_featureされるのでここではboardを入れる)
                # intermediate_reward = calculate_intermediate_reward(board, player)
                # ai.episode_memory.append((board, action, intermediate_reward))
                player *= -1  # プレイヤー交代
                continue

            if action not in moves:
                print("合法手ではない手が選択されました。")
                exit()

            # 石を置く("execute"は盤面を更新する)
            board = OthelloLogic.execute(board, action, player, size)
            # intermediate_reward = calculate_intermediate_reward(board, player)
            # ai.episode_memory.append((board, action, intermediate_reward))
            # print(f"{'黒' if player == -1 else '白'}が{action}に置きました。\n")
        


        # 学習相手が1(白〇)
        # Q値の更新処理が必要
        else:
            moves = OthelloLogic.getMoves(board, player, size)

            if not moves:
                print(f"{'黒' if player == -1 else '白'}に合法手がないため、パスします。")
                # aiにも合法手がない場合は終了
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
                            
                        update_weights_func(reward, board, ai,loss_history)
                        # OthelloLogic.printBoard(board)

                        # 最後の手に報酬を与える
                        # ai.episode_memory[-1] = (ai.episode_memory[-1][0], ai.episode_memory[-1][1], reward)
                        # update_weights_monte_carlo(ai)
                        # OthelloLogic.printBoard(board)
                        return result
                   
                
                # 学習相手には合法手がないため、プレイヤー交代
                # これ以降の処理をスキップ
                # 更新処理必須
                reward = calculate_intermediate_reward(board, -player)
                update_weights_func(reward, board, ai,loss_history)
                player *= -1  # プレイヤー交代
                continue
            
            # 合法手がある場合
            
            
            # プレイヤーの手を決定（簡易AIとしてランダム選択）
            # print(f"合法手: {moves}")
            cpus = [cpu1,cpu2]
            action = random.choice(cpus).get_action(board, moves)
            # 合法手から選択
           

            if action not in moves:
                print("合法手ではない手が選択されました。")
                exit()

            # 石を置く("execute"は盤面を更新する)
            board = OthelloLogic.execute(board, action, player, size)
            # print(f"{'黒' if player == -1 else '白'}が{action}に置きました。\n")
            
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
                            
                        update_weights_func(reward, board, ai,loss_history)
                        
                        # ai.episode_memory[-1] = (ai.episode_memory[-1][0], ai.episode_memory[-1][1], reward)
                        # update_weights_monte_carlo(ai)
                        # OthelloLogic.printBoard(board)
                        return result
                    
            
            # 更新処理
            reward = calculate_intermediate_reward(board, -player)
            update_weights_func(reward, board, ai,loss_history)


        # ここから下は共通処理
        # 盤面表示
        # OthelloLogic.printBoard(board)

        # プレイヤー交代
        player *= -1

    # print("ゲーム終了")


    # # 重みの確認
    # print("学習後の重み:")
    # print(ai.weights)
   
def calculate_exponential_temperature(game_num, initial_temp, min_temp, tau):
    """
    温度を指数減少スケジュールで計算
    """
    return min_temp + (initial_temp - min_temp) * math.exp(-game_num / tau)


def main():
    size = 8  # ボードサイズ
    games_to_play = 3000  # 総ゲーム数
    report_interval = 100  # 勝率を報告する間隔
    win_count = 0  # 勝利数カウント
    draw_count = 0  # 引き分け数カウント

    initial_tmp = 1.0  # 初期温度
    min_tmp = 0.08   # 最小温度
    decay_steps = 2500  # 温度が最小値に到達するまでのゲーム数
    tau = 1000  # 温度の減少スケジュールを調整するパラメータ

      # カウント変数
    interval_win_count = 0  # 100ゲーム内の勝利数
    interval_draw_count = 0  # 100ゲーム内の引き分け数
    win_rate = [] #100ゲームごとの勝率を格納するリスト
    loss_history = []  # 損失の履歴
    
    
    ai = OthelloAction.OthelloQLearning()
    naive = OthelloAction.Naive_ai()
    random_ai = OthelloAction.Random_ai()
    max_stone = OthelloAction.Max_stone()
    for game_num in range(1, games_to_play + 1):            
            
            if game_num <= decay_steps:
                # 線形減少スケジュール
                tmp = initial_tmp - (initial_tmp - min_tmp) * (game_num / decay_steps)
                
                
            else:
                # 最小値で固定
                tmp = min_tmp
            ai.temperature = tmp
            # 指数減少スケジュール
            # ai.temperature = calculate_exponential_temperature(game_num, initial_tmp, min_tmp, tau)

            
            result = play_single_episode(ai,max_stone,max_stone,size,loss_history)
            print("ゲーム結果")
            print(result)
            if result == 1:
                interval_win_count += 1
            elif result == 0:
                 interval_draw_count += 1  # ここを追加

            # 100ゲームごとに勝率を計算
            if game_num % report_interval == 0:
                interval_win_rate = interval_win_count / report_interval
                win_rate.append(interval_win_rate)  # リストに追加
          
            
                # カウントをリセット
                interval_win_count = 0
                interval_draw_count = 0

           
            # 指定の間隔で勝率を表示
            if game_num % report_interval == 0:
                print(f"ゲーム数: {game_num}, 勝率: {win_count / game_num:.2%}, 引き分け率: {draw_count / game_num:.2%}")

    weights_array = np.array(ai.weights)

    # 各次元ごとの平均 (全行動での64次元平均)
    dimension_mean = np.mean(weights_array, axis=0)

    # 全体平均 (行動 x 次元すべての平均値)
    overall_mean = np.mean(weights_array)

    print("各次元ごとの平均 (64次元):", dimension_mean)
    print("全体の平均:", overall_mean)

    std_dev = np.std(weights_array)
    print("全体の標準偏差:", std_dev)
    print(ai.temperature)


    # # 勝率のグラフを表示
    # print(win_rate)
    # plt.figure(figsize=(10, 6))
    # plt.plot(range(report_interval, games_to_play + 1, report_interval), win_rate, marker='o', label="win rate")
    # plt.title("win rate")
    # plt.xlabel("games")
    # plt.ylabel("win rate")
    # plt.ylim(0, 1)  # 勝率の範囲を 0〜1 に固定
    # plt.grid()
    # plt.legend()
    # plt.show()

    def moving_average(x, window_size):
        """移動平均を計算"""
        return np.convolve(x, np.ones(window_size) / window_size, mode='valid')

    smoothed_win_rate = moving_average(win_rate, window_size=3)

    # x軸を調整（移動平均の結果に合わせる）
    x_original = range(report_interval, games_to_play + 1, report_interval)
    x_smoothed = x_original[:len(smoothed_win_rate)]

    # グラフのプロット
    print(win_rate)
    plt.figure(figsize=(10, 6))
    plt.plot(x_original, win_rate, marker='o', label="Original Win Rate", alpha=0.5)
    plt.plot(x_smoothed, smoothed_win_rate, marker='o', label="Smoothed Win Rate")
    plt.title("Win Rate (Smoothed)")
    plt.xlabel("Games")
    plt.ylabel("Win Rate")
    plt.ylim(0, 1)
    plt.grid()
    plt.legend()
    plt.show()

    


if __name__ == "__main__":
    main()

