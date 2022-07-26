from tkinter import *

class MyLeftPanel:
	def __init__(self, root, frame):
		self.root = root
		self.frame = frame

		#Left Frame and its contents

		Label(self.frame, text="Instructions:").grid(row=0, column=0, padx=10, pady=2)


		self.instruct = Label(self.frame, text="1\n2\n2\n3\n4\n5\n6\n7\n8\n9\n")
		self.instruct.grid(row=1, column=0, padx=10, pady=2)

		try:
		    self.imageEx = PhotoImage(file = 'image.gif')
		    Label(self.frame, image=self.imageEx).grid(row=2, column=0, padx=10, pady=2)
		except:
		    print("Image not found")