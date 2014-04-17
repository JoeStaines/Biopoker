from Vicarious.Consumers.Consumer import Consumer
import sys,time
from collections import deque

class BaselineConsumer():

	def __init__(self, host, port, minBox, maxBox):
		self.consumer = Consumer(host,int(port), self)
		self.minBox = minBox
		self.maxBox = maxBox
		
		self.continueRunning = False
		self.max = 0
		self.min = 0
		
		
	def run(self):
		while(self.continueRunning):
			self.consumer.waitData()
			data = self.consumer.getData()
			if data != None:
				fltData = float(data)
				if fltData > self.max:
					self.max = fltData
					self.maxBox.SetValue(data)
				elif fltData < self.min:
					self.min = fltData
					self.minBox.SetValue(data)
			
def main(host,port):
	chart = BiodataConsumer(host,port)
	chart.run()
	
if __name__ == '__main__': main(sys.argv[1],int(sys.argv[2]))
    