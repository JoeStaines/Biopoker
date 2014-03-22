import socket, time, cPickle, sys
from Player import Player

class UISocket():
	def __init__(self):
		self.socket = self.clientSocket()
		self.timeout = 10

	def clientSocket(self):
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
		
	def recvInfo(self, errorID):
		allData = None
		data = ''
		length = None
		
		beginTime = time.time()
		while time.time() - beginTime < self.timeout:
			try:
				data = self.socket.recv(4096)
			except:
				pass
			
			if data != '' and allData == None:
				lengthStr, sep, payload = data.partition(':#:')
				print lengthStr
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
		print "Timeout: could not receive data through socket"
		print "Error Identifier: {0}".format(errorID)
		self.socket.close()
		sys.exit()
		
	def sendInfo(self, data, errorID):
		try:
			lengthPrefix = str(len(data)).encode('utf-8') + ':#:'
			payload = lengthPrefix + data
			self.socket.sendall(payload)
		except:
			print "Error: could not send data"
			print "Error Identifier: {0}".format(errorID)
			self.socket.close()
			sys.exit()
			
		
	def getTableData(self):
		#recv
		allData = []
		data = ''
		
		try:
			data = self.socket.recv(4096)
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
			
	def sendCommand(self, command):
		try:
			self.socket.sendall(command)
		except:
			print "Failed to send command {0}".format(command)
			
	def getAndSendName(self):
		nameSuitable = False
		while not nameSuitable:
			name = raw_input('Your name: ')
			if len(name) > 7:
				print "Name must be 7 characters or less"
			else:
				nameSuitable = True
		
		self.sendInfo(name, 'Send Name')
				
				
	def receiveSeat(self):
		"""
		seatno = ''
		timeout = 10
		starttime = time.time()
		while not seatno:
			if time.time() - starttime < timeout:
				try:
					seatno = self.socket.recv(4096)
				except:
					pass
			else:
				print "Timeout: couldn't receive seat number. Exiting"
				self.socket.close()
				sys.exit()
		"""
		
		seatno = self.recvInfo('Receive Seat Number')
		
		# send handshake OK
		self.sendInfo('OK', 'Handshake')
				
		return int(seatno)
		
#if __name__ == "__main__":
#		clientSocket()