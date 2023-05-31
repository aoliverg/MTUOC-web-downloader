#    Copyright: Antoni Oliver (2023) - Universitat Oberta de Catalunya - aoliverg@uoc.edu
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import argparse
import yaml
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
#from requests_html import HTMLSession
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import sys
import os
import time
import codecs

import requests
#import tempfile

from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)
    
def createDIRS(rootdir,URL):
    isExist = os.path.exists(rootdir)
    if not isExist and len(rootdir)>0:
       os.makedirs(rootdir)
    URL=URL.replace("https://","").replace("http://","").replace("//","/")
    subdirs=URL.split("/")
    for i in range(0,len(subdirs)):
        try:
            tocreate=rootdir+"/"+"/".join(subdirs[0:i])
            if os.path.isfile(tocreate):
                os.rename(tocreate,tocreate+"_copy")
                
            isExist = os.path.isdir(tocreate)
            if not isExist and len(tocreate)>0:
               os.makedirs(tocreate)
        except KeyboardInterrupt:
            sys.exit(0)
        except:
            print("Error creating directory:",tocreate,sys.exc_info())

def arregla(text):
    textlist=text.split("\n")
    textlist2=[]
    i=0
    for t in textlist:
        try:
            if textlist[i+1].strip()[0].isupper():
                textlist2.append(t+"@SALTPARA@")
            else:
                textlist2.append(t)
        except:
            textlist2.append(t)
        i+=1
    aux="".join(textlist2)
    aux2=aux.replace("@SALTPARA@","\n")
    return(aux2)

def get_page(browser,url,source_dir):
    """
    Returns all URLs that is found on `url` in which it belongs to the same website
    """
    createDIRS(source_dir,url)
    urls = set()
    try:
        try:
            browser.get(url)
        except KeyboardInterrupt:
            sys.exit(0)
        except:
            print("ERROR:",sys.exc_info())
        
        source=browser.page_source
        
        
        URL=url.replace("https://","").replace("http://","").replace("//","/")
        filename=source_dir+"/"+URL
        try:
            sourcefile=codecs.open(filename,"w",encoding="utf-8")
            sourcefile.write(source+"\n")
            sourcefile.close()
        except:
            pass
        
                
        elems = browser.find_elements(By.XPATH,"//a[@href]")
        urls=set()
        for elem in elems:
            href=elem.get_attribute("href")
            if is_valid(href):
                urls.add(href)
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        print("Error: ",sys.exc_info())       
    return urls

def searchGoogle(query):

    headers = {
        'User-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }

    params = {
      'q': 'site:'+query,
      #'gl': 'us',
      #'hl': 'en',
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

parser = argparse.ArgumentParser(description='MTUOC-server. With no arguments the config-web-downloader.yaml file will be used.')

parser.add_argument('-c','--config', action="store", dest="config", help='The configuration file to be used.',required=False)


args = parser.parse_args()
if args.config:
    configfile=args.config
else:
    configfile="config-web-downloader.yaml"

stream = open(configfile, 'r',encoding="utf-8")
config=yaml.load(stream, Loader=yaml.FullLoader)

url=config["url"]
domain_name = urlparse(url).netloc
action=config["action"]

linksfile=config["linksfile"]
if linksfile=="auto": linksfile="links-"+domain_name+".txt"
outfile=config["outfile"]
if outfile=="auto": outfile="text-"+domain_name+".txt"
outdir=config["outdir"]
if outdir=="auto":  outdir=domain_name

source_dir=outdir

timeout=float(config["timeout"])

maxtime=float(config["maxtime"])
if maxtime==-1:
    maxtime=1000000000000
else:
    maxtime=float(maxtime)

#-1 means no limit
max_urls=float(config["max_urls"])
if max_urls==-1:
    max_urls=1000000000000
else:
    max_urls=float(max_urls)
toinspect=set()
alreadydone=set()

opts = Options()
opts.add_argument('-headless')
opts.accept_untrusted_certs = True
browser = webdriver.Firefox(options=opts)
browser.set_page_load_timeout(8)

if action=="start":
    sortida=codecs.open(linksfile,"w",encoding="utf-8")
else:
    entrada=codecs.open(linksfile,"r",encoding="utf-8")
    for linia in entrada:
        linia=linia.rstrip()
        alreadydone.add(linia)
    entrada.close()
    sortida=codecs.open(linksfile,"a",encoding="utf-8")

start = time.time()

toinspect.add(url)
continua=True
while continua:
    try:
        URL=toinspect.pop()
        if not URL in alreadydone:
            print(URL,len(alreadydone),len(toinspect))
            sortida.write(URL+"\n")
            links = get_page(browser,URL,source_dir)
            for link in links:
                link = urljoin(url, link)
                parsed_href = urlparse(link)
                # remove URL GET parameters, URL fragments, etc.
                href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
                if url in href and not link in alreadydone:
                    toinspect.add(link)
            alreadydone.add(URL)
        if time.time() > start + maxtime: 
            continua=False
        if len(alreadydone)>=max_urls:
            continua=False
            proceed=False
    except KeyboardInterrupt:
        sys.exit(0)
if len(alreadydone)<min_links:
    googlelinks=searchGoogle(url)
    for gl in googlelinks:
        toinspect.add(gl)

    continua=True
    while continua:
        try:
            URL=toinspect.pop()
            if not URL in alreadydone:
                print(URL,len(alreadydone),len(toinspect))
                sortida.write(URL+"\n")
                links = get_all_website_links(browser,URL)
                for link in links:
                    link = urljoin(url, link)
                    parsed_href = urlparse(link)
                    # remove URL GET parameters, URL fragments, etc.
                    href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
                    if url in href and not link in alreadydone:
                        toinspect.add(link)
                alreadydone.add(URL)
            if time.time() > start + maxtime: 
                continua=False
            if len(alreadydone)>=max_urls:
                continua=False
        except KeyboardInterrupt:
            sys.exit(0)
sortida.close()
