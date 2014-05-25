#!/usr/bin/env python
import os
import wx
import webbrowser

class MainBox(wx.Frame):
	#MainBox init stuff
	def __init__(self, parent, title):
		super(MainBox,self).__init__(parent, title=title, size=(450,350))
		self.dirpath = os.getcwd() #working directory set to dirpath. no point yet
		self.savepath = os.getcwd()
		self.InitUI()
		self.Centre()
		self.Show()
		
		#html template below
		self.headStart = """
<html>
<!--
COOPER: the Chapter On One Page GenERator
presents
-->
<head>
	<title>
		"""
		self.headEnd = """
	</title>
</head>

<body>
	<center>

"""
		self.srcA = '''
		<img src="'''
	
		self.srcB = '''"><br><br>
'''
	
		self.bodyEnd = """

	</center>	
</body>
</html>	
"""	
	

	
	def InitUI(self):
		#init panels
		pnl1 = wx.Panel(self) #panel for the widgets
		self.infoBar = wx.InfoBar(pnl1) 
		#info bar to show msg when successfully generated ;D
		
		#sizers and widgets and placement
		vbox = wx.BoxSizer(wx.VERTICAL) #one big vertical sizer
		
		vbox.Add(self.infoBar, 0, wx.EXPAND) #add info bar
		
		vbox.Add((-1,70)) #space between hboxes / padding
		
		hbox1 = wx.BoxSizer(wx.HORIZONTAL) #hor sizer for pnl1
		browsebtn = wx.Button(pnl1, label="Browse for source folder...")
		hbox1.Add(browsebtn)
		vbox.Add(hbox1,flag=wx.ALIGN_CENTER)
		
		vbox.Add((-1,5)) #add some space between hboxes
		
		hbox2 = wx.BoxSizer(wx.HORIZONTAL)
		self.printdir = wx.StaticText(pnl1,wx.ID_ANY,label="No directory selected.")
		hbox2.Add(self.printdir)
		vbox.Add(hbox2, flag=wx.ALIGN_CENTER)
		
		vbox.Add((-1,25))
		
		hbox3 = wx.BoxSizer(wx.HORIZONTAL)
		gobtn = wx.Button(pnl1, label="Go!",size=(70,30))
		hbox3.Add(gobtn)
		vbox.Add(hbox3,flag=wx.ALIGN_CENTER)
		
		vbox.Add((-1,20))
		
		pnl1.SetSizer(vbox)
		
		
		#binding button events
		browsebtn.Bind(wx.EVT_BUTTON, self.onDir)
		gobtn.Bind(wx.EVT_BUTTON, self.onGo)
	

	#event handling
		
	def onDir(self,e):
		"""show DirDialog and save & print spec. directory"""
		dlg = wx.DirDialog(self,"Choose a directory:",style=wx.DD_DEFAULT_STYLE | wx.DD_CHANGE_DIR)
		if dlg.ShowModal() == wx.ID_OK:
			self.dirpath = dlg.GetPath()
			
			#get dir name for title later
			self.dirname = os.path.basename(self.dirpath)
			
			#set static text to show chosen dir
			self.printdir.SetLabel(self.dirpath)
		dlg.Destroy()
		
		
	def onGo(self,e):
		"""do the html file writing"""
		# get list of files in dir (and filter by extension)
		self.filenames = [] #all files in dir
		self.imgnames = [] #filter to files w/ img extensions only
		for (root, dirs, files) in os.walk(self.dirpath):
			self.filenames.extend(files)
			break
			
		#only want img files	
		for file in self.filenames:
			if file.lower().endswith(('.png','.jpg','.jpeg','.gif')):
				self.imgnames.append(file)
		
		#sort imgnames
		self.imgnames.sort()

		
		#write the html file
		with open(os.path.join(self.dirpath,"index.html"),'w') as f:
			f.write(self.headStart)
			f.write(self.dirname)
			f.write(self.headEnd)
			#stopped here, add the filename w/ directory list thing and cont
			for img in self.imgnames:
				f.write(self.srcA)
				f.write(img)
				f.write(self.srcB)
			f.write(self.bodyEnd)
		
		#show info bar w/ success msg
		self.infoBar.ShowMessage("HTML file generated successfully!",wx.ICON_INFORMATION)
		
		
		
def main():
	app = wx.App(False)
	MainBox(None, title="COOPer!") # A Frame is a top-level window.
	app.MainLoop()

if __name__ == "__main__":
	main()