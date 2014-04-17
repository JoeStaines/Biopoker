import socket, time, cPickle, sys
from Player import Player

class UISocket():
	def __init__(self):
		self.socket = self.clientSocket()
		self.timeout = 10
		
		
		self.gameState = {}

	def clientSocket(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		ipaddr = raw_input("IP Address of server: ")
		if ipaddr == '':
			ipaddr = '127.0.0.1'
			
		s.connect((ipaddr, 20000))
		
		#remove this: code for getting out of process
		"""
		if ri == 1:
			s.send('end')
			sys.exit()
		else:
			s.send('start')
		"""
		s.settimeout(5)
		return s
		
	def recvInfo(self, timeout):
		self.socket.settimeout(timeout)
		allData = None
		buffer = ''
		length = None
		while True:
			try:
				buffer = self.socket.recv(4096)
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
		
	def sendInfo(self, data):
		try:
			lengthPrefix = str(len(data)).encode('utf-8') + ':#:'
			payload = lengthPrefix + data
			self.socket.sendall(payload)
		except socket.error:
			raise
			
		
	def recvTableData(self):
		
		buffer = ''
		dataLength = None
		stillAlive = True
		
		while stillAlive:
		
			try:
				buffer += self.socket.recv(4096)
			except socket.error as msg:
				self.socket.close()
				stillAlive = False
				break
				
			if dataLength == None:
				if ":#:" in buffer:
					lengthStr, sep, buffer = buffer.partition(':#:')
					dataLength = int(lengthStr)
			
			if len(buffer) >= dataLength:
				pickleState = buffer[:dataLength]
				buffer = buffer[dataLength:]
				self.gameState = cPickle.loads(pickleState)
				dataLength = None
					
				
			
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