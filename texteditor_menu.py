import os
import wx

""" to do:
- implement save/save as functions
- find out how to update gui to disable 'save' OR lead save to saveas
- implement other features.. incl. calculations, tabs, syntax, font and color change
"""

class MainWindow(wx.Frame):
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title=title, size=(200,100))
		self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
		self.CreateStatusBar() # A StatusBar in the bottom of the window

		# Setting up the menu.
		filemenu= wx.Menu()
		helpmenu= wx.Menu()

		# wx.ID_ABOUT and wx.ID_EXIT are standard ids provided by wxWidgets.
		
		# explicitly defining menu item Save for practice/future ref
		menuSave = wx.MenuItem(filemenu, wx.ID_SAVE, "&Save"," Save current file")
		
		# implicit define the rest of menu items
		menuOpen = filemenu.Append(wx.ID_OPEN, "&Open..."," Open a file from your computer")
		#menuSave = filemenu.Append(wx.ID_SAVE, "&Save"," Save current file")
		menuSaveAs = filemenu.Append(wx.ID_SAVEAS,"Save &As...","Save current file as...")
		menuAbout = filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
		menuExit = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")
		
		
		
		# Creating the menubar.
		menuBar = wx.MenuBar()
		menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
		menuBar.Append(helpmenu,"&Help") # Adding the "helpmenu" to the MenuBar
		self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

		# Set events.
		self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
		self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
		self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
		self.Bind(wx.EVT_MENU, self.OnSave, menuSave)
		self.Bind(wx.EVT_MENU, self.OnSaveAs, menuSaveAs)
		
		self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateSave, menuSave)
		
		self.Show(True)
		

	def OnAbout(self,e):
		# A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
		with open("about.txt") as f:
			msg = f.read()
		dlg = wx.MessageDialog( self, msg, "About ediate", wx.OK)
		dlg.ShowModal() # Show it
		dlg.Destroy() # finally destroy it when finished.

	def OnExit(self,e):
		self.Close(True)  # Close the frame.
		
	def OnNew(self,e):
		# TO DO: implement new (tab?)
		self.enablecheck = 0 #don't yet know where to Save
	
	def OnOpen(self,e):
		""" Open a file"""
		self.dirname = ''
		dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
		if dlg.ShowModal() == wx.ID_OK:
			self.filename = dlg.GetFilename()
			self.dirname = dlg.GetDirectory()
			f = open(os.path.join(self.dirname, self.filename), 'r')
			self.control.SetValue(f.read())
			f.close()
		dlg.Destroy()
		self.enablecheck = 1 #enable Save menu item
	
	def OnSave(self,e):
		""" Save file """
		f = open(os.path.join(self.dirname,self.filename), 'w')
		f.write(self.control.GetValue())
		f.close()
		
	def OnSaveAs(self,e):
		#TO DO: implement SaveAs
		
		self.enablecheck = 1 #enable faster direct Save
		
	def OnUpdateSave(self,e):
		e.Enable(self.enablecheck)
	
		
app = wx.App(False)
frame = MainWindow(None, "ediate")
app.MainLoop()