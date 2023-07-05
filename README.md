# MTUOC-web-downloader
A set of scripts to download a whole website and store it locally. 

# 1. Introduction

In this repository a set of scripts for downloading a whole website are available. To perform this task, two different strategies can be performed:

- Starting from a URL, detect, store and follow all the links in the web page, and performing this until all the website is downloaded and stored localy, or a maximum number of webpages are downloaded, or a maximumn time is consumed. This methodology is implemented in the script MTUOC-web-downloader.py.
- Retrieve all the sitemap of the website with MTUOC-sitemap.py and download all the URLs from the sitemap with MTUOC-download-from-sitemap.py

Not all strategies work for all websites, so you should try them and decide which is more suitable.

# 2. Prerequisites

The programs are develped in Python version 3 and you need a Python 3 interpreter in your sistem. To run the programs you should install the following prerequisites

```
beautifulsoup4
PyYAML
requests
selenium
urllib3
```

You can use pip or pip3 (depending on your installation) (use sudo if you plan to install in the whole system or use a virtual environment):

```
pip3 install beautifulsoup4 PyYAML requests selenium urllib3
```

# 3. MTUOC-web-downloader
## 3.1. Configuring the download task

Before using the program you should edit the config-web-downloader.py to tell the websit to download and other configurations:

```
url: https://webtodownload.com
action: start
#one of start/resume

linksfile: auto
outfile: auto
outdir: auto

timeout: 10
maxtime: -1
#-1 means no limit
max_urls: -1
#-1 means no limit
```

This file can be renamed if needed.

## 3.2. Downloading the website

To download the website, if you want to use the config-web-downloader.yaml file you can simply write in terminal (use python3 or python depending on your installation):

```
python3 MTUOC-web-downloader.py
```

If you have renamed the config-web-downloader.yaml file, you can speciy it in the command:

```
python3 MTUOC-web-downloader.py -c yourOwnConfig.yaml
```

# 4. Download from sitemap

## 4.1. Getting the sitemap of the site

If we want to get the sitemap of a website, let's say https://medlineplus.gov/, we can run MTUOC-sitemap.py giving as a first parameter the URL and as the second parameter the file where the sitemap will be stored:

```
python3 MTUOC-sitemap.py https://medlineplus.gov/ sitemapMedline.txt
```

Now, in sitemapMedline.txt we have all the links in the website (the links found in the sitemap):

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
```

Sometimes these sitemaps are too large. You can edit the file, copy desired links to another file, use grep or whatever to adapt the results to your needs.

## 4.2. Downloading the links in the sitemap

To download the linkgs in the sitemap file, or the edited version of the sitemap, you can run MTUOC-download-from-sitemap.py giving the file containing the sitemap and the directory where the website will be downloaded as parameters:

```
python3 MTUOC-download-from-sitemap.py sitemapMedline.txt  dirMedline
```

Under the directory dirMedline all the structure and files of the website will be stored.

