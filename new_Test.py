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
        n = input()
        
        # 合法手を取得
        
        # aiが-1(黒●)
        if player == -1:
            moves = OthelloLogic.getMoves(board, player, size)
            if not moves:
                print(f"{'黒' if player == -1 else '白'}に合法手がないため、パスします。")
                
                # 相手にも合法手がない場合は終了
                opponent_moves = OthelloLogic.getMoves(board, -player, size)
                if not opponent_moves:
                    print("両者に合法手がないため、ゲーム終了")
                    break
                
                # 自分には合法手がないため、プレイヤー交代
                player *= -1  # プレイヤー交代
                # これ以降の処理をスキップ
                continue

            print(f"合法手: {moves}")
            action = OthelloAction.getAction(board, moves)  # 合法手から選択

            if action not in moves:
                print("合法手ではない手が選択されました。")
                exit()
        
        # 学習相手が1(白〇)
        else:
            moves = OthelloLogic.getMoves(board, player, size)

            if not moves:
                print(f"{'黒' if player == -1 else '白'}に合法手がないため、パスします。")
                # 相手にも合法手がない場合は終了
                opponent_moves = OthelloLogic.getMoves(board, -player, size)
                if not opponent_moves:
                    print("両者に合法手がないため、ゲーム終了")
                    break
                
                # 自分には合法手がないため、プレイヤー交代
                # これ以降の処理をスキップ
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

        # 盤面表示
        OthelloLogic.printBoard(board)

        # プレイヤー交代
        player *= -1

    print("ゲーム終了")
    OthelloLogic.printBoard(board)

if __name__ == "__main__":
    main()
