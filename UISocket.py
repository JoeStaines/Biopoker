import socket, time, cPickle, sys
from Player import Player

class UISocket():
	def __init__(self):
		self.socket = self.clientSocket()
		self.timeout = 10
		
		
		self.gameState = {}

	def clientSocket(self):
		"""
		Creates a client socket that connects to a server socket. Will as for through command line 
		what the server host is
		"""
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
		"""
		Code that wraps around ``socket.recv``. Will set the timeout of the socket to whatever is specified in 
		``timeout``.
		
		This function has some protection from the standard ``socket.recv`` function, as it is agreed between UISocket.py and TableSocket.py an agreed delimiter that is prefixed to the message to determine the length of 
		the message being sent. Using that length, it then goes round in a loop until it has enough characters in
		the buffer to collect all of the message and return it
		"""
		self.socket.settimeout(timeout)
		allData = None
		buffer = ''
		length = None
		while True:
			try:
				buffer += self.socket.recv(4096)
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
		"""
		Sends info through the socket while prefixing the length of the message plus the agreed upon delimiter 
		defined in UISocket.py and TableSocket.py
		"""
		try:
			lengthPrefix = str(len(data)).encode('utf-8') + ':#:'
			payload = lengthPrefix + data
			self.socket.sendall(payload)
		except socket.error:
			raise
			
		
	def recvTableData(self):
		"""
		Similar in essence to the function :func:`recvInfo`, but because this is used to get the table state data, 
		it needs to run in a continuous loop and cannot return like :func:`recvInfo`. Because of this, it deals with
		the logic of working with the received message internally and delivers the output to an instance variable that 
		is read by the UI class
		"""
		
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
		"""
		Sends the command (call, fold raise) through the socket
		"""
		try:
			self.sendInfo(command)
		except:
			print "Failed to send command {0}".format(command)
			
	def getAndSendName(self):
		"""
		Gets the name of the player through command line interaction and sends it through the socket
		"""
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
		"""
		Receive the seat number of this specific client. Used to update client specific data in the UI
		"""

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