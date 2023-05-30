# MTUOC-web-downloader
A script to download a whole website and store it locally. 

# Prerequisites

To run the program you should install the following prerequisites

'''
beautifulsoup4
PyYAML
requests
selenium
urllib3
'''

You can use pip or pip3 (depending on your installation) (use sudo if you plan to install in the whole system or use a virtual environment):

```
pip3 install beautifulsoup4 PyYAML requests selenium urllib3
```

# Configuring the download task

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

# Downloading the website

To download the website, if you want to use the config-web-downloader.yaml file you can simply write in terminal (use python3 or python depending on your installation):

```
python3 MTUOC-web-downloader.py
```

If you have renamed the config-web-downloader.yaml file, you can speciy it in the command:

```
python3 MTUOC-web-downloader.py -c yourOwnConfig.yaml
```


