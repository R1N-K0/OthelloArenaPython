import random
import copy
import OthelloLogic

"""
引数について

board:現在の盤面の状態
moves:現在の合法手の一覧

詳しい説明はサイトのHomeページをご覧ください。

"""

def getAction(board,moves):
	print("現在の盤面")
	print(board)

	print("自分が石を置ける場所のリスト")
	print(moves)

	#渡されたMovesの中からランダムで返り値として返却する。
	index = random.randrange(len(moves))
	next_move = moves[index]

	print("次に石を置く予定の場所")
	print(next_move)

	# next_moveに石を置いた場合の次の盤面を取得する
	# OthelloLogic.executeの第1引数は現在の盤面、第2引数はこれから石を置く場所、
	# 第3引数は石を置く人が自分のAIなら1で、対戦相手なら-1に設定、
	# 第4引数は盤面の大きさで8×8なら8を設定
	next_board = OthelloLogic.execute(copy.deepcopy(board),next_move,1,8)

	print("次の盤面")
	print(next_board)

	# 次の盤面で対戦相手が石を置くことができる場所のリスト
	# OthelloLogic.getMovesの第1引数は盤面、第２引数は対戦相手なら-1、自分なら1
	# 第3引数は盤面の大きさで8×8なら8を設定
	opponents_moves = OthelloLogic.getMoves(next_board,-1,8)

	print("対戦相手が次に石を置く予定の場所")
	print(opponents_moves)

	return next_move