import socket, sys, time, cPickle
from Player import Player

stateData = {}

def socketListener():
	serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serversock.bind(('127.0.0.1', 2000))
	serversock.listen(1)
	while 1:
		conn, addr = serversock.accept()
		delay = 1
		begin = time.time()
		while 1:
			if time.time() - begin > delay:
				pickleState = cPickle.dumps(stateData)
				sendret = conn.sendall(pickleState)
				print sendret
				begin = time.time()
		
		
if __name__ == "__main__":
	playerList = []
	for _ in range(6):
		playerList.append(Player())
	
	stateData = {	'playerlist': playerList[:], \
					'comcards': [0, 0, 0, 0, 0], \
					'pots':	[200, 30, 10], \
					'curbet':	[100, 30, 10], \
					'turn':		0 }
	
	socketListener()