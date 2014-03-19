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
		namedata = ''
		while not namedata:
			try:
				namedata = conn.recv(4096)
			except:
				pass
		seatNum = table.addPlayer(Player(namedata, 1000))
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
	delay = 0.5
	begin = time.time()
	cmddata = ''
	conn.setblocking(0)
	while 1:
		if time.time() - begin > delay:
			stateData = table.stateDict
			pickleState = cPickle.dumps(stateData)
			try:
				sendret = conn.sendall(pickleState)
			except:
				if table.playerList[seat] != None:
					table.playerRemoveList.append(table.playerList[seat])
					print table.playerRemoveList
					break
				else:
					print 'already deleted'
					print table.playerRemoveList
					break
				
			try:
				cmddata = conn.recv(4096)
			except:
				pass
				
			if cmddata != '':
				if seat == table.turn:
					left, _, right = cmddata.partition(':')
					if left == 'call':
						table.call(table.playerList[seat])
					elif left == 'raise':
						table.raiseBet(table.playerList[seat], int(right))
					elif left ==  'fold':
						table.fold(table.playerList[seat])
				cmddata = ''
				
			begin = time.time()