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

	def select_update_file(self):
		self.updatefilename.set(askopenfilename(title="Select file to update"))
		self.updatedVar.set("Hit save to update file")
		

	def update_file(self):
		with open (self.updatefilename.get()) as myfile:
			data = myfile.read()

		file_list = data.split('\n')
		new_list = stop_list

		for word in file_list:
			if not self.check_list(word):
				new_list.append(word)

		fileUpdate = open(self.updatefilename.get(), 'w')
		for word in new_list:
			fileUpdate.write('\n'+word)

		self.updatedVar.set("File has been updated")



	def __init__ (self, parent):
		top = self.top = tk.Toplevel(parent)

		top.title("Stop Words")

		self.updatefilename =StringVar()
		self.updatedVar = StringVar()
		self.updatefilename.set("")

		#box size
		w=500
		h=200
		# get screen width and height
		ws = top.winfo_screenwidth()
		hs = top.winfo_screenheight()
		# calculate position x, y
		x = (ws/2) - (w/2)
		y = (hs/2) - (h/2)
		top.geometry('%dx%d+%d+%d' % (w, h, x, y))

		pane=PanedWindow(top, orient=HORIZONTAL)

		frame = Frame(pane, relief=RAISED, borderwidth = 1)
		frame.pack(fill=BOTH, expand=1)

		pane.pack(fill=BOTH, expand=1)

		closeButton = Button(pane, text="Close", command=top.destroy)
		closeButton.pack(side=RIGHT, padx=5, pady=5)

		pane2 = PanedWindow(pane, orient=HORIZONTAL)

		leftFrame = Frame(frame)
		leftFrame.pack(side=LEFT)

		#list current stop words
		Button(leftFrame, text="Import file", command=self.open_file).pack()
		Label(leftFrame, text="Stop words in use:").pack()
		list_frame = ttk.Frame(leftFrame)
		list_frame.pack()

		scrollbar = Scrollbar(list_frame)
		self.word_list_box = Listbox(list_frame, yscrollcommand = scrollbar.set, width=12, height=5)
		scrollbar.config(command=self.word_list_box.yview)
		scrollbar.pack(side=RIGHT, fill=Y)
		self.word_list_box.pack(side=LEFT, fill=BOTH)
		self.get_stop_words()

		#options to add more
		rightFrame = Frame(frame)
		rightFrame.pack(side=LEFT, fill=BOTH)

		self.stop_entry = Entry(rightFrame)
		self.stop_entry.grid(row=1, column=0)
		Button(rightFrame, text="Add Word", command=self.add_word).grid(row=1, column=1)

		#Label(rightFrame, textvariable=self.updatefilename).grid(row=4,column=0)
		Label(rightFrame, text="Select file to save to").grid(row=2,column=0)
		Button(rightFrame, text="Select File", command=self.select_update_file).grid(row=2,column=1)
		Button(rightFrame, text="Save list", command=self.update_file).grid(row=3, column=1)
		Label(rightFrame, textvariable=self.updatedVar).grid(row=3)


	def send(self):
		self.top.destroy

	
