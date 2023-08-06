import datetime
import json
import os
import shelve

import requests
import PIL
from dateutil.parser import parse as dateutil_parser


from .custom_exceptions import NoNewsError, NotCachedError


class CacheDB:
    """ Class that caches news  """

    def __init__(self, source=None):
        self.db = os.path.join(os.path.expanduser('~'), 'cache.db')  # cache file in user's home directory
        self.source = source

    def save(self, news):
        """
        Saves news to cache according to their source.
        Source is the key and their value is main feed containing list of cached news

        """

        with shelve.open(self.db, writeback=True) as db:
            date = news['pubDate']
            # convert date to YYYYMMDD format
            news['pubDate'] = date if date == 'No info' else dateutil_parser(date).strftime('%Y%m%d')
            if self.source in db:
                feed_str = db[self.source]
                feed = json.loads(feed_str)
                cached_news_titles = [cached_news['title'] for cached_news in feed['news_list']]
                # checks if news going to be saved has already been cached to avoid duplicates
                if feed['title'] != news['title'] and news['title'] not in cached_news_titles:
                    temp = feed['news_list']
                    temp.append(news)
                    feed['news_list'] = temp
                    db[self.source] = json.dumps(feed)
            else:
                # if there is no key with source then it's first value is main rss feed.
                # Subsequent saves for this source go to main rss feed's news list
                news['news_list'] = []
                # cache feed's image
                image_cache = CacheImage(news)
                image_cache.save()
                # saved in string to avoid recursion error while pickling object
                db[self.source] = json.dumps(news)

    def get_with_given_source(self, date, limit):
        """ Gets news from specified source  in a given limit

            Return list of one tuple containing main rss feed and its news list
         """
        if limit is not None and limit <= 0:
            raise NoNewsError

        with shelve.open(self.db) as db:
            try:
                feed = json.loads(db[self.source])
                self.convert_date_format(feed)
                news_list = feed['news_list']
            except KeyError:
                msg = f'News from source {self.source} are not cached yet'
                raise NotCachedError(msg)

            filtered_news = []
            for news in news_list:
                if news['pubDate'] == date.strftime('%Y%m%d'):
                    self.convert_date_format(news)
                    filtered_news.append(news)
            if not filtered_news:
                raise NoNewsError
            else:
                return [(feed, filtered_news[:limit])]

    def get_from_all_source(self, date, limit):
        """ Gets news from all sources if source is not specified with --date option

            Returns list of tuples containing main rss feed and its news list

            If  limit is given and is greater than first rss feed's news list then

            second rss feed and its news list is returned as the second tuple item of list

            and so on until limit is reached
         """
        if limit is not None and limit <= 0:
            raise NoNewsError

        with shelve.open(self.db) as db:
            all_sources = db.keys()
            filtered_news_with_sources = []
            total_news_count = 0
            for source in all_sources:
                filtered_news = []
                feed = json.loads(db[source])
                self.convert_date_format(feed)
                for news in feed['news_list']:
                    if limit is not None and total_news_count >= limit:
                        filtered_news_with_sources.append((feed, filtered_news))
                        return filtered_news_with_sources

                    if news['pubDate'] == date.strftime('%Y%m%d'):
                        self.convert_date_format(news)
                        filtered_news.append(news)
                        total_news_count += 1
                filtered_news_with_sources.append((feed, filtered_news))

            all_filtered_news = [news for feed, news in filtered_news_with_sources]
            if not any(all_filtered_news):
                raise NoNewsError
            else:
                return filtered_news_with_sources

    def get(self, date, limit):
        """ Main get method that patches to get_with_given_source or get_from_all_source

            according to existence of source
         """

        if self.source:
            return self.get_with_given_source(date, limit)
        else:
            return self.get_from_all_source(date, limit)

    @staticmethod
    def convert_date_format(news):
        """ Convert news published date to human-readable format """
        if news['pubDate'] != 'No info':
            date_obj = datetime.datetime.strptime(news['pubDate'], '%Y%m%d')
            news['pubDate'] = date_obj.strftime('%d %B, %Y ')

    def clear(self):
        """ Clears caches when --clear-cache option is given"""

        with shelve.open(self.db) as db:
            db.clear()
            print('Cached news was removed')

    def remove(self, source):
        """ Removes key from cache. Mainly used for unittests """

        with shelve.open(self.db) as db:
            del db[source]


class CacheImage:

    image_cache_dir = os.path.join(os.path.expanduser('~'), 'image_cache')

    if not os.path.exists(image_cache_dir):
        os.makedirs(image_cache_dir)

    def __init__(self, feed):
        self.feed = feed
        self.title = feed['title']
        self.image = feed['image']
        if self.image != 'No info':
            self.image_extension = self.image['url'].split('.')[-1]
            self.image_name = f"{self.title.replace(' ', '')}.{self.image_extension}"
        else:
            self.image_name = 'No info'

    def save(self):
        if self.image != 'No info' and not os.path.exists(os.path.join(self.image_cache_dir, self.image_name)):
            image = requests.get(self.image['url']).content
            with open(os.path.join(self.image_cache_dir, self.image_name), 'wb') as file:
                file.write(image)

    def get_image(self):
        if os.path.exists(os.path.join(self.image_cache_dir, self.image_name)):
            image = {'url': os.path.join(self.image_cache_dir, self.image_name),
                     'link': self.image['link'],
                     'title': self.image['title']
                     }
            return image
        else:
            return 'No info'
