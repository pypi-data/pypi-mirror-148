# RSS Reader

## Description

Command-line RSS reader utility implemented in Python

## Installation

``` 
$ pip install -r requirements.txt
```

## Interface

Utility provides the following interface:

```shell
usage: rss_reader.py [-h] [--version] [--json] [--verbose] [--limit LIMIT]
                     source

Pure Python command-line RSS reader.

positional arguments:
  source         RSS URL

optional arguments:
  -h, --help     show this help message and exit
  --version      Print version info
  --json         Print result as JSON in stdout
  --verbose      Outputs verbose status messages
  --limit LIMIT  Limit news topics if this parameter provided
```

## Usage Examples

```
> python3 rss_reader.py http://rss.cnn.com/rss/edition_world.rss --limit 1
```

```shell
Feed: CNN.com - RSS Channel - World

Title: His house was demolished because he is Muslim, he says
Date Published: Thu, 21 Apr 2022 05:36:32 GMT
Description: Shahdullah Baig stands among the rubble of what was once his modest two-bedroom home, his belongings buried under debris and broken bricks.
Link: https://www.cnn.com/2022/04/21/india/india-hindu-muslim-violence-khargone-bulldozing-intl-hnk-dst/index.html

====================================================================================

```

```
> python3 rss_reader.py http://rss.cnn.com/rss/edition_world.rss --limit 1 --json
```

```shell
[
    {
        "Feed Source": "CNN.com - RSS Channel - World",
        "News Item": {
            "Title": "His house was demolished because he is Muslim, he says",
            "Publication Date": "Thu, 21 Apr 2022 05:36:32 GMT",
            "Description": "Shahdullah Baig stands among the rubble of what was once his modest two-bedroom home, his belongings buried under debris and broken bricks.",
            "Link": "https://www.cnn.com/2022/04/21/india/india-hindu-muslim-violence-khargone-bulldozing-intl-hnk-dst/index.html"
        }
    }
]
```

## Feed Sources

1. https://moxie.foxnews.com/feedburner/latest.xml
2. https://rss.nytimes.com/services/xml/rss/nyt/World.xml
3. http://feeds.bbci.co.uk/news/world/rss.xml
4. http://rss.cnn.com/rss/edition_world.rss
5. https://feeds.washingtonpost.com/rss/world?itid=lk_inline_manual_41


