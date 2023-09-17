#    MTUOC-download-from-sitemap-selenium
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

from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait

from bs4 import BeautifulSoup

import urllib.parse
import requests

from random import randint
from time import sleep

import argparse


from urllib.parse import urlparse

import pathlib

def base_url(url, with_path=False):
    parsed = urllib.parse.urlparse(url)
    path   = '/'.join(parsed.path.split('/')[:-1]) if with_path else ''
    parsed = parsed._replace(path=path)
    parsed = parsed._replace(params='')
    parsed = parsed._replace(query='')
    parsed = parsed._replace(fragment='')
    return parsed.geturl()

fileextensions=[".pdf",".PDF",".doc",".docx",".odt"]
htmlextensions=[".html",".HTML","htm","HTM"]
minwait=0
maxwait=3

parser = argparse.ArgumentParser(description='MTUOC program to get the links from a website.')
parser.add_argument('-f','--file', action="store", dest="sitemapfile", help='The file containing the links to download (the sitemap).',required=True)
parser.add_argument('-d','--directory', action="store", dest="outdir", help='The directory where the downladed files will be stored. If not provided, "download" subdirectory will be used.',required=False)


args = parser.parse_args()

sitemapfile=args.sitemapfile

if not args.outdir==None:
    outdir=args.outdir
else:
    outdir="download"


if not os.path.exists(outdir):
    os.makedirs(outdir)

opts = Options()
opts.add_argument('-headless')
opts.accept_untrusted_certs = True
browser = webdriver.Firefox(options=opts)
browser.set_page_load_timeout(5)  

entrada=codecs.open(sitemapfile,"r",encoding="utf-8")

links=[]
done=[]


for linia in entrada:
    linia=linia.rstrip()
    if not linia in links and not linia.startswith("#"):
        links.append(linia)


moreelements=len(links)
while moreelements>0:
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
            print("DOWNLOADING: ",link," to ", fullfilename)
            response = requests.get(link) 
            document = open(fullfilename, 'wb')
            document.write(response.content)
            document.close()
        else:
            print("GETTING: ",link)
            browser.get(link)
            delay = 3
            html = browser.page_source
            response = requests.get(link)
            page_source = response.content.decode("utf-8")
            html=page_source
            #text=h.handle(html)
            soup = BeautifulSoup(html, "lxml")
            newlinks=soup.findAll('a')
            for l in newlinks:
                l2=l.get('href')
                if not l2==None and l2.startswith(baseurl):
                    if not l2 in links and not l2 in done:
                        links.append(l2)
            file_extension = pathlib.Path(fullfilename).suffix
            if not file_extension in htmlextensions:
                fullfilename=fullfilename+".html"
            sortida=codecs.open(fullfilename,"w",encoding="utf-8")
            sortida.write(html+"\n")
            sortida.close()
            sleep(randint(minwait,maxwait))
        print("DONE: ",len(done),"TO DOWNLOAD:",moreelements)
    
    except:
        print("ERROR:",sys.exc_info())
    moreelements=len(links)
    
    

    
    
    
    
    
