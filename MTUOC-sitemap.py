from usp.tree import sitemap_tree_for_homepage
import requests
import codecs
import sys

import requests

from bs4 import BeautifulSoup


def searchGoogle(query):

    headers = {
        'User-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }

    params = {
      'q': 'site :'+query,
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

URL=sys.argv[1]
outfile=sys.argv[2]

if not URL.startswith("http"): URL="http://"+URL

response = requests.get(URL)

if response.status_code == 200:
    print('Web site exists')
    URL=response.url
else:
    print('Web site does not exist') 
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
