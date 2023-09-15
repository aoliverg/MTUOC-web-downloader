# MTUOC-web-downloader
A set of scripts to download a whole website and store it locally. 

# 1. Introduction

In this repository a set of scripts for downloading a whole website are available. To perform this task, two different steps should be:

- Retrieve all the sitemap of the website with MTUOC-sitemap.py
- Download all the links in the sitemap, and while downloading, detecting new internal links to download. This can be performed by MTUOC-download-from-sitemap-selenium.py and MTUOC-download-from-sitemap-requests.py

Not all strategies (selenium and requests) work for all websites, so you should try them and decide which is more suitable. You may also find some websites from where you can't get any file.

# 2. Prerequisites

The programs are develped in Python version 3 and you need a Python 3 interpreter in your system. To run the programs you should install the following prerequisites:

For MTUOC-sitemap.py

```
requests
ultimate_sitemap_parser
beautifulsoup4
```

You can use pip or pip3 (depending on your installation) (use sudo if you plan to install in the whole system or use a virtual environment):

```
pip3 install beautifulsoup4 PyYAML requests selenium urllib3
```

# 3. MTUOC-sitemap

You can use the option -h to get the help of the program:

```
python3 MTUOC-sitemap.py -h
usage: MTUOC-sitemap.py [-h] -u URL [-p PREFIX] [-n FILENAME]

MTUOC program to get the links from a website.

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     The URL of the website to explore.
  -p PREFIX, --prefix PREFIX
                        The prefix to use for the file containing the links. The full name will
                        contain the prefix and the domain.
  -n FILENAME, --name FILENAME
                        The name of the file containing the links. This option overrides -p/--prefix.
```

If we want to get the sitemap of a website, let's say https://medlineplus.gov/, we can run MTUOC-sitemap.py giving the URL with the option -u or --url. If we don't specify a prefix or a name, an automatic name for the sitemap file will be generated ("sitemap-"+domain+".txt")

```
python3 MTUOC-sitemap.py -u https://medlineplus.gov
```
The sitemap would be named: sitemap-medlineplus_gov.txt We can specify a different prefix with the -p/--prefix option or a name with the -n/--name option. The sitemap will contain "all" the links in the webpage, or at least some of them.

Now, in sitemap-medlineplus_gov.txt we have all the links in the website (the links found in the sitemap):

```
https://medlineplus.gov/all_easytoread.html
https://medlineplus.gov/games.html
https://medlineplus.gov/healthchecktools.html
https://medlineplus.gov/druginfo/herb_All.html
https://medlineplus.gov/organizations/all_organizations.html
https://medlineplus.gov/organizations/orgbytopic_v.html
https://medlineplus.gov/organizations/orgbytopic_e.html
https://medlineplus.gov/organizations/orgbytopic_n.html
https://medlineplus.gov/organizations/orgbytopic_j.html
https://medlineplus.gov/organizations/orgbytopic_p.html
https://medlineplus.gov/organizations/orgbytopic_g.html
...

If no links are retrieved, the output file will contain the URL and some links obtained from a search in Google.

Sometimes these sitemaps are too large. You can edit the file, copy desired links to another file, use grep or whatever to adapt the results to your needs.

# 4. MTUOC-download-from-sitemap


To download the linkgs in the sitemap file, or the edited version of the sitemap, you can run MTUOC-download-from-sitemap.py giving the file containing the sitemap and the directory where the website will be downloaded as parameters:

```
python3 MTUOC-download-from-sitemap.py sitemapMedline.txt  dirMedline
```

Under the directory dirMedline all the structure and files of the website will be stored.

