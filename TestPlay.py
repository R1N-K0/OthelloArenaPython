import OthelloAction
import OthelloLogic
from OthelloAction import OthelloQLearning

#sizeを変更することでテストプレイする盤面の大きさを変更できます。
#size = 4
#size = 6
size = 8
board = [[0 for i in range(size)] for j in range(size)]

board[int(size/2)-1][int(size/2)-1] = 1;
board[int(size/2)][int(size/2)-1]=-1;
board[int(size/2)-1][int(size/2)]=-1;
board[int(size/2)][int(size/2)]=1;

ai = OthelloQLearning()

player =-1
moves = OthelloLogic.getMoves(board,player,size)
while(True):
	n = input()
	if(player == -1):
		board_reversed = OthelloLogic.getReverseboard(board)
		action = OthelloAction.getAction(board_reversed,moves)
	else:
		action = OthelloAction.getAction(board,moves)
		# 相手が打ったとして更新処理をする
	
	
	if(not (action in moves)):
		print(board)
		print('合法手ではない手が打たれました' + action)
		exit()
	board = OthelloLogic.execute(board,action,player,size)
	OthelloLogic.printBoard(board)

	# moves=次のプレイヤーの合法手
	moves = OthelloLogic.getMoves(board,player*-1,size)
	if(len(moves) == 0):
		# 次のプレイヤーが打つ手がない場合(next_next_movesは次の次のプレイヤーの合法手)
		next_next_moves = OthelloLogic.getMoves(board,player,size)
		if not next_next_moves:
			break
		
		# もし次のプレイやが自分の場合で打つ手がない場合はそのままpass対応しているため、何もしない
		elif (player*-1 == -1):
			player = player * -1
		# 相手をスキップ
		else:
			moves = next_next_moves
			player = player
	
	# 次のプレイヤーに交代
	else:
		player = player * -1

		

print('正常に終了しました。')		
