[![image](https://travis-ci.org/Liupold/demeter_dl.svg?branch=master)](https://travis-ci.org/Liupold/demeter_dl)
[![image](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/Liupold)

Demeter Dl (With HarvesterEngine)
=======================================

Aim of the Project:
-------------------

This is a project aim to provide the *Fast , Free & Efficient* way to download
files from internet. At the same time keeping the code readable and flexible.

![](harvest.png)

python version used - 3.7.2 for latest release!

 
***

##Installation 
### Using "pip" (only on python 3.4+)[Recomended]
You will need ffmpeg for complete youtube support.
Install ffmpeg on your platform.

> ```pip install demeter_dl```

And you are good to go. Make sure to *pip3 on linux*. 
After installation use ```python3 -m demeter_dl``` to use the downloader.

### Using pre-compiled binary (Only Windows):
Download and extract the zip from the release. Open the folder you will find a "cli.exe" file. Right click on that and send that to desktop. (Create shortcut). Double click on the sgortcut to launch and use the cli.

##### On LInux use pip to install.

***

## Using the Donwloader(CLI):

* Give any url and hit enter
* A confirnmation message will be shown with file info.
* Hit enter to continue.
* On completion a audible bell will pe played.
* and new instance will be initiated.

some special urls ;)

* art
* clear
* about


***

## Using in your own code (Intoduction):

Let's start out project By downloading a Test File.

*** The file url: https://speed.hetzner.de/100MB.bin ***

Make sure the link is working else report.

Let's get started.

	from demeter_dl.Core import HarvesterEngine
	url = "https://speed.hetzner.de/100MB.bin"
	download_instance = HarvesterEngine(url)  # This will use the default options
	print(download_instance.Get_info())

#### OUTPUT

>FILE NAME     : 100MB.bin,
FILE SIZE     : 100.0 MB(104857600 Bytes),
TARGET        : 


This Patch of code will initiate a download instance and print the information of the file

Now let's see what are the the options availabe during initiation(params):

* **file_name** : Override the filename from the server
* **location**: Overide the file location (Default is the current directory)
* **part_location**: location of the part files (temporary files, Default is current directory)
* **no_of_parts**: How many parts the file will be devided into for speed(More is not always better, Default is 16)
* **max_alive_at_once**: Max no of parts. (Max part allowed to download at the same time Default is 8)

so it seems there are preety good options let's use some

	from demeter_dl.Core import HarvesterEngine
	url = "https://speed.hetzner.de/100MB.bin"
	download_instance = HarvesterEngine(url, file_name="Test file.bin", location="Downloads/")  # This will use the custom options
	print(download_instance.Get_info())

#### OUTPUT

>FILE NAME     : Test file.bin,
FILE SIZE     : 100.0 MB(104857600 Bytes),
TARGET        : Downloads/

satisfied with the output now we will proceed to download the file:
(It's simple AF)

	download_instance.Download()

wait for it to finish and you will see the file in Donwloads folder in your current directory.
For more info go through the cli.py file in src. (Documention is on the way). 
***

## Licence and Copyright

© Rohn chatterjee (Liupold)
Licence -> LGPL 3.0