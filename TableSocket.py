import socket, sys, time, cPickle, thread, copy
from Player import Player

stateData = {}

def socketListener(table, numplayers):
	serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serversock.bind(('127.0.0.1', 2000))
	serversock.listen(1)
	while 1:
		conn, addr = serversock.accept()
		try:
			namedata = recvInfo(conn, 5)
		except:
			print "Timeout: couldn't receive name"
			conn.close()
			sys.exit()
		seatNum = table.addPlayer(Player(namedata, 1000))
		if len(table.getPlayers()) == numplayers:
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
		conn.setblocking(0)
		sendSeatNumber(conn, seatNum)
		
		thread.start_new_thread(receiveCommand, (conn, table,seatNum))
		thread.start_new_thread(sendStateData, (conn, table,seatNum))
		
				
def receiveCommand(conn, table, seat):
	cmddata = ''
	
	while 1:				
		try:
			cmddata = recvInfo(conn, 1800)
		except socket.timeout:
			print "Timeout: didn't receive any command in 30 minutes"
			conn.close()
			sys.exit()
			
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
			
			
def sendStateData(conn, table, seat):
	delay = 0.5
	begin = time.time()
	table.setState()
	
	while 1:
		if time.time() - begin > delay:
			stateData = copy.deepcopy(table.stateDict)
			if stateData != {}:
				removeOtherPlayersCards(seat, stateData['playerlist'])
			pickleState = cPickle.dumps(stateData)
			try:
				sendInfo(conn, pickleState)
			except:
				if table.playerList[seat] != None:
					table.playerRemoveList.append(table.playerList[seat])
					print table.playerRemoveList
					break
				else:
					print 'already deleted'
					print table.playerRemoveList
					break
					
			begin = time.time()
		else:
			time.sleep(0.1)
	
def recvInfo(conn, timeout):
	allData = None
	data = ''
	length = None
	
	beginTime = time.time()
	while time.time() - beginTime < timeout:
		try:
			data = conn.recv(4096)
		except:
			time.sleep(0.1)
		
		if data != '' and allData == None:
			lengthStr, sep, payload = data.partition(':#:')
			length = int(lengthStr)
			allData = payload
			data = ''
		elif data != '' and allData != None:
			allData += data
			data = ''
			
		if length != None:
			if len(allData) == length:
				return allData
			
			
	#exceed timeout: exit
	raise socket.timeout
	
def sendInfo(conn, data):
	try:
		lengthPrefix = str(len(data)).encode('utf-8') + ':#:'
		payload = lengthPrefix + data
		conn.sendall(payload)
	except socket.error:
		raise
	
def sendSeatNumber(conn, seat):
	# send seat number
	seatStr = str(seat).encode('utf-8')
	try:
		sendInfo(conn, seatStr)
	except socket.error:
		print "Error: could not send seat number"
		conn.close()
		sys.exit()
	
	# wait for handshake
	try:
		handshake = recvInfo(conn, 10)
	except socket.timeout:
		print "Timeout: could not receive handshake"
		conn.close()
		sys.exit()
			
	if handshake == 'OK':
		return
	else:
		print "Handshake not ok. Received: {0}".format(handshake)
		conn.close()
		sys.exit()
		
def removeOtherPlayersCards(seat, playerlist):
	for i, x in enumerate(playerlist):
		if i != seat and x != None:
			x.hand = [52, 52]