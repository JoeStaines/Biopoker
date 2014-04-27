import socket, sys, time, cPickle, threading, copy, os
from Player import Player
from BiodataConsumer import BiodataConsumer

stateData = {}

def socketListener(table, numplayers):
	"""
	Sets up the socket to listen in on a certain port. After a client has connected, it passes some messages
	back and forth between the client to pass some data such as receiving the player name and sending the 
	player seat.
	
	After that, hands over the connection socket to 2 separate threads: :func:`receiveCommand` and :func:`sendStateData`.
	It then listens in for another client connection
	"""
	serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	port = 50050
	
	hostanswer = raw_input("Do you want to run on locahost (for testing) [y/n]: ")
	if hostanswer == 'y' or hostanswer == 'Y':
		host = "127.0.0.1"
	elif hostanswer == 'n' or hostanswer == 'N':
		host = socket.gethostbyname(socket.gethostname())
	else:
		print "'y' or 'n' only"
		sys.exit()
		
	sameportans = raw_input("All players use the same biodata port? (for testing) [y/n]: ")
	if sameportans == 'y' or sameportans == 'Y':
		isSamePort = True
	elif sameportans == 'n' or sameportans == 'N':
		print "in ans"
		isSamePort = False
	else:
		print "'y' or 'n' only"
		sys.exit()
		
	print "IP Address of server {0}".format(host)
	#serversock.bind((socket.gethostbyname(socket.gethostname()), 20000))
	serversock.bind(("127.0.0.1", 20000))
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
			threading.Thread(target=writeStatsToCSV, args=(table,)).start()
		
		consumer = BiodataConsumer("127.0.0.1", port, table, table.playerList[seatNum])
		if not isSamePort:
			port += 1
			
		threading.Thread(target=consumer.run).start()
		
		sendSeatNumber(conn, seatNum)
		
		threading.Thread(target=receiveCommand, args=(conn,table,seatNum)).start()
		threading.Thread(target=sendStateData, args=(conn, table, seatNum)).start()
		
				
def receiveCommand(conn, table, seat):
	"""
	Runs in a threaded constant loop to catch any commands (call, raise, fold) that the client sends and 
	pass the command onto the ``Table`` object so that it can process and update the game state
	"""
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
	"""
	Constantly sends the state data from the ``Table`` object through the socket to the client, so that the 
	client can update it's visualisation
	"""
	delay = 0.1
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
			except socket.error as msg:
				print msg
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
			time.sleep(0.05)
			
def writeStatsToCSV(table):
	"""
	Writes various data about the game state to a csv file
	"""
	#pathname = "C:\\Users\\Joe\\Desktop\\test\\" + time.strftime("%b %dth [%H][%M][%S]", time.localtime()) + ".csv"
	pathname = os.path.abspath(".\\data") + "\\" + time.strftime("%b %dth [%H][%M][%S]", time.localtime()) + ".csv"
	players = table.getPlayers()
	while True:
		p1ppm = players[0].peaksPerMin
		p2ppm = players[1].peaksPerMin
		pot = sum(table.pots)
		if len(table.potwinQ) > 0:
			event = table.potwinQ.popleft()
		else:
			event = "NULL"
		
		if len(table.allinQ) > 0:
			allin = table.allinQ.popleft()
		else:
			allin = "NULL"
			
		with open(pathname, 'a+') as f:
			f.write(str(p1ppm) + "," + 
				str(p2ppm) + "," + 
				str(table.roundNo) + "," + 
				str(pot) + "," +
				event + "," +
				allin +
				"\n")
		time.sleep(1)
	
def recvInfo(conn, timeout):
	"""
	Code that wraps around ``socket.recv``. Will set the timeout of the socket to whatever is specified in 
	``timeout``.
	
	This function has some protection from the standard ``socket.recv`` function, as it is agreed between UISocket.py and TableSocket.py an agreed delimiter that is prefixed to the message to determine the length of 
	the message being sent. Using that length, it then goes round in a loop until it has enough characters in
	the buffer to collect all of the message and return it
	"""
	conn.settimeout(timeout)
	allData = None
	buffer = ''
	length = None
	while True:
		try:
			buffer += conn.recv(4096)
		except:
			raise
		
		if length == None:
			if ":#:" in buffer:
				lengthStr, sep, buffer = buffer.partition(':#:')
				length = int(lengthStr)
		
		if len(buffer) >= length:
			allData = buffer[:length]
			buffer = buffer[length:]
			return allData
	
def sendInfo(conn, data):
	"""
	Sends info through the socket while prefixing the length of the message plus the agreed upon delimiter 
	defined in UISocket.py and TableSocket.py
	"""
	try:
		lengthPrefix = str(len(data)).encode('utf-8') + ':#:'
		payload = lengthPrefix + data
		conn.sendall(payload)
	except socket.error:
		raise
	
def sendSeatNumber(conn, seat):
	"""
	Sends the seat number through to the client
	"""
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
	"""
	Using the ``seat`` number, it removes all of the other player's cards so that the client can only
	see their cards. The rest will just be the back of the card
	"""
	for i, x in enumerate(playerlist):
		if i != seat and x != None:
			x.hand = [52, 52]