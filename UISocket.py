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
			
	
if __name__ == "__main__":
	clientSocket()