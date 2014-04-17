import wx, threading
from BaselineConsumer import BaselineConsumer

class BaselineUI(wx.Frame):
	def __init__(self, parent, title):
		super(BaselineUI, self).__init__(parent, title=title, size=(200,200))
		self.InitUI()
		self.consumer = BaselineConsumer('127.0.0.1', 50006, self.minBox, self.maxBox)
		
		self.Centre()
		self.Show()
		
	def InitUI(self):
		panel = wx.Panel(self)
		
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
		self.Bind(wx.EVT_BUTTON, self.OnStartPress, id=startButton.GetId())
		self.Bind(wx.EVT_BUTTON, self.OnStopPress, id=stopButton.GetId())
		
	def OnStartPress(self, event):
		self.onOffText.SetLabel('On')
		self.consumer.continueRunning = True
		threading.Thread(target=self.consumer.run).start()
		
	def OnStopPress(self, event):
		self.onOffText.SetLabel('Off')
		self.consumer.continueRunning = False

		
if __name__ == "__main__":
	app = wx.App()
	frame = BaselineUI(None, 'Baseline')
	app.MainLoop()