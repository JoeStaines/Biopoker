from Vicarious.Consumers.Consumer import Consumer
import sys,time
from collections import deque

class BiodataConsumer():

	def __init__(self, host, port, table, player):
		self.consumer = Consumer(host,int(port), self)
		self.table = table
		self.player = player
		
		self.peaksPerMin = deque([], 1000)
		self.lastValue = None
		
	def run(self):
		"""
		Thread run method. Waits on data to come in and then once received, sends it to :func:`processData`
		"""
		while(True):
			self.consumer.waitData()
			data = self.consumer.getData()
			if data != None:
				self.processData(float(data))
				
	def processData(self, value):	
		"""
		Evaluates the peaks per min based on the ``value`` and sends both the (possibly) new peaks per min value 
		and the ``value`` through to the ``Player`` object
		"""
		if value == 0.0 and self.lastValue > 0.0: #reached a peak, add to list
			self.peaksPerMin.append(time.time())
			
		# Prune any peaks > 60 secs
		if len(self.peaksPerMin) > 0:
			if time.time() - self.peaksPerMin[0] >= 60.0:
				self.peaksPerMin.popleft()
				
		self.player.threshValue = value
		self.player.peaksPerMin = len(self.peaksPerMin)
		self.lastValue = value
			
def main(host,port):
	chart = BiodataConsumer(host,port)
	chart.run()
	
if __name__ == '__main__': main(sys.argv[1],int(sys.argv[2]))
    