from Vicarious.Consumers.Consumer import Consumer
import sys,time

class BiodataConsumer():

    def __init__(self, host, port, table, seatNo):
        self.consumer = Consumer(host,int(port), self)
        self.table = table
        self.seatNo = seatNo

    def run(self):
        while(True):
            self.consumer.waitData()
            data = self.consumer.getData()
            if data != None:
				if self.table.playerList[self.seatNo] != None:
					self.table.playerList[self.seatNo].GSRData = data
            
            
def main(host,port):
    chart = BiodataConsumer(host,port)
    chart.run()
    
if __name__ == '__main__': main(sys.argv[1],int(sys.argv[2]))
    