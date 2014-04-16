import thread, TableSocket
from Table import Table
import threading, sys

if __name__ == "__main__":
	if len(sys.argv) != 2 or sys.argv[1].isdigit() == False:
		print "Usage: TableMain.py [number of players in game]"
		sys.exit()
		
	numplayers = int(sys.argv[1])
	table = Table()
	TableSocket.socketListener(table, numplayers)