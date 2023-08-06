import importlib
import os
import pickle
import subprocess
import threading
import webbrowser
from functools import partial
from itertools import zip_longest
from lwdia.locale import _
from tkinter import *
from tkinter import ttk
import tkinter as tk
from lwdia.widgets.widgetarea import WidgetArea
from lwdia.widgets.combinationarea import CombinationArea
from lwdia.widgets.presentationarea import PresentationArea


class MainWindow:
    def __init__(self):
        self.root = Tk()
        self.scr_width = self.root.winfo_screenwidth()
        self.scr_height = self.root.winfo_screenheight()
        self.scr_widthof2 = int(self.scr_width / 2)
        self.scr_widthof6 = int(self.scr_width / 6)
        self.scr_heightof2 = int(self.scr_height / 2)
        self.canvas = tk.Canvas(self.root)
        self.widgetarea = WidgetArea(self)
        self.combinationarea = CombinationArea(self)
        self.presentationarea = PresentationArea(self)

    def get_w_width(self, of=1):
        return int(self.root.winfo_width() / of)

    def get_w_height(self, of=1):
        return int(self.root.winfo_height() / of)

    def set_root(self):
        self.root.bind("<Configure>", self.root_configure)

    def set_title(self, title=None):
        self.root.title(title or _("lwdia"))

    def set_geometry(self, geo=None):
        self.root.geometry(geo or f"{self.scr_widthof2}x{self.scr_heightof2}")

    def root_configure(self, *args):
        self.canvas.config(
            width=self.get_w_width(), height=self.get_w_height()
        )
        self.widgetarea.config()
        self.combinationarea.config()
        self.presentationarea.config()

    def mainloop(self):
        self.set_title()
        self.set_geometry()
        self.set_root()
        self.widgetarea.place()
        self.combinationarea.place()
        self.presentationarea.place()
        self.root.mainloop()
