import socket, sys, time

def socketListener():
	serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serversock.bind(('127.0.0.1', 2000))
	serversock.listen(1)
	while 1:
		conn, addr = serversock.accept()
		delay = 1
		begin = time.time()
		while 1:
			if time.time() - begin > delay:
				conn.send("Hello!")
				begin = time.time()
		
		
if __name__ == "__main__":
	socketListener()