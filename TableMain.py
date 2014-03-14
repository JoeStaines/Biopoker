import thread, TableSocket
from Table import Table

if __name__ == "__main__":
	table = Table()
	TableSocket.socketListener(table)