#    MTUOC-download-from-sitemap
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

import codecs
import sys
import os

from bs4 import BeautifulSoup

import requests

from random import randint
from time import sleep

import argparse

from urllib.parse import urlparse
from urllib.parse import urljoin

import pathlib

from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askdirectory

from tkinter import ttk


import tkinter 

def base_url(url, with_path=False):
    parsed = urlparse(url)
    path   = '/'.join(parsed.path.split('/')[:-1]) if with_path else ''
    parsed = parsed._replace(path=path)
    parsed = parsed._replace(params='')
    parsed = parsed._replace(query='')
    parsed = parsed._replace(fragment='')
    return parsed.geturl()

fileextensions=[".pdf",".PDF",".doc",".docx",".odt"]
htmlextensions=[".html",".HTML","htm","HTM"]


def go():
    sitemapfile=E1.get().strip()
    nofollow=False
    if var.get()==1:
        nofollow=True
    minwait=int(E6.get().strip())
    maxwait=int(E7.get().strip())
    maxdowload=int(E8.get().strip())
    outdir=E2.get().strip()
    strategy=CB4.get()
    timeout=int(E9.get().strip())
    
    if strategy=="selenium":
        from selenium import webdriver
        from selenium.webdriver import Firefox
        from selenium.webdriver.firefox.options import Options
        from selenium.webdriver.support.ui import WebDriverWait
        opts = Options()
        opts.add_argument('-headless')
        opts.accept_untrusted_certs = True
        browser = webdriver.Firefox(options=opts)
        browser.set_page_load_timeout(timeout)  
    
    entrada=codecs.open(sitemapfile,"r",encoding="utf-8")
    logfilename="downloadlog-"+os.path.basename(sitemapfile).replace("sitemap-","")
    sortidalog=codecs.open(logfilename,"w",encoding="utf-8")

    links=[]
    done=[]


    for linia in entrada:
        linia=linia.rstrip()
        if not linia in links and not linia.startswith("#"):
            links.append(linia)


    moreelements=len(links)
    totaldownloaded=0
    while moreelements>0:
        cadenalog=[]
        try:
            
            link=links.pop(0)
            done.append(link)
            baseurl=base_url(link)
            domain = urlparse(link).netloc
            camps=os.path.split(link)
            filename=camps[-1]
            dirs=camps[0].replace(baseurl,"").split("/")[1:]
            dir1=os.path.join(outdir,domain,"/".join(dirs))
            if not os.path.exists(dir1):
                os.makedirs(dir1)
            fullfilename=os.path.join(dir1,filename)
            file_extension = pathlib.Path(fullfilename).suffix
            if file_extension in fileextensions:
                cadenalog.append("DOWNLOADING")
                cadenalog.append(str(link))
                cadenalog.append(fullfilename)
                print("DOWNLOADING: ",link," to ", fullfilename)
                response = requests.get(link) 
                document = open(fullfilename, 'wb')
                document.write(response.content)
                document.close()
                cadenalog.append("SUCCESS")
                totaldownloaded+=1
                sleep(randint(minwait,maxwait))
            else:
                print("GETTING: ",link)
                cadenalog.append("GETTING")
                cadenalog.append(link)
                if strategy=="selenium":
                    browser.get(link)
                    delay = 3
                    html = browser.page_source
                elif strategy=="requests":
                    response = requests.get(link)
                    page_source = response.content.decode("utf-8")
                    html=page_source
                #text=h.handle(html)
                soup = BeautifulSoup(html, "lxml")
                newlinks=soup.findAll('a')
                if not nofollow:
                    for l in newlinks:
                        l2=l.get('href')
                        if not l2==None and l2.startswith("/"):
                            l2=urljoin(baseurl,l2)
                        if not l2==None and l2.startswith(baseurl):
                            if not l2 in links and not l2 in done:
                                print("NEWLINK:",l2)
                                links.append(l2)
                file_extension = pathlib.Path(fullfilename).suffix
                
                if not file_extension in htmlextensions:
                    fullfilename=fullfilename+".html"
                fullfilename=fullfilename.replace("?","_").replace("<","_")
                cadenalog.append(fullfilename)
                sortida=codecs.open(fullfilename,"w",encoding="utf-8")
                sortida.write(html+"\n")
                sortida.close()
                cadenalog.append("SUCCESS")
                cadenalog.append(strategy)
                totaldownloaded+=1
                sleep(randint(minwait,maxwait))
            print("DONE: ",str(len(done)),"TO DOWNLOAD:",str(moreelements))
        
        except:
            print("ERROR:",sys.exc_info())
            cadenalog.append("ERROR")
            cadenalog.append(str(sys.exc_info()[0]))
        moreelements=len(links)
        cadenalog="\t".join(cadenalog)
        sortidalog.write(cadenalog+"\n")
        sortidalog.close()
        sortidalog=codecs.open(logfilename,"a",encoding="utf-8")
        if totaldownloaded>=maxdowload:
            sys.exit()
    sortidalog.close()    

def select_sitemap_file():
    infile = askopenfilename(initialdir = ".",filetypes =(("txt files","*.txt"),("All Files","*.*")),
                           title = "Select the input file.")
    E1.delete(0,END)
    E1.insert(0,infile)
    E1.xview_moveto(1)

def select_output_directory():
    infile = askdirectory(initialdir = ".",title = "Select the output directory.")
    E2.delete(0,END)
    E2.insert(0,infile)
    E2.xview_moveto(1)

top = Tk()
top.title("MTUOC-download-from-sitemapGUI")

B1=tkinter.Button(top, text = str("Select sitemap file"), borderwidth = 1, command=select_sitemap_file,width=18).grid(row=0,column=0)
E1 = tkinter.Entry(top, bd = 5, width=80, justify="right")
E1.grid(row=0,column=1)

B2=tkinter.Button(top, text = str("Select output directory"), borderwidth = 1, command=select_output_directory,width=18).grid(row=1,column=0)
E2 = tkinter.Entry(top, bd = 5, width=80, justify="right")
E2.grid(row=1,column=1)
currentdir = os.getcwd()
defaultdir=os.path.join(currentdir,"download")
E2.insert(0,defaultdir)

L3=tkinter.Label(top, text = str("Strategy:")).grid(row=3,column=0)

#list_items = tkinter.Variable(value=["Generic","English","Spanish"])
list_items = ["selenium","requests"]
CB4 = ttk.Combobox(top, state="readonly", values=list_items)
CB4.grid(row=3,column=1, sticky="w")
CB4.current(0)

L5=tkinter.Label(top, text = str("no follow:")).grid(row=4,column=0)
var = tkinter.IntVar()
CB5 = tkinter.Checkbutton(top, text="", variable=var)
CB5.grid(row=4,column=1,sticky="w")

L6=tkinter.Label(top, text = str("min wait:")).grid(row=5,column=0)
E6 = tkinter.Entry(top, bd = 5, width=10, justify="right")
E6.grid(row=5,column=1,sticky="w")
E6.insert(0,0)

L7=tkinter.Label(top, text = str("max wait:")).grid(row=6,column=0)
E7 = tkinter.Entry(top, bd = 5, width=10, justify="right")
E7.grid(row=6,column=1,sticky="w")
E7.insert(0,2)

L8=tkinter.Label(top, text = str("max. downloads:")).grid(row=7,column=0)
E8 = tkinter.Entry(top, bd = 5, width=10, justify="right")
E8.grid(row=7,column=1,sticky="w")
E8.insert(0,1000000)

L9=tkinter.Label(top, text = str("timeout:")).grid(row=8,column=0)
E9 = tkinter.Entry(top, bd = 5, width=10, justify="right")
E9.grid(row=8,column=1,sticky="w")
E9.insert(0,10)

B4=tkinter.Button(top, text = str("Download!"), borderwidth = 1, command=go,width=14).grid(sticky="W",row=9,column=0)

top.mainloop()

    
    
    
    
    
