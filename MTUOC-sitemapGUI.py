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

def searchGoogle(query):

    headers = {
        'User-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }

    params = {
      'q': 'site :'+query,
    }
    links=[]
    html = requests.get('https://www.google.com/search', headers=headers, params=params)
    soup = BeautifulSoup(html.text, 'lxml')

    for result in soup.select('.tF2Cxc'):
      #title = result.select_one('.DKV0Md').text
        link = result.select_one('.yuRUbf a')['href']
      #print(title, link, sep='\n')
        links.append(link)
    return(links)


def go():
    URL=E1.get().strip()
    if not URL.startswith("http"): URL="http://"+URL
    
    '''
    if not args.filename==None:
        outfile=args.filename
    elif not args.prefix==None:
        domain = urlparse(URL).netloc
        suffix=domain.replace(".","_")
        outfile=args.prefix+"-"+suffix+".txt"
    else:
    '''
    domain = urlparse(URL).netloc
    suffix=domain.replace(".","_")
    outfile="sitemap-"+suffix+".txt"

    response = requests.get(URL)

    if response.status_code == 200:
        #print('Web site exists')
        URL=response.url
    else:
        #print('Web site does not exist') 
        sys.exit()

    sortida=codecs.open(outfile,"w",encoding="utf-8")

    tree = sitemap_tree_for_homepage(URL)
    cont=0
    control=[]
    for page in tree.all_pages():
        URL=page.url
        if not URL in control:
            sortida.write(page.url+"\n")
            control.append(URL)
            cont+=1

    if cont==0:
        cadena="###URL###"
        sortida.write(cadena+"\n")
        sortida.write(URL+"\n")
        
        cadena="###Google###"
        sortida.write(cadena+"\n")
        googlelinks=searchGoogle(URL)
        for gl in googlelinks:
            sortida.write(gl+"\n")


top = Tk()
top.title("MTUOC-sitemapGUI")

L1=tkinter.Label(top, text = str("URL:")).grid(row=0,column=0)
E1 = tkinter.Entry(top, bd = 5, width=40, justify="left")
E1.grid(row=0,column=1)

#L2=tkinter.Label(top, text = str("Prefix:")).grid(row=1,column=0)
#E2 = tkinter.Entry(top, bd = 5, width=40, justify="left").grid(row=1,column=1)
#L3=tkinter.Label(top, text = str("Name:")).grid(row=2,column=0)
#E3 = tkinter.Entry(top, bd = 5, width=40, justify="left").grid(row=2,column=1)
B4=tkinter.Button(top, text = str("Get sitemap!"), borderwidth = 1, command=go,width=14).grid(sticky="W",row=5,column=0)

top.mainloop()
