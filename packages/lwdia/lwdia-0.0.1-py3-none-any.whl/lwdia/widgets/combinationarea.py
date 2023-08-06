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
from lwdia.widgets.areabase import AreaBase


class CombinationArea(AreaBase):
    def __init__(self, win, width=None):
        super().__init__(win, width)

    def place(self):
        self.separator.place(
            x=2 * self.win.get_w_width(of=3), y=0, relwidth=0.2, relheight=1
        )
