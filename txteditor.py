import os
import wx

""" COMPLETED:
- implement save/save as functions
-DONE find out how to update gui to disable 'save' 
- // split this below IGNOREFORNOWimplement other features.. incl. calculations, tabs, syntax, font and color change
-DONE move About -> Help

TO DO LIST!
--- next on list -> font change, bg color change
- toggle word wrap
- add docs, html window.
--- which also means writing said docs
--- which means more features first, to have things to write abt
- enable copy and paste features. 
- implement searching
- and printing
- display paths to a few recently opened files? mb five of em
- shortcuts, for saving, new, etc. (eg ctrl+s)
- change About to add more info with AboutBox/AboutDialogInfo
"""

class MainWindow(wx.Frame):
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title=title, size=(400,450))
		self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
		self.CreateStatusBar() # A StatusBar in the bottom of the window

		# Setting up the menu.
		filemenu= wx.Menu()
		helpmenu= wx.Menu()
		setmenu = wx.Menu() # settings menu, if you're confused

		# wx.ID_ABOUT and wx.ID_EXIT are standard ids provided by wxWidgets.
		
		# explicitly defining menu item Save for practice/future ref
		menuSave = wx.MenuItem(filemenu, wx.ID_SAVE, "&Save\t\tCtrl+S"," Save current file")
		# appending to filemenu below
		# & implicit define the rest of menu items
		menuOpen = filemenu.Append(wx.ID_OPEN, "&Open...\t\tCtrl+O"," Open a file from your computer")
		#menuSave = filemenu.Append(wx.ID_SAVE, "&Save"," Save current file")
		filemenu.AppendItem(menuSave)
		menuSaveAs = filemenu.Append(wx.ID_SAVEAS,"Save &As...","Save current file as...")
		filemenu.AppendSeparator()
		menuExit = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")
		
		
		# append to Helpmenu
		menuAbout = helpmenu.Append(wx.ID_ABOUT, "&About"," Information about this program")		
		
		# append to Setmenu
		menuWrap = wx.MenuItem(setmenu, wx.ID_ANY, "Word &Wrap", " Toggle word wrap")
		setmenu.AppendItem(menuWrap)
		
		# Creating the menubar.
		menuBar = wx.MenuBar()
		menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
		menuBar.Append(filemenu,"&Settings") # Adding the "setmenu" to the MenuBar		
		menuBar.Append(helpmenu,"&Help") # Adding the "helpmenu" to the MenuBar
		self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

		# Set events.
		self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
		self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
		self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
		self.Bind(wx.EVT_MENU, self.OnSave, menuSave)
		self.Bind(wx.EVT_MENU, self.OnSaveAs, menuSaveAs)
		self.Bind(wx.EVT_MENU, self.OnWrap, menuWrap)
		
		# events requiring updates in UI
		self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateSave, menuSave)
		self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateWrap, menuWrap)
		
		self.Show(True)
		

	def SetTitle(self,e):
		""" set title of program at the top"""
		#MainWindow.SetTitle overrides wx.Frame.SetTitle, super instead
		super(MainWindow,self).SetTitle("%s - edicate" %self.filename)
		
	def OnAbout(self,e):
		# A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
		with open("about.txt") as f:
			msg = f.read()
		dlg = wx.MessageDialog( self, msg, "About edicate", wx.OK)
		dlg.ShowModal() # Show it
		dlg.Destroy() # finally destroy it when finished.

	def OnExit(self,e):
		self.Close(True)  # Close the frame.
		
	def OnNew(self,e):
		# TO DO: implement new (tab?)
		pass
	
	def OnOpen(self,e):
		""" Open a file"""
		self.dirname = ''
		dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.FD_OPEN)
		if dlg.ShowModal() == wx.ID_OK:
			self.filename = dlg.GetFilename()
			self.dirname = dlg.GetDirectory()
			self.SetTitle(e) # set title w/ filename
			f = open(os.path.join(self.dirname, self.filename), 'r')
			self.control.SetValue(f.read())
			f.close()
		dlg.Destroy()

	
	def OnSave(self,e):
		""" Save file """
		f = open(os.path.join(self.dirname,self.filename), 'w')
		f.write(self.control.GetValue())
		f.close()
		self.SetTitle(e)
		
	def OnSaveAs(self,e):
		""" Save file as... calling OnSave when path is set"""
		self.dirname = ''
		dlg = wx.FileDialog(self, "Save as...", self.dirname, "", \
		"Text files (*.txt)|*.txt", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
		if dlg.ShowModal() == wx.ID_OK:
			self.filename = dlg.GetFilename()
			self.dirname = dlg.GetDirectory()
			self.OnSave(e)
		
	
	def OnWrap(self,e):
		""" toggle word wrap"""
		pass
	
	# def of methods for updating UI
	def OnUpdateSave(self,e):
		""" grey out Save for new files, where save path
		unspecified, and also when document hasn't been
		modified"""
		# TO DO: Check for textctrl having been modified or not
		# to prevent mindless saving
		enablecheck = hasattr(self, 'filename')
		e.Enable(enablecheck)
		
	def OnUpdateWrap(self,e):
		""" check mark for menu item Wrap toggle"""
		pass
	
		
app = wx.App(False)
frame = MainWindow(None, "edicate")
app.MainLoop()
print "Thanks for using edicate. I hope it was adequate."