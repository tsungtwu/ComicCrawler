Comic Crawler
=============

Comic Crawler 是用來扒圖的一支 Python Script。擁有簡易的下載管理員、圖書館功能、
與方便的擴充能力。

Todos
-----
* Ignore module.rest in ImageExistsError.

20150608 更新
-------------
* 放上 PyPI，改變安裝方式
* 使用 json 儲存檔案，存檔結構改變。使用 migrate 指令可以將當下目錄的 save.dat,
  library.dat 轉換成新格式。
* 更新方法︰
	- 開啟 cmd，輸入 `pip install comiccrawler`
	- 用 cd 指令進入舊存檔的資料夾。例 `cd /d D:\ComicCrawler-master`
	- 輸入 `comiccrawler migrate` 轉換存檔。
	- 輸入 `comiccrawler gui` 啟動，啟動完再關閉。
	- 開啟資料夾 `%USERPROFILE%\comiccrawler`，把 `setting.ini` 給覆蓋掉。
	- 再次輸入 `comiccrawler gui`。
		+ 以後只要輸入這個指令就能啟動了

Features
--------
* Extendible module design.
* Easy to use function grabhtml, grabimg.
* Auto setup referer and other common headers.

Dependencies
------------
* pyexecjs - to execute javascript.
* pythreadworker - a small threading library.

Development Dependencies
------------------------
* pypandoc - to convert markdown to rst.

下載和安裝（Windows）
------------------
Comic Crawler is on [PyPI][2]. 安裝完 python 後，可以直接用 pip 指令自動安裝。

[2]: https://pypi.python.org/pypi/comiccrawler/@@VERSION

### Python ###
你需要 Python 3.4 以上。安裝檔可以從它的 [官方網站][1] 下載。

[1]: https://www.python.org/

安裝時記得要選「Add python.exe to path」，才能使用 pip 指令。

### Node.js ###
有些網站的 JavaScript 用 Windows 內建的 Windows Script Host 會解析失敗，建議安裝 
[Node.js][3].

[3]: https://nodejs.org/

### Comic Crawler ###
在 cmd 底下輸入以下指令︰

	pip install comiccrawler
	
更新時︰

	pip install --update comiccrawler

	
Supported domains
-----------------
> @@SUPPORTED_DOMAINS


使用說明
-------
```
Usage:
  comiccrawler domains
  comiccrawler download URL [--dest SAVE_FOLDER]
  comiccrawler gui
  comiccrawler migrate
  comiccrawler (--help | --version)
  
Commands:
  domains             列出支援的網址
  download URL        下載指定的 url
  gui                 啟動主視窗
  migrate             轉換當前目錄底下的 save.dat, library.dat 成新格式
  
Options:
  --dest SAVE_FOLDER  設定下載目錄（預設為 "."）
  --help              顯示幫助訊息
  --version           顯示版本
```

圖形介面
-------
![主視窗](http://i.imgur.com/ZzF0YFx.png)

* 在文字欄貼上網址後點「加入連結」或是按 Enter
* 若是剪貼簿裡有支援的網址，且文字欄同時是空的，程式會自動貼上
* 對著任務右鍵，可以選擇把任務加入圖書館。圖書館內的任務，在每次程式啟動時，都會檢查是否有更新。

設定檔
-----
```
[DEFAULT]
; 設定下載完成後要執行的程式，會傳入下載資料夾的位置
runafterdownload = 

; 啟動時自動檢查圖書館更新
libraryautocheck = true

; 下載目的資料夾
savepath = ~/comiccrawler/download

; 開啟 grabber 偵錯
logerror = false

; 每隔 5 分鐘自動存檔
autosave = 5

```
* 設定檔位於 `%USERPROFILE%\comiccrawler\setting.ini`
* 執行一次 `comiccrawler gui` 後關閉，設定檔會自動產生

Module example
--------------
```python
#! python3
"""
This is an example to show how to write a comiccrawler module.

"""

import re
from ..core import Episode

# The header used in grabber method
header = {}

# Match domain
domain = ["www.example.com", "comic.example.com"]

# Module name
name = "This Is an Example"

# With noepfolder = True, Comic Crawler won't generate subfolder for each episode.
noepfolder = False

# Wait 5 seconds between each page
rest = 5

# Specific user settings
config = {
	"user": "user-default-value",
	"hash": "hash-default-value"
}

def loadconfig():
	"""This function will be called each time the config reloaded.
	"""
	header["Cookie"] = "user={}; hash={}".format(config["user"], config["hash"])

def gettitle(html, url):
	"""Return mission title.
	
	Title will be used in saving filepath, so be sure to avoid duplicate title.
	"""
	return re.search("<h1 id='title'>(.+?)</h1>", html).group(1)
	
def getepisodelist(html, url):
	"""Return episode list.
	
	The episode list should be sorted by date, latest at last, so the 
	downloader will download the oldest first.
	"""
	base = re.search("(https?://[^/]+)", url).group(1)
	match_iter = re.finditer("<a href='(.+?)'>(.+?)</a>", html)
	episodes = []
	for match in match_iter:
		m_url, title = match.groups()
		episodes.append(Episode(title, base + m_url))
	return episodes

"""
There are two methods to get images url. If you can get all urls from the 
first page, then use getimgurls. If you have to download each pages to get
image url, use getimgurl and nextpage functions.

You should only use one of two methods. Never write getimgurls and getimgurl
both.
"""

def getimgurls(html, url):
	"""Return the list of all images"""
	
	match_iter = re.finditer("<img src='(.+?)'>", html)
	return [match.group(1) for match in match_iter]
	
def getimgurl(html, page, url):
	"""Return the url of the image"""
	
	return re.search("<img id='showimage' src='(.+?)'>", html).group(1)
	
def getnextpageurl(page, html, url):
	"""Return the url of the next page. Return None if this is the last page.
	"""
	
	match = re.search("<a id='nextpage' href='(.+?)'>next</a>", html)
	return match and match.group(1)
		
def errorhandler(er, ep):
	"""Downloader will call errorhandler if there is an error happened when
	downloading image. Normally you can just ignore this function.
	"""
	pass
```

Author
------
* eight <eight04@gmail.com>