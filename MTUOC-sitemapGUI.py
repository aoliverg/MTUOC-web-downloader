#    MTUOC-sitemapGUI
#    Copyright (C) 2023  Antoni Oliver
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

from usp.tree import sitemap_tree_for_homepage
import requests
import codecs
import sys

import requests

from bs4 import BeautifulSoup

from tkinter import *
from tkinter.ttk import *

import tkinter 

from urllib.parse import urlparse


import importlib  
sitemap = importlib.import_module("MTUOC-sitemap")

def go():
    URL=E1.get().strip()
    domain = urlparse(URL).netloc
    suffix=domain.replace(".","_")
    outfile="sitemap-"+suffix+".txt"
    sitemap.get_sitemap(URL, outfile)


top = Tk()
top.title("MTUOC-sitemapGUI")

L1=tkinter.Label(top, text = str("URL:")).grid(row=0,column=0)
E1 = tkinter.Entry(top, bd = 5, width=40, justify="left")
E1.grid(row=0,column=1)

B4=tkinter.Button(top, text = str("Get sitemap!"), borderwidth = 1, command=go,width=14).grid(sticky="W",row=5,column=0)

top.mainloop()
