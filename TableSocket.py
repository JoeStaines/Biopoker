import socket, sys, time, cPickle, thread
from Player import Player

stateData = {}

def socketListener(table=None):
	serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serversock.bind(('127.0.0.1', 2000))
	serversock.listen(1)
	while 1:
		conn, addr = serversock.accept()
		print "player connected"
		seatNum = table.addPlayer(Player("Player", 1000))
		if len(table.getPlayers()) > 1:
			table.beginRound()
		
		# remove this: code for getting out of process
		"""
		data = ''
		while not data:
			try:
				data = conn.recv(4096)
			except:
				pass
		if data == 'end':
			sys.exit()
		"""
		
		thread.start_new_thread(socketThread, (conn, table,seatNum))
		
				
def socketThread(conn, table, seat):
	delay = 1
	begin = time.time()
	while 1:
		if time.time() - begin > delay:
			stateData = table.stateDict
			pickleState = cPickle.dumps(stateData)
			try:
				sendret = conn.sendall(pickleState)
			except:
				table.playerRemoveList.append(table.playerList[seat])
				print table.playerRemoveList
				break
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