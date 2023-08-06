import argparse
import os.path

import requests
from bs4 import BeautifulSoup

from argument_parser.arg_parser import ArgParser
from converters.displayer import RssDisplayer
from converters.file_converters import FileConverter
from utils.log import SystemLog
from utils.caching import CacheDB, CacheImage
from utils.custom_exceptions import NoNewsError, NotCachedError


class RssReader:
    """ Main class that gets news, parses it and runs as main the program """

    def __init__(self):
        self.news = []
        self.parser = ArgParser()
        self.format = RssDisplayer()
        self.system_log = SystemLog(self.parser.cli_args.colorize + '%(asctime)s : %(levelname)s : %(message)s')

        if self.parser.cli_args.loglevel:
            self.system_log.set_level(self.parser.cli_args.loglevel)
        self.system_log.logger.info(f'Setting command line argument options : source = {self.parser.cli_args.source};'
                                    f' json = {self.parser.cli_args.json}; limit = {self.parser.cli_args.limit}')

    def parse_url(self):
        """ Accepts source and parses it"""

        res = requests.get(self.parser.cli_args.source, timeout=5)
        self.soup = BeautifulSoup(res.content, 'xml')
        self.feed = self.soup.find('channel')
        self.system_log.logger.info(f'Parsed given source {self.parser.cli_args.source}')

    def get_tag_string(self, entry, idx):
        """ Collects entry's tag string if there is, else marks it as no info.

            Caches news from given source
         """

        entry_info = {}
        # entry tags that should be displayed
        tags = ['title', 'pubDate', 'link', 'image', 'description']
        for tag in tags:
            try:
                if tag == 'image':
                    entry_info[tag] = {'title': self.remove_non_ascii(entry.find(tag).title.string),
                                       'link': entry.find(tag).link.string,
                                       'url': entry.find(tag).url.string}
                else:
                    entry_info[tag] = self.remove_non_ascii(entry.find(tag).string).strip()
            except AttributeError:
                entry_info[tag] = 'No info'
                self.system_log.logger.info(f'entry {idx + 1} has no {tag} tag')

        cache = CacheDB(self.parser.cli_args.source)
        cache.save(entry_info.copy())
        self.system_log.logger.info(f'Cached news from source {self.parser.cli_args.source}')
        return entry_info

    @staticmethod
    def remove_non_ascii(text):
        """ Removes non ascii characters """

        if text is not None:
            return ''.join(i for i in text if ord(i) < 128)
        else:
            return 'No info'

    def get_news(self):
        """ Return all news in a given source.
         If limit is set, then return news as the limit size """

        self.parse_url()
        if self.parser.cli_args.limit is not None and self.parser.cli_args.limit <= 0:
            entries = []
        else:
            entries = self.soup.find_all('item', limit=self.parser.cli_args.limit)

        self.feed = self.get_tag_string(self.feed, 0)

        for idx, entry in enumerate(entries):
            entry_info = self.get_tag_string(entry, idx)
            self.news.insert(idx, entry_info)

        self.feed['news_list'] = self.news

        self.system_log.logger.info(f'Returned {len(self.news)} news')

    def convert_to_file(self, file_source):
        if file_source:
            file_format = os.path.splitext(file_source)[1][1:]
            self.system_log.logger.info(f'Converting news into {file_format}')

            file = FileConverter(self.feed, file_source, file_format, self.parser.cli_args.date)
            file.convert()

    def display(self):
        """ Display news in a given format

            If --date option is provided retrieves news from cache
         """

        if self.parser.cli_args.clear_cache:

            cache = CacheDB()
            cache.clear()

        elif self.parser.cli_args.date:

            cache = CacheDB(self.parser.cli_args.source)
            cached_news = cache.get(self.parser.cli_args.date, self.parser.cli_args.limit)

            self.system_log.logger.info(f'Retrieved news from cache')
            self.feed = cached_news

        else:
            self.get_news()
            image_cache = CacheImage(self.feed)
            image_cache.save()

        file_source = self.parser.cli_args.to_pdf or self.parser.cli_args.to_html

        if self.parser.cli_args.json and not self.parser.cli_args.clear_cache:
            self.format.display_news_json(self.feed, self.parser.cli_args.colorize)
            self.convert_to_file(file_source)

        elif not self.parser.cli_args.clear_cache:
            self.convert_to_file(file_source)
            if not file_source:
                self.format.display_news(self.feed, self.parser.cli_args.colorize)


def main():
    rss_reader = RssReader()
    try:
        rss_reader.display()
    except requests.ConnectionError:
        print('Rss reader could not establish connection with server.'
              'Check your internet connection or try again a bit later!')
    except requests.exceptions.MissingSchema:
        print('Please enter source or use --date option without source to get news from cache')
    except argparse.ArgumentTypeError as ex:
        print(ex.args)
    except NotCachedError as ex:
        print(ex)
    except NoNewsError:
        print('No news corresponding to given parameters. Please, give a valid date or limit')
    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    main()
