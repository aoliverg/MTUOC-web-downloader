from usp.tree import sitemap_tree_for_homepage
import requests
import codecs
import sys

import requests



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
for page in tree.all_pages():
    print(page.url)
    sortida.write(page.url+"\n")
