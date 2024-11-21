import requests
import json
import OthelloAction
import AuthCheck
import OthelloLogic
import numpy as np
import random
import copy
import os
import OthelloAction

base_url = "http://tdu-othello.com/api/"
headers = AuthCheck.auth_check(base_url)

r = requests.post(base_url + "where", headers=headers)

if(r.status_code == 422):
	message = r.json()
	print(message['message'])
	exit()
if(r.status_code != requests.codes.ok):
	print('エラーが発生しました。')
	exit()

data = r.json()
roomid = data['id']
player = data['player']
board = []
payload = {}

count_num = 0

ai = OthelloAction.OthelloQLearning()
ai.temperature = 0.08
ai.load_weights()
count_num+= 1
print(count_num)
print("AIの重みを読み込みました。")
print("ai.temperature:{}".format(ai.temperature))
print("ai.weights:{}".format(ai.weights))

if(player == 1):
    payload = {'player':player}
    r = requests.post(base_url + "wait_for_player/" + roomid, data=payload,headers=headers)
    data = r.json()
    OthelloLogic.printBoard(json.loads(data['board']))
    board = json.loads(data['board'])
    moves = json.loads(data['moves'])
else:
    OthelloLogic.printBoard(json.loads(data['board']))
    rev_board = json.loads(data['board'])
    board = json.loads(data['board'])
    for x in range(len(rev_board)):
        for y in range(len(rev_board)):
            board[x][y] = rev_board[x][y] * -1
    moves = json.loads(data['moves'])

print(f"重み{ai.weights}")
action = json.dumps(ai.get_learned_action(board,moves))
payload = {'action' : action,'player':player}

while(True):
    print("打った場所は" + action)
    r = requests.post(base_url + "room/" + roomid, data=payload,headers=headers)
    if(r.status_code == 401):
        print('認証エラーが起きました。')
        exit()
    if(r.status_code != requests.codes.ok):
	    print('エラーが発生しました。')
	    exit()
    data = r.json()
    if(data['finish_flag']):
    	print('処理が終了しました。')
    	exit()

    OthelloLogic.printBoard(json.loads(data['board']))
    if(player == -1):
    	rev_board = json.loads(data['board'])
    	board = json.loads(data['board'])
    	for x in range(len(rev_board)):
            for y in range(len(rev_board)):
                board[x][y] = rev_board[x][y] * -1
    else:
    	board = json.loads(data['board'])

    moves = json.loads(data['moves'])
    print(f"重み{ai.weights}")
    action = json.dumps(ai.get_learned_action(board,moves))
    payload = {'action' : action,'player':player}

