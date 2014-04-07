import thread, TableSocket
from Table import Table
from BiodataConsumer import BiodataConsumer
import thread, sys

if __name__ == "__main__":
	if len(sys.argv) != 2 or sys.argv[1].isdigit() == False:
		print "Usage: TableMain.py [number of players in game]"
		sys.exit()
		
	numplayers = int(sys.argv[1])
	table = Table()
	for i in range(numplayers):
		consumer = BiodataConsumer("0@127.0.0.1", "49992", table, i)
		thread.start_new_thread(consumer.run, ())
	TableSocket.socketListener(table, numplayers)