Open Download Manager (with OpenEngine)
=======================================

Aim of the Project:
-------------------

This is a project aim to provide the *Fast , Free & Efficient* way to download
files from internet. At the same time keeping the code readable and flexible.

![](harvest.png)

python version used - 3.6.5 for latest release!

 

How to use the CLI:
-------------------

-   Download the release for your platform, Extract, and read the readme.txt for
    how to start the cli.

-   copy and paste the download link and hit enter key.

    -   confirm the sown info about the file. wolah! download started.

    -   if the file is resume-able close the program to stop and will
        automatically resume the next time you try to

 

Features:
---------

-   Super Fast Download speed

-   Auto resume for download supporting resume feature

-   Download YouTube videos just with URL ;)

-   with only audio support for YouTube

-   Supper informative CLI(Command Line Interface)

-   In-Buit Log and Debug Feature

-   Can be implemented directly into other python programs

###### You can also

-   Directly implement into GUI using non-blocking structure!

    -   Chose custom *Location/Name/Max alive* For Each Download.

 

Requirements:
-------------

The following Python modules are needed in order the Program to work **Only if
compiling from source or Interpreting the source! OR implementing dl_engine.**

 

-   threading `pre-installed with python`

-   os `pre-installed with python`

-   time `pre-installed with python`

-   cgi `pre-installed with python`

-   Queue `pre-installed with python`

-   requests `pip install requests`

-   colorama `pip install colorama`

-   urllib `pip install urllib`

-   tqdm `pip install tqdm`

-   cx_freeze `pip install cx_freeze`

-   pafy `pip install pafy`

-   youtube-dl `pip install youtube-dl`

 

Project Structure:
------------------

 

The main **class (OpenEngine)** is stored in **dl_engine.py**

The class required some functionality such as to get the file name / file size
and etc **provided by req_fn.py**

smart thread management is taken care by **smart_thread.py** *available as a
separate project here.*

The main download function and file write part is present in **main_fn.py**

The user friendly CLI is present in **cli.py.**

That’s all.

For Implementation details check **cli.py.**

 

### dl_engine:

class OpenEngine:

Main class where every thing takes place.

Variable:

self.given_url -\> URL provided

self.verify -\> Whether to verify the certificate of the website

self.filename -\> Name of the file to be downloaded

self.url -\> Final redirected URL

self.headed -\> request header for self.url

self.downloadable -\> check if file is downloadable.

self.size -\> file size in Bytes

self.pauseable -\> is download pause able

self.location -\> download location

self.completed -\> is download completed ?

self.done -\> Bytes already downloaded!

self.max_alive_at_once -\> Max no of parts to be downloaded at once(default=8)

self.no_of_parts -\> No of file the file will be divided during
download.(default=16)

self.block -\> To block the thread or not during download.

 

Functions:

self.download -\> download function.

self.pause -\> Not yet implemented!

self.stop -\> working on It!

 

Known issue:
------------

some typo errors.

not working with G-drive

### Report if you found any!

 

Working on:
-----------

-   issues

-   GUI

 

oh Yeah! it’s free and working!
