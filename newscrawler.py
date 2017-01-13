# -*- coding: utf-8 -*-
import sys
import requests

from bs4 import BeautifulSoup
from newsdao import NewsDAO
from memcache import MemCache

reload(sys)
sys.setdefaultencoding('utf-8')


def find_a(tags):
    return tags.name == 'a' and not tags.has_attr('class') \
                            and tags.has_attr('href')


class NaverNewsCrawler(object):
    def __init__(self, newsdao, memcache):
        self.newsdao = newsdao
        self.memcache = memcache
        self.urls = memcache.get_crawl_urls()

    def crawl_link(self):
        for url in self.urls:
            res = requests.get(url)
            content = res.content

            soup = BeautifulSoup(content)

            table = soup.find('table', attrs={'class': 'container'})
            for a in table.find_all(find_a):
                link = a['href']
                self.crawl_title_content(link)

    def crawl_title_content(self, link):
        res = requests.get(link)
        content = res.content

        soup = BeautifulSoup(content)

        try:
            title = soup.find('h3', attrs={'id': 'articleTitle'}) \
                        .get_text()
            content = soup.find('div', attrs={'id': 'articleBodyContents'}) \
                          .get_text() \
                          .strip()
        except Exception as e:
            return

        # if news saved
        if self.newsdao.save_news(link, str(title), str(content)):
            self.memcache.cache_news(str(title), str(content))

if __name__ == '__main__':
    memcache = MemCache()
    newsdao = NewsDAO()

    urls = ['http://news.naver.com/main/main.nhn?mode=LSD&mid=shm&sid1=105']
    crawler = NaverNewsCrawler(newsdao, memcache)
    crawler.crawl_link()
