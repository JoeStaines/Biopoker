import socket, time, cPickle, sys
from Player import Player

def clientSocket():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(('127.0.0.1', 2000))
	
	#remove this: code for getting out of process
	"""
	if ri == 1:
		s.send('end')
		sys.exit()
	else:
		s.send('start')
	"""
		
	s.setblocking(0)
	return s

def getTableData(s):
	#recv
	allData = []
	data = ''
	
	try:
		data = s.recv(4096)
		if data:
			allData.append(data)
	except:
		pass
		
	if allData != []:
		joinData = ''.join(allData)
		state = cPickle.loads(joinData)
		return state
	else:
		return None
		
def sendCommand(s, command):
	try:
		s.sendall(command)
	except:
		print "Failed to send command {0}".format(command)
		
def getAndSendName(s):
	nameSuitable = False
	while not nameSuitable:
		name = raw_input('Your name: ')
		if len(name) > 7:
			print "Name must be 7 characters or less"
		else:
			nameSuitable = True
	
	try:
		s.sendall(name)
	except:
		print "Failed to send name: {0}".format(name)
			
			
def receiveSeat(s):
	seatno = ''
	timeout = 10
	starttime = time.time()
	while not seatno:
		if time.time() - starttime < timeout:
			try:
				seatno = s.recv(4096)
			except:
				pass
		else:
			print "Timeout: couldn't receive seat number. Exiting"
			s.close()
			sys.exit()
	
	# send handshake OK
	try:
		s.sendall('OK')
	except:
		print "Failed sending handshake OK"
		conn.close()
		sys.exit()
			
	return int(seatno)
	
if __name__ == "__main__":
	clientSocket()