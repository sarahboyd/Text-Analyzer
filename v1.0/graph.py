# =============================================================================
#     Author: Sarah Boyd
#     Date:   April 5, 2015
#     File:  grpah.py
#     Description: This creates the segment graph
# =============================================================================

import Tkinter as tk
import ttk
from Tkinter import *

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure




class Graph:

	def update_graph(self, seg_list,word):
		self.a.clear()
		self.a.plot([1,2,3,4,5,6,7,8,9,10],seg_list)
		self.a.set_title(word)
		self.a.set_ylim(0,max(seg_list)+25)
		self.canvas.draw()

	def __init__ (self, parent):
		f = Figure(figsize=(3,3), dpi=100)
		self.a = f.add_subplot(111)
		self.a.set_title('word distribution')
		self.a.set_ylabel("word count")
		self.a.set_xlabel("segment")
		self.a.set_ylim(0,100)
		self.a.set_xlim(0,10)

		# for item in ([self.a.title, self.a.xaxis.label, self.a.yaxis.label]):
		# 	item.set_fontsize(8)
		#self.a.plot([1,2,3,4,5,6,7,8,9,10],[0,0,0,0,0,0,0,0,0,0])

		self.canvas = FigureCanvasTkAgg(f, parent)
		self.canvas.show()
		self.canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)
		self.canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)
