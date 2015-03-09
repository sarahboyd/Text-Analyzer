import Tkinter as tk
import ttk
from Tkinter import *
from tkFileDialog import *
from string import punctuation
import re


stop_list = []




class MyDialog:

	def check_list(self, word):
		if word in stop_list:
			return True
		return False

	def get_stop_words(self):
		self.word_list_box.delete(0,END)
		for word in stop_list:
			self.word_list_box.insert(END, word)
		self.word_list_box.update_idletasks()

	def open_file(self):
		stopfile = askopenfilename()	
		with open (stopfile) as myfile:
			data = myfile.read()
		
		word_list = data.split('\n')

		for word in word_list:
			if not self.check_list(word):
				stop_list.append(word)

		self.get_stop_words()

	def add_word(self):
		new_word =self.stop_entry.get()
		if not self.check_list(new_word):
			stop_list.append(new_word)
		self.get_stop_words()
		self.stop_entry.delete(0,END)

	def __init__ (self, parent):
		top = self.top = tk.Toplevel(parent)
		self.testLabel = tk.Label(top, text="testing this")
		self.testLabel.pack()

		top.title("Stop Words")

		#box size
		w=400
		h=220
		# get screen width and height
		ws = top.winfo_screenwidth()
		hs = top.winfo_screenheight()
		# calculate position x, y
		x = (ws/2) - (w/2)
		y = (hs/2) - (h/2)
		top.geometry('%dx%d+%d+%d' % (w, h, x, y))

		pane=PanedWindow(top, orient=HORIZONTAL)
		pane.pack(fill=BOTH,expand=1)

		leftFrame = Frame(pane)
		leftFrame.pack()

		#list current stop words
		Label(leftFrame, text="Current stop words:").pack()
		list_frame = ttk.Frame(leftFrame)
		list_frame.pack()

		scrollbar = Scrollbar(list_frame)
		self.word_list_box = Listbox(list_frame, yscrollcommand = scrollbar.set, width=12)
		self.word_list_box.pack(side=LEFT, fill=BOTH)
		self.get_stop_words()

		#options to add more
		rightFrame = Frame(pane)
		rightFrame

		Label(rightFrame, text="Import more words:").grid(row=0)
		Button(rightFrame, text="Import", command=self.open_file).grid(row=0, column=1)
		Label(rightFrame, text="Add stop word:").grid(row=1)
		self.stop_entry = Entry(rightFrame)
		self.stop_entry.grid(row=2, column=0)
		Button(rightFrame, text="Add", command=self.add_word).grid(row=2, column=1)


		pane.add(leftFrame)
		pane.add(rightFrame)
		pane.pack()


	def send(self):
		self.top.destroy

	
