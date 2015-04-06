#!/usr/bin/python

# =============================================================================
#     Author: Sarah Boyd
#     Date:   April 5, 2015
#     File:  p.py
#     Description: This is the main file for the Text Analyzer app
# =============================================================================

from __future__ import division
from string import punctuation
import re
import Tkinter as tk
import ttk
from Tkinter import *
from tkFileDialog import *
import tkMessageBox
import stopwords
import csv
import exportcsv
import graph
import tkFont
import webbrowser



#print "Sarahs project now....\n\n"

root = tk.Tk()

#global variables
filename=StringVar()
default_filename = "Please choose the file you would like to analyze->"
filename.set(default_filename)

sorted_count = {}
word_list = []
kwicdict = {}

def center_window(w=300, h=200):
    # get screen width and height
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    # calculate position x, y
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))

#check if word is in the stop word list
def checkStop(word):
	if word in stopwords.stop_list:
		return True
	return False

#open file to analyze
def open_file():
	#print filename.get()

	with open (str(filename.get())) as myfile:
		data = myfile.read().replace('\n','')
	process_file(data)

#process file
def process_file(data):
	data_pro = re.sub(r'[^\w]', ' ',data)
	data_pro = re.sub(' +',' ',data_pro)
	data_pro = data_pro.lower()
	for p in list(punctuation):
		data_pro =data_pro.replace(p,'')
	
	global word_list 
	word_list = data_pro.split(' ')
	count_words(word_list)
	keywords(word_list)

#get context for a certain word
def get_context (word):
	context_list_box.delete(0, END)

	for n in kwicdict[word]:
		outstring = ' '.join(n[:2]).rjust(20)
		outstring += str(n[2]).center(len(n[2])+6)
		outstring += ' '.join(n[3:])
		context_list_box.insert(END, outstring)
		##print outstring

#create keyword dictionary
def keywords (word_list):
	ngrams = [word_list[i:i+5] for i in range(len(word_list)-4)]
	global kwicdict
	kwicdict = {}
	for n in ngrams:
		if n[2] not in kwicdict:
			kwicdict[n[2]] = [n]
		else:
			kwicdict[n[2]].append(n)

#get selected word from wordlist
def get_selection():
	sel = word_list_box.curseselection()
	#print str(sel)

#open file dialog
def get_file():
	sorted_count = {}
	word_list = []
	filename.set(askopenfilename(parent=root)) #make this only text files

#count word frequency
def count_words(word_list):
	word_list_box.delete(0, END)
	count_list_box.delete(0,END)

	word_count = {}
	#print stopwords.stop_list

	for word in word_list:
		if not checkStop(word):
			if word_count.has_key(word):
				word_count[word] = word_count[word] + 1
			else:
				word_count[word] = 1

	global sorted_count
	sorted_count = sorted(word_count.items(),key=lambda x:x[1], reverse=TRUE)

	#print sorted_count

	for word in sorted_count:
		word_list_box.insert(END, word[0])
		count_list_box.insert(END, word[1])

	word_list_box.update_idletasks()
	count_list_box.update_idletasks()

#open stop word dialog
def get_stop_words():
	#stop_fname = askopenfilename(parent=root)
	stop_dialog = stopwords.MyDialog(root)
	root.wait_window(stop_dialog.top)

	open_file()

#function to write to a csv file
def csv_writer (data, path):
	with open (path, "wb") as csv_file:
		writer = csv.writer(csv_file, delimiter = ',')
		writer.writerow(['Word', 'Count'])
		for line in data:
			writer.writerow(line)
#export to a csv file
def export():
	export_dialog = exportcsv.Export(root)
	root.wait_window(export_dialog.top)
	#print "exporting to.." + export_dialog.dirname
	csv_writer(sorted_count, export_dialog.dirname+"/" + export_dialog.saveName+".csv")

#sync scrollbars
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

#live update word selection
def OnSelect(event):
	widget=event.widget
	selection=widget.curselection()
	value = widget.get(selection[0])
	#print "selection:", selection, ": '%s'" %value
	get_context(value)
	segmentList(10,value)

#sz = words in segment
def segmentList(sz,word):
    #newlist = [word_list[i:i+sz] for i in xrange(0, len(word_list), sz)]
    newlist = [ word_list[i::sz] for i in xrange(sz) ]
    #print [seg.count(word) for seg in newlist]
    segGraph.update_graph([seg.count(word) for seg in newlist], word)



center_window(600,600)
root.title("Text Analyzer")
my_font = tkFont.Font(family="Monaco", size=12) 

#menubar
menubar = Menu(root)

#filemenu 
filemenu = Menu(menubar, tearoff=0)
#filemenu.add_command(label="Save")
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
#menubar.add_cascade(label="File", menu=filemenu)

#editmenu
editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Stop Words", command = get_stop_words)
editmenu.add_command(label="Export to CSV", command = export)
menubar.add_cascade(label="Edit", menu=editmenu)

#helpmenu
def open_link():
    webbrowser.open_new(r"https://github.com/sarahboyd/Text-Analyzer/wiki")
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help docs", command=open_link)
menubar.add_cascade(label="Help",menu =helpmenu)



pane=PanedWindow(orient=VERTICAL)
pane.pack(fill=BOTH,expand=1)

mainframe = tk.Frame(pane)
mainframe.pack()

#Getting the file
tk.Label(mainframe, text="File:  ", font = "Verdana 12 bold").pack(side=LEFT)
tk.Label(mainframe, textvariable=filename).pack(side=LEFT)
tk.Button(mainframe, text="choose file", command=get_file).pack(side=LEFT)
tk.Button(mainframe, text="Go!", command=open_file).pack(side=LEFT)

pane.add(mainframe)
bottomframe = PanedWindow(orient=HORIZONTAL)
bottomframe.pack(fill=BOTH, expand=1)

#display_count frame
list_frame = tk.Frame(bottomframe)
title_frame = tk.Frame(list_frame)
title_frame.pack()
list_frame.pack()

Label(title_frame, text="Word", width=7, font = "Verdana 14 bold").grid(row=0, column=0)
Label(title_frame, text="Count", width=12, font = "Verdana 14 bold").grid(row=0, column=1)
scrollbar = Scrollbar(list_frame)

word_list_box = Listbox(list_frame, yscrollcommand = yscroll1, width=13,font=my_font)
word_list_box.bind("<<ListboxSelect>>", OnSelect)
word_list_box.pack(side=LEFT, fill=BOTH)

count_list_box = Listbox(list_frame, yscrollcommand = yscroll2, width=13, font=my_font)
count_list_box.pack(side=LEFT, fill=BOTH)

scrollbar.config(command=yview)
scrollbar.pack( side = RIGHT, fill=Y)


#right side
rightPane = PanedWindow(orient=VERTICAL)
rightPane.pack(fill=BOTH, expand=1)

rightTop = tk.Frame(rightPane)
rightTop.pack()

segGraph = graph.Graph(rightTop)

rightBottom = tk.Frame(rightPane, )
rightBottom.pack()

tk.Label(rightBottom, text="keyword context",font = "Verdana 14 bold").pack()
scrollbar2 = Scrollbar(rightBottom)
context_list_box = Listbox(rightBottom, yscrollcommand = scrollbar2.set, width=53, font=my_font)
context_list_box.pack(side=LEFT, fill=BOTH)
scrollbar2.config(command=context_list_box.yview)
scrollbar2.pack(side=RIGHT, fill=Y)

rightPane.add(rightTop)
rightPane.add(rightBottom)
rightPane.pack()

bottomframe.add(list_frame)
bottomframe.add(rightPane)
bottomframe.pack()
pane.add(bottomframe)

pane.pack()

root.config(menu=menubar)

root.lift()
root.call('wm', 'attributes', '.', '-topmost', True)
root.after_idle(root.call, 'wm', 'attributes', '.', '-topmost', False)
root.mainloop()
