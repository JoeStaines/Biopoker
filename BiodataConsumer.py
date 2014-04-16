from Vicarious.Consumers.Consumer import Consumer
import sys,time
from collections import deque

class BiodataConsumer():

	def __init__(self, host, port, table, player):
		self.consumer = Consumer(host,int(port), self)
		self.table = table
		self.player = player
		
		self.MAX_QUEUE_SIZE = 1000
		
		self.biodataValuesHigh = deque([], self.MAX_QUEUE_SIZE)
		self.biodataValuesLow = deque([], self.MAX_QUEUE_SIZE)
		self.biodataAvgHigh = 0
		self.biodataAvgLow = 0
		
		self.highPeak = 0
		self.lowPeak = 0
		
	def run(self):
		while(True):
			self.consumer.waitData()
			data = self.consumer.getData()
			if data != None:
				self.addBiodata(float(data))
				
	def addBiodata(self, data):
		if data > 0:
			if data > self.highPeak:
				self.highPeak = data
		
			if len(self.biodataValuesHigh) > (self.MAX_QUEUE_SIZE - 10) and data > self.biodataAvgHigh * 2:
				print "DETECTHED HIGH THRESHOLD"
			
			self.biodataValuesHigh.append(data)
			self.biodataAvgHigh = sum(self.biodataValuesHigh) / len(self.biodataValuesHigh)
		else:
			if data < self.lowPeak:
				self.lowPeak = data
		
			if len(self.biodataValuesLow) > (self.MAX_QUEUE_SIZE - 10) and data < self.biodataAvgLow * 2:
				print "DETECTED LOW THRESHOLD"
			
			self.biodataValuesLow.append(data)
			self.biodataAvgLow = sum(self.biodataValuesLow) / len(self.biodataValuesLow)
				
		print "High len = {0} || Low len = {1}".format(len(self.biodataValuesHigh), len(self.biodataValuesLow))
		print "High avg = {0} || Low avg = {1}".format(self.biodataAvgHigh, self.biodataAvgLow)
		print "High peak = {0} || Low peak = {1}\n".format(self.highPeak, self.lowPeak)
			
def main(host,port):
	chart = BiodataConsumer(host,port)
	chart.run()
	
if __name__ == '__main__': main(sys.argv[1],int(sys.argv[2]))
    