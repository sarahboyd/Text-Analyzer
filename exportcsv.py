import Tkinter as tk
import ttk
from Tkinter import *
from tkFileDialog import *
import tkMessageBox

class Export: 

	def pick_location(self):

		if not self.name_entry.get():
			tkMessageBox.showerror("Error", "Please enter a file name!")
		else:
			self.saveName = self.name_entry.get()
			self.dirname = askdirectory(title = 'Please select a directory')	

	def __init__ (self, parent):
		top = self.top = tk.Toplevel(parent)
		top.title("Export to CSV")

		self.dirname = ""
		self.save_name = ""

		#box size
		w=200
		h=100
		# get screen width and height
		ws = top.winfo_screenwidth()
		hs = top.winfo_screenheight()
		# calculate position x, y
		x = (ws/2) - (w/2)
		y = (hs/2) - (h/2)
		top.geometry('%dx%d+%d+%d' % (w, h, x, y))

		pane = PanedWindow(top, orient=VERTICAL)
		pane.pack(fill=BOTH, expand=1)

		top_frame = Frame(pane)
		top_frame.pack()

		Label(top_frame, text="Export as:").pack(side=LEFT)
		self.name_entry = Entry(top_frame, width=10)
		self.name_entry.pack(side=LEFT)

		bottom_frame = Frame(pane)
		bottom_frame.pack()

		Button(bottom_frame, text="Choose location", command=self.pick_location).pack()
		#Button(bottom_frame, text="Export", command=self.export_list).pack()
		Button(bottom_frame, text="Export", command=top.destroy).pack()

		pane.pack()

		def send(self):
			self.top.destroy