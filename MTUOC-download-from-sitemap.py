import codecs
import sys
import os

from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait

sitemapfile=sys.argv[1]
outdir=sys.argv[2]

opts = Options()
opts.add_argument('-headless')
opts.accept_untrusted_certs = True
browser = webdriver.Firefox(options=opts)
browser.set_page_load_timeout(5)  


entrada=codecs.open(sitemapfile,"r",encoding="utf-8")

for linia in entrada:
    link=linia.rstrip()
    print(link)
    if link.endswith("/"):
        try:
            direc=link.replace("https://","").replace("http://","")
            direc=os.path.join(outdir,direc)
            if not os.path.exists(direc):
               os.makedirs(direc)
        except:
            pass
        
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
                browser.get(link)
                html = browser.page_source
                sortida=codecs.open(fullfile,"w",encoding="utf-8")
                sortida.write(html+"\n")
                sortida.close()
            except:
                pass
        except:
            pass
