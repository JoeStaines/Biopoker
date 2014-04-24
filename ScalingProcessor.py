from Vicarious.Processors.Processor import Processor

class ScalingProcessor(Processor):
	"""
	A scaling processor used with Vicarious
	
	It has a GUI where you can start baselining for min and max data values and then to stop baselining. This 
	processor will scale all of the data values coming in to the range of -1 to 1. This is determined from the 
	min and max values from baselining
	"""
	def __init__(self):
		Processor.__init__(self, "ScalingProcessor", [("source", "source data to be scaled")], [("Scaled data")], [], self.InitUI)
		self.oldmin = 0
		self.oldmax = 0
		self.newmin = -1.0
		self.newmax = 1.0
		self.isBaselineRunning = False
		self.hasBaselineEnded = False
		self.run()
		
	def process(self,timeStamp,values,queueNo):
		"""
		Overwritten function of the ``Processor`` class. Deals with incoming data values on the port chosen 
		calls :func:`testMinMax` if the baselining is still running or calls :func:`scale` if the baselining 
		has ended. Finally makes a call to `addProcessedValues` to send the data through to the outport
		"""
		datain = values[0]
		curValue = float(datain)
		if self.isBaselineRunning:
			self.testMinMax(curValue)
		
		if self.hasBaselineEnded:
			scaledValue = self.scale(curValue)
			#print scaledValue
			self.addProcessedValues(scaledValue)
		
	def testMinMax(self, value):
		"""
		Determines if the ``value`` coming in has a larger value that the current max or a smaller value 
		than the current min. If it does, it updates the min/max accordingly and updates the value in the gui
		"""
		if value > self.oldmax:
			self.oldmax = value
			self.maxBox.SetValue(str(value).encode('utf-8'))
		elif value < self.oldmin:
			self.oldmin = value
			self.minBox.SetValue(str(value).encode('utf-8'))
		
	def scale(self, value):
		"""
		Algorithm to scale/normalize the value between a specific range
		"""
		oldscale = self.oldmax - self.oldmin
		newscale = self.newmax - self.newmin
		return (newscale * (value - self.oldmin) / oldscale) + self.newmin
		
	def InitUI(self, frame):
		"""
		Defines the GUI of the scaling processor
		"""
		import wx
		frame.SetSize((200,200))
		
		panel = wx.Panel(frame)
		
		vbox = wx.BoxSizer(wx.VERTICAL)
		
		hbox1 = wx.BoxSizer(wx.HORIZONTAL)
		startButton = wx.Button(panel, label='Start Baselining', size=(170, 25))
		hbox1.Add(startButton)
		vbox.Add(hbox1, flag=wx.LEFT | wx.RIGHT | wx.ALIGN_CENTRE, border=5)
		
		vbox.Add((-1, 5))
		
		hbox2 = wx.BoxSizer(wx.HORIZONTAL)
		stopButton = wx.Button(panel, label='Stop Baselining', size=(170, 25))
		hbox2.Add(stopButton)
		vbox.Add(hbox2, flag=wx.LEFT | wx.RIGHT | wx.ALIGN_CENTRE, border=5)
		
		vbox.Add((-1, 10))
		
		hbox3 = wx.BoxSizer(wx.HORIZONTAL)
		self.onOffText = wx.StaticText(panel, label='Off')
		hbox3.Add(self.onOffText)
		vbox.Add(hbox3, flag=wx.LEFT | wx.RIGHT | wx.ALIGN_CENTRE, border=5)
		
		vbox.Add((-1, 20))
		
		hbox4 = wx.BoxSizer(wx.HORIZONTAL)
		minText = wx.StaticText(panel, label='Min', style=wx.ALIGN_CENTRE)
		maxText = wx.StaticText(panel, label='Max', style=wx.ALIGN_CENTRE)
		hbox4.Add(minText, -1)
		hbox4.Add(maxText, -1)
		vbox.Add(hbox4, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=5)
		
		vbox.Add((-1, 5))
		
		hbox5 = wx.BoxSizer(wx.HORIZONTAL)
		self.minBox = wx.TextCtrl(panel, style=wx.TE_READONLY)
		self.maxBox = wx.TextCtrl(panel, style=wx.TE_READONLY)
		self.minBox.SetBackgroundColour((210,210,210))
		self.maxBox.SetBackgroundColour((210,210,210))
		hbox5.Add(self.minBox, -1, wx.EXPAND)
		hbox5.Add(self.maxBox, -1, wx.EXPAND)
		vbox.Add(hbox5, flag=wx.LEFT | wx.RIGHT | wx.EXPAND, border=5)
		
		panel.SetSizer(vbox)
		
		# Bind items
		frame.Bind(wx.EVT_BUTTON, self.OnStartPress, id=startButton.GetId())
		frame.Bind(wx.EVT_BUTTON, self.OnStopPress, id=stopButton.GetId())
		
	def OnStartPress(self, event):
		"""
		Bind event process for the GUI when the user presses the start button. Sets the gui label to 'on' and 
		tells the object that the baselining is running
		"""
		self.onOffText.SetLabel('On')
		self.isBaselineRunning = True
		
	def OnStopPress(self, event):
		"""
		Bind event for the stop button. Sets the gui label to 'off' and tells the object that the baselining has ended
		"""
		self.onOffText.SetLabel('Off')
		self.isBaselineRunning = False
		self.hasBaselineEnded = True
		
if __name__ == "__main__": ScalingProcessor()