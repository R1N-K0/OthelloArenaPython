import random
import numpy as np

"""
引数について

board:現在の盤面の状態
moves:現在の合法手の一覧

詳しい説明はサイトのHomeページをご覧ください。

"""

def getAction(board,moves):
	if not moves:
		return "pass"
	#渡されたMovesの中からランダムで返り値として返却する。
	index = random.randrange(len(moves))
	print("ボードの状態")
	print(board)

	# board_bp = np.array(board)
	# board_flatten = board_bp.flatten()
	# print("ボードの状態(1次元)")
	# print(board_flatten)

	print("合法手の一覧")
	print(moves)
	
	# test_index = 26
	# adjust_index = test_index - sum(1 for i in [27, 28, 35, 36] if i < test_index)
	# print("例えば(7,7)に打つ場合のインデックス")
	# print(adjust_index)

	return moves[index]

class OthelloQLearning:
	def __init__(self, feature_dim =64, action_dim = 61, alpha = 0.1, gamma = 0.9, initial_temperature=1.0, min_temperature=0.1, decay_rate=0.99):
		self.feature_dim = feature_dim
		self.action_dim = action_dim
		self.alpha = alpha
		self.gamma = gamma
		self.temperature = initial_temperature  # 初期温度
		self.min_temperature = min_temperature  # 最小温度
		self.decay_rate = decay_rate  # 温度減衰率

		# 重みの初期化(61個の行動の重みを64次元の特徴量で表現)
		self.weights = np.random.uniform(-0.1, 0.1, (self.action_dim, self.feature_dim))

		# 前回の状態と行動
		self.current_feature = None
		self.current_action = None
		self.current_q = None
	
	def get_feature(self, board):
		#盤面から特徴量を取得
		# 64次元の特徴量を返す

		# 1次元に変換
		board_np = np.array(board, dtype = np.float64)
		feature = board_np.flatten()

		# 正規化(値の類似性を保つため)
		norm = np.linalg.norm(feature)
		if norm != 0:
			feature /= float(norm)

		return feature
	
	def calc_action_index(self, action):
		# Q値の計算(渡された行動のQ値を計算する)
		# 行動のインデックスを取得(盤面の左上から右下にかけて0~63)
		# 27, 28, 35, 36は初期位置なので除外(初期位置を過ぎるごとに1だけずれる)
		# passの時は-1を返す(一番後ろのインデックス)
		if action == "pass":
			return -1
		else:

			action_index = (action[0] + action[1] * 8)
			adjusted_index = action_index - sum(1 for i in [27, 28, 35, 36] if i < action_index)
			return adjusted_index
	
	def calc_q(self, board_feature, action):
		
		# Q値の計算(渡された行動のQ値を計算する)
		adjusted_index = self.calc_action_index(action)
		q_value = np.dot(self.weights[adjusted_index], board_feature)
		
		return q_value
	
	def select_action(self, board_feature, moves):
		#  """ボルツマン選択で行動を選択"""
		
		if not moves:
			return "pass"
		
		# Q値の計算
		q_values = []
		for action in moves:
			q_values.append(self.calc_q(board_feature, action))
		
		# ボルツマン選択の確率分布を計算
		q_values = np.array(q_values)
		exp_q_values = np.exp(q_values / self.temperature)
		probability = exp_q_values / np.sum(exp_q_values)

		# 行動を選択(確率分布に従って行動を選択)
		action = np.random.choice(moves, p=probability)

		# 温度を下げる
		self.temperature = max(self.min_temperature, self.temperature * self.decay_rate)

		return action
		

		# if np.random.rand() < self.epsilon:
		# 	# ランダムに行動を選択
		# 	action = random.choice(moves)
			
		# else:
		# 	# Q値が最大となる行動を選択
		# 	q_values = [self.calc_q(board_feature, action) for action in moves]
		# 	# 最大のQ値を持つ行動を選択(argmaxは最大のインデックスを返す-> 行動ごとにQ値を計算しているので、インデックスが行動そのもの)
		# 	action = moves[np.argmax(q_values)]

		# return action
	

	def get_action(self, board, moves):
		# 盤面から特徴量を取得
		board_feature = self.get_feature(board)

		# 行動を選択
		if not moves :
			action = "pass"
		else:
			action = self.select_action(board_feature, moves)

		# 状態の更新
		self.current_feature = board_feature
		self.current_action = action
		self.current_q = self.calc_q(board_feature, action)

		return action
	

	def get_reward(self, is_game_over, is_winner):
		# 報酬の計算
		if is_game_over:
			if is_winner:
				reward = 1
			else:
				reward = -1
		else:
			reward = 0
		return reward
	
	def update_weights(self, reward, next_board_feature, next_moves):
		# 重みの更新
		# next_board, next_movesは次の"自分"の盤面と合法手

		# もし次の行動がない場合はpassを選択(passのQを計算)
		if not next_moves:
			action = "pass"
			next_max_q = self.calc_q(next_board_feature, action)

		# 次の行動がある場合は最大のQ値を計算
		else:
			next_q_values = [self.calc_q(next_board_feature, next_action) for next_action in next_moves]
			next_max_q = np.max(next_q_values)

		
		td_error = reward + self.gamma * next_max_q - self.current_q
		adjusted_index = self.calc_action_index(self.current_action)

		print(f"報酬: {reward}, 次状態の最大Q値: {next_max_q}, 現在のQ値: {self.current_q}, TD誤差: {td_error}")

		print("更新前の重み")
		print(f"weight{adjusted_index}")
		print(self.weights[adjusted_index])

		# 重みの更新
		self.weights[adjusted_index] += self.alpha * td_error * self.current_feature

		print("更新後の重み")
		print(f"weight{adjusted_index}")
		print(self.weights[adjusted_index])

	
	



		

		