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

def base_url(url, with_path=False):
    parsed = urllib.parse.urlparse(url)
    path   = '/'.join(parsed.path.split('/')[:-1]) if with_path else ''
    parsed = parsed._replace(path=path)
    parsed = parsed._replace(params='')
    parsed = parsed._replace(query='')
    parsed = parsed._replace(fragment='')
    return parsed.geturl()

sitemapfile=sys.argv[1]
outdir=sys.argv[2]

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
    if not linia in links:
        links.append(linia)


moreelements=len(links)
while moreelements>0:
    link=links.pop(0)
    done.append(link)
    print(link)
    baseurl=base_url(link)
    if link.endswith("/"):
        try:
            direc=link.replace("https://","").replace("http://","")
            direc=os.path.join(outdir,direc)
            if not os.path.exists(direc):
               os.makedirs(direc)
        except:
            print("ERROR:",sys.exc_info())
        
    else:
        try:
            camps=os.path.split(link)
            direc=camps[0:-1]
            direc=link.replace("https://","").replace("http://","")
            filename=camps[-1]+".html"
            direc=os.path.join(outdir,direc)
            fullfile=os.path.join(direc,filename)
            if not os.path.exists(direc):
               os.makedirs(direc)
            try:
            
                if link.endswith(".pdf") or link.endswith(".PDF"):
                    fullfile=fullfile.replace(".html",".pdf")
                    print("DOWNLOADING: ",link," to ", fullfile)
                    response = requests.get(link) 
                    # Write content in pdf file
                    pdf = open(fullfile, 'wb')
                    pdf.write(response.content)
                    pdf.close()
                else:
                    browser.get(link)
                    html = browser.page_source
                    soup = BeautifulSoup(html, "lxml")
                    newlinks=soup.findAll('a')
                    for l in newlinks:
                        l2=l.get('href')
                        if not l2==None and l2.startswith(baseurl):
                            if not l2 in links and not l2 in done:
                                links.append(l2)

                    sortida=codecs.open(fullfile,"w",encoding="utf-8")
                    sortida.write(html+"\n")
                    sortida.close()
            except:
                print("ERROR:",sys.exc_info())
        except:
            print("ERROR:",sys.exc_info())
    moreelements=len(links)
    print("DONE: ",len(done),"TO DOWNLOAD:",moreelements)
    
    
    
    
