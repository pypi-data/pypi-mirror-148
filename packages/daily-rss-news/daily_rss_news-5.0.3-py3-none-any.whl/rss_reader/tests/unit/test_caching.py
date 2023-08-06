import datetime

import pytest

from rss_reader.utils.caching import CacheDB, NoNewsError, NotCachedError


date = datetime.datetime.strptime('2022-04-10', '%Y-%m-%d')

feed_example = {
    'title': 'Some title',
    'link': 'Some link',
    'description': 'Some description',
    'pubDate': '2022-04-10',
    'image': 'Some image'
}

news_example = {
    'title': 'news title',
    'link': 'news link',
    'description': 'news description',
    'pubDate': '2022-04-10',
    'image': 'No info'
}

source = 'Some source'


def test_not_cached_source():

    with pytest.raises(NotCachedError):
        cache = CacheDB('not cached source')
        cache.get(date, 1)
        cache.remove('not cached source')


def test_cached_news_count():

    cache = CacheDB(source)
    cache.save(feed_example.copy())
    cache.save(news_example.copy())
    news_info = cache.get(date, None)
    feed, news = news_info[0]
    assert len(news) == 1
    cache.remove(source)


def test_cache_with_negative_limit():

    cache = CacheDB(source)
    cache.save(feed_example.copy())
    cache.save(news_example.copy())
    with pytest.raises(NoNewsError):
        cache.get(date, -1)
        cache.remove(source)
