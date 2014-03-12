import socket, time

def clientSocket():
	s = socket.socket(socket.AF_INET, socket. SOCK_STREAM)
	s.connect(('127.0.0.1', 2000))
	s.setblocking(0)
	
	#recv
	while 1:
		allData = []
		data = ''
		begin = time.time()
		
		while time.time() - begin < 1:
			try:
				data = s.recv(4096)
				if data:
					allData.append(data)
			except:
				time.sleep(0.1)
			
		begin = time.time()
		print data
	
if __name__ == "__main__":
	clientSocket()