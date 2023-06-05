from usp.tree import sitemap_tree_for_homepage
import requests
import codecs
import sys

URL=sys.argv[1]
outfile=sys.argv[2]

sortida=codecs.open(outfile,"w",encoding="utf-8")

tree = sitemap_tree_for_homepage(URL)
for page in tree.all_pages():
    print(page.url)
    sortida.write(page.url+"\n")
