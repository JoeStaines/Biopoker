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
		
	def recvInfo(self, timeout):
		allData = None
		data = ''
		length = None
		
		beginTime = time.time()
		while time.time() - beginTime < timeout:
			try:
				data = self.socket.recv(4096)
			except:
				pass
			
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
		
	def sendInfo(self, data):
		try:
			lengthPrefix = str(len(data)).encode('utf-8') + ':#:'
			payload = lengthPrefix + data
			self.socket.sendall(payload)
		except socket.error:
			raise
			
		
	def getTableData(self):
		#recv
		self.allTableData = None
		self.tableData = ''
		self.dataLength = None
		
		try:
			self.tableData = self.socket.recv(4096)
		except:
			pass
			
		if self.tableData != '' and self.allTableData == None:
			lengthStr, sep, payload = self.tableData.partition(':#:')
			self.dataLength = int(lengthStr)
			self.allTableData = payload
			self.tableData = ''
		elif self.tableData != '' and self.allTableData != None:
			self.allTableData += self.tableData
			self.tableData = ''
			
		if self.dataLength != None:
			if len(self.allTableData) == self.dataLength:
				state = cPickle.loads(self.allTableData)
				self.allTableData = None
				self.tableData = ''
				self.dataLength = None
				return state
		
		# Data is not altogether yet: return None
		return None
			
	def sendCommand(self, command):
		try:
			self.sendInfo(command)
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
		try:
			self.sendInfo(name)
		except socket.error:
			print 'Could not send name'
			self.socket.close()
			sys.exit()
				
	def receiveSeat(self):

		try:
			seatno = self.recvInfo(10)
		except socket.timeout:
			print "Timeout: receiving seat number"
			self.socket.close()
			sys.exit()
		
		# send handshake OK
		try:
			self.sendInfo('OK')
		except socket.error:
			print "Could not send handshake"
			self.socket.close()
			sys.exit()
			
		return int(seatno)
		
#if __name__ == "__main__":
#		clientSocket()