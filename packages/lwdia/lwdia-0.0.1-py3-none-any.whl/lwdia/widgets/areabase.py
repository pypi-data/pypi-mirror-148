import importlib
import os
import pickle
import subprocess
import threading
import webbrowser
from functools import partial
from itertools import zip_longest
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


class AreaBase:
    def __init__(self, win, width=None):
        self.win = win
        self.root = self.win.root
        self.width = width or self.win.scr_widthof6
        self.separator = ttk.Separator(self.root, orient=VERTICAL)

    def config(self):
        self.place()
