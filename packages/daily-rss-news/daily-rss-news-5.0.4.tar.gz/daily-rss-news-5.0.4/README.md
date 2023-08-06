# Python RSS Reader

## Installation
To install this package type 

```shell
$ pip install daily-rss-news==5.0.4
```

or if you have already installed previous version type

```shell
$ pip install --upgrade daily-rss-news
```

If you do not want to install it , you can clone source code from gitlab

```shell
$ git clone https://gitlab.com/Ilhom_Xusanov/RSS-parser.git
```

## Requirements
This program depends on some third party packages.
If you downloaded it from gitlab, first create virtual environment 
and go to the folder where requirements.txt resides and type
 
```shell
$ pip install -r requirements.txt
```
This will install all packages to run this program.

# Usage
If you installed this packages by pip, you can use it everywhere
by typing
```shell
$ rss-reader [options]
```
or

```shell
$ python -m rss_reader [options]
```


If you downloaded from gitlab, go to root folder where rss_reader.py is,
and you can run python with rss_reader.py module.
#### Note
if you are in different folder specify full path to rss_reader.py to run with python

```shell
$ python rss_reader.py [options]
```

To see help message type
```shell
$ rss-reader -h
```
or
```shell
$ python rss_reader.py -h 
```
output is:
```shell
                                                            ─╯
usage: rss-reader [-h] [--version] [--json] [--verbose] [--limit ] [--date ]
                  [--to-pdf ] [--to-html ] [--clear-cache]
                  [--colorize [{red,green,blue,yellow,magenta,black,cyan}]]
                  [source]

Pure Python command-line RSS reader

positional arguments:
  source                RSS URL

optional arguments:
  -h, --help            show this help message and exit
  --version             Print version info
  --json                Print result as JSON in stdout
  --verbose             Outputs verbose status messages
  --limit []            Limit news topics if this parameter provided
  --date []             Published date of news in format YYYYMMDD
  --to-pdf []           Directory and file name where pdf file is stored
  --to-html []          Directory and file name where html file is stored
  --clear-cache         Clears all news from cache
  --colorize [{red,green,blue,yellow,magenta,black,cyan}]
                        Prints stdout in a colored mode


```
If --version option is given, program prints its version to console and exits.

If --verbose option is given, outputs logs in a INFO level, default is WARNING

if --limit(N) option is given, N number of news, else all news is returned

if --date option is provided with date in format YYYYMMDD , then news published that date will be returned

if -- date option is provided with given source , then only news published in a given date from that source will be returned

if --to-pdf 'file path' or --to-html 'file path' is given, 
converts news into given format and saves in a given 'file path' 

if --clear-cache option is given, all news in cache are removed

if --colorize option is given, news will be displayed in green to console. Default is white.

if --json option is provided, program displays news to console in json format

--json output example:
```shell
$ python rss_reader/rss_reader.py http://rss.cnn.com/rss/edition.rss --json --limit 2                                  ─╯
{
    "title": "CNN.com - RSS Channel - App International Edition",
    "pubDate": "Tue, 12 Apr 2022 18:23:43 GMT",
    "link": "https://www.cnn.com/app-international-edition/index.html",
    "image": {
        "title": "CNN.com - RSS Channel - App International Edition",
        "link": "https://www.cnn.com/app-international-edition/index.html",
        "url": "http://i2.cdn.turner.com/cnn/2015/images/09/24/cnn.digital.png"
    },
    "description": "CNN.com delivers up-to-the-minute news and information on the latest top stories, weather, entertainment, politics and more.",
    "news_list": [
        {
            "title": "Putin: Talks with Ukraine are at a 'dead end'",
            "pubDate": "No info",
            "link": "https://edition.cnn.com/webview/europe/live-news/ukraine-russia-putin-news-04-12-22/h_c91c00763f131bbeed411565ee0b6319",
            "image": "No info",
            "description": "No info"
        },
        {
            "title": "'People often cry during their questioning': CNN speaks to woman investigating Russian war crimes",
            "pubDate": "Tue, 12 Apr 2022 01:05:09 GMT",
            "link": "https://www.cnn.com/videos/world/2022/04/11/russia-war-crimes-investigation-evidence-tapper-lead-dnt-vpx.cnn",
            "image": "No info",
            "description": "CNN speaks with investigators and Ukrainian witnesses who testified about the brutality they witnessed by the Russian military for prosecutors building a case to charge Russia with war crimes."
        }
    ]
}

 
```
## Caching
Retrieved news are cached. Cache file is in home directory called 'cache.db'.
Caching technique is accomplished via shelve library. To get news from cache internet connection is not required.
Each source is the key of shelve file 'cache.db'. Its value is list of news.

Cache is going to grow in size continuously when you read news from rss sources.
To clear cache type 

### Caching images
Directory named image_cache will be created in user's home directory to store feeds' images
in cache. If feed has image, it will be stored in image_cache directory. When --date option is
available images will be displayed from that directory.  

```shell
$ python -m rss_reader --clear-cache
```

## File converting
Program supports two file converting formats pdf and html. To convert news into file formats,
give either --to-pdf or --to-html and file path where file is created. Give your file path 
relative to your current working directory, like if you are in:

```shell
$ home/user/
```

and giving file path 'custom_dir/file.pdf' will create custom_dir directory if not exists and
saves news into file.pdf.

If file path is not given, it will not convert to given file formats. Instead, just prints news to console 

### Note
Retrieving news from cache without specifying source returns all feeds and their news_list.
In that case, temporary files file_{feed_number}.pdf are created in user's home directory, 
merged into given file path and removed.

While converting to html files, give unique file names. Because it will not override existing files
like pdf, instead it appends news to the end of html file.

## Output colorizing
--colorize option is available to print news in a colored mode. It takes one argument, color, 
and prints news in a given color, default is white. Type -h option to see all available colors

To colorize outputs package named colorama was used, and it is supposed to work well with default 
terminals in Linux and Mac, default cmd in Windows


## Tested Rss links
1.[http://feeds.wired.com/wired/index](http://feeds.wired.com/wired/index)
2.[http://feeds.nytimes.com/nyt/rss/Technology](http://feeds.nytimes.com/nyt/rss/Technology)
3.[http://feeds.nature.com/nature/rss/current](http://feeds.nature.com/nature/rss/current)
4.[http://newsrss.bbc.co.uk/rss/newsonline_world_edition/americas/rss.xml](http://newsrss.bbc.co.uk/rss/newsonline_world_edition/americas/rss.xml)
5.[http://feeds.nytimes.com/nyt/rss/HomePage](http://feeds.nytimes.com/nyt/rss/HomePage)
6.[https://news.yahoo.com/rss/](https://news.yahoo.com/rss/)
7.[http://feeds1.nytimes.com/nyt/rss/Sports](http://feeds1.nytimes.com/nyt/rss/Sports)
8.[http://rss.cnn.com/rss/edition.rss](http://rss.cnn.com/rss/edition.rss)

## Testing
Tested modules
   1. log.py
   2. rss_reader.py
   3. arg_parser.py

**Test coverage is 57%**

To run tests go to root folder of program and type:
```shell
$ python -m pytest 
```
to run tests in a specific module type:
```shell
$ python -m pytest 'folder/modulename'
```

to check test coverage run :
```shell
$ python -m pytest --cov=rss_reader/ 
```

