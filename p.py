#!/usr/bin/python

from __future__ import division
from string import punctuation
import re
import Tkinter
import ttk
from Tkinter import *
from tkFileDialog import *
import tkMessageBox
import stopwords

print "Sarahs project now....\n\n"

root = Tkinter.Tk()

filename=StringVar()
default_filename = "Please choose the file you would like to analyze->"
filename.set(default_filename)

sorted_count = {}
word_list = []

def checkStop(word):
	if word in stopwords.stop_list:
		return True
	return False

def open_file():
	print filename.get()

	with open (str(filename.get())) as myfile:
		data = myfile.read().replace('\n','')
	process_file(data)

def process_file(data):
	data_pro = re.sub(r'[^\w]', ' ',data)
	data_pro = re.sub(' +',' ',data_pro)
	data_pro = data_pro.lower()
	for p in list(punctuation):
		data_pro =data_pro.replace(p,'')
	
	word_list = data_pro.split(' ')
	count_words(word_list)

def count_words(word_list):
	word_list_box.delete(0, END)
	count_list_box.delete(0,END)

	word_count = {}
	print stopwords.stop_list

	for word in word_list:
		if not checkStop(word):
			if word_count.has_key(word):
				word_count[word] = word_count[word] + 1
			else:
				word_count[word] = 1

	sorted_count = sorted(word_count.items(),key=lambda x:x[1], reverse=TRUE)

	print sorted_count

	for word in sorted_count:
		word_list_box.insert(END, word[0])
		count_list_box.insert(END, word[1])

	word_list_box.update_idletasks()
	count_list_box.update_idletasks()

def get_stop_words():
	#stop_fname = askopenfilename(parent=root)
	stop_dialog = stopwords.MyDialog(root)
	root.wait_window(stop_dialog.top)
	
	if str(filename.get()) is  str(default_filename):
		print "here"
	else:
		open_file()



def center_window(w=300, h=200):
    # get screen width and height
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    # calculate position x, y
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))

def get_file():
	sorted_count = {}
	word_list = []
	filename.set(askopenfilename(parent=root)) #make this only text files

def yscroll1( *args ):
	if count_list_box.yview() != word_list_box.yview():
		count_list_box.yview_moveto(args[0])
	scrollbar.set(*args)

def yscroll2( *args ):
	if word_list_box.yview() != count_list_box.yview():
		word_list_box.yview_moveto(args[0])
	scrollbar.set(*args)

def yview(*args):
	word_list_box.yview(*args)
	count_list_box.yview(*args)

center_window(600,300)
root.title("Title goes here")

#menubar
menubar = Menu(root)

#filemenu 
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Save")
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

#editmenu
editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Stop Words", command = get_stop_words)
menubar.add_cascade(label="Edit", menu=editmenu)

#helpmenu
helpmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help",menu =helpmenu)


pane=PanedWindow(orient=VERTICAL)
pane.pack(fill=BOTH,expand=1)

mainframe = ttk.Frame(pane)
mainframe.pack()

#Getting the file
ttk.Label(mainframe, text="File:  ").pack(side=LEFT)
ttk.Label(mainframe, textvariable=filename).pack(side=LEFT)
ttk.Button(mainframe, text="choose file", command=get_file).pack(side=LEFT)
ttk.Button(mainframe, text="Go!", command=open_file).pack(side=LEFT)

pane.add(mainframe)

bottomframe = PanedWindow(orient=HORIZONTAL)
bottomframe.pack(fill=BOTH, expand=1)

#display_count frame
list_frame = ttk.Frame(bottomframe)
list_frame.pack()

scrollbar = Scrollbar(list_frame)

word_list_box = Listbox(list_frame, yscrollcommand = yscroll1, width=12)

word_list_box.pack(side=LEFT, fill=BOTH)

count_list_box = Listbox(list_frame, yscrollcommand = yscroll2, width=8)
count_list_box.pack(side=LEFT, fill=BOTH)

scrollbar.config(command=yview)
scrollbar.pack( side = RIGHT, fill=Y)


#right side
rightframe = ttk.Frame(bottomframe)
rightframe.pack()

ttk.Label(rightframe, text="testing").pack()

bottomframe.add(list_frame)
bottomframe.add(rightframe)
bottomframe.pack()
pane.add(bottomframe)

pane.pack()

root.config(menu=menubar)
root.mainloop()
