from tkinter import *
from MyLeftPanel import *
from MyRightPanel import *

class MyTkWindow:
	def __init__(self):

		self.root = Tk() #Makes the window
		self.root.wm_title("Window Title") #Makes the title that will appear in the top left
		self.root.config(background = "#FFFFFF")

		self.leftFrame = Frame(self.root, width=200, height = 600)
		self.leftFrame.grid(row=0, column=0, padx=10, pady=2)

		self.rightFrame = Frame(self.root, width=200, height = 300)
		self.rightFrame.grid(row=0, column=1, padx=10, pady=2)

		self.leftPanel = MyLeftPanel(self.root, self.leftFrame)
		self.rightPanel = MyRightPanel(self.root, self.rightFrame)

	def start(self):
		self.root.mainloop() #start monitoring and updating the GUI