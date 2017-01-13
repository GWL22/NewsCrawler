# -*- coding: utf-8 -*-

import sys
import re
import requests
import urlparse
import datetime
import json

from bs4 import BeautifulSoup
from newsdao import NewsDAO
from commentdao import CommentDAO

reload(sys)
sys.setdefaultencoding('utf-8')


class CommentCrawler(object):
    def __init__(self, newsdao, commentdao):
        self.newsdao = newsdao
        self.commentdao = commentdao
        self.recent_news = self.newsdao.get_recent_news(days=3)

    def crawl_recent_news_comment(self):
        for link in self.recent_news:
            self.crawl_comment(link)

    def crawl_comment(self, link, page=1):
        headers = {}
        headers['referer'] = link

        query_dict = urlparse.parse_qs(urlparse.urlsplit(link).query)
        oid = query_dict['oid'][0]
        aid = query_dict['aid'][0]

        comment_base_url = 'https://apis.naver.com/commentBox/cbox/web_naver_list_jsonp.json?ticket=news&templateId=default_it&pool=cbox5&lang=ko&country=KR&objectId=news{}&categoryId=&pageSize=100&indexSize=1&groupId=&page={}&sort=new'
        url = comment_base_url.format('{}%2C{}'.format(oid, aid), page)

        response = requests.get(url, headers=headers)

        m = re.search('_callback\((.*)\)', response.content)

        if m:
            # json으로 변경
            comments = json.loads(m.group(1))['result']['commentList']
            if not comments:
                return

            for comment in comments:
                id              = comment['commentNo']
                news_id         = link
                contents        = comment['contents']
                written_time    = comment['regTime']
                crawl_time      = datetime.datetime.strptime(written_time.split('+')[0], '%Y-%m-%dT%H:%M:%S')
                sympathy_count  = comment['sympathy_count']
                antipathy_count = comment['antipathy_count']

                cid = aid + str(id)
                self.commentdao.save_comment(cid, news_id, str(contents))

            self.crawl_comment(link, page + 1)

if __name__ == '__main__':
    newsdao = NewsDAO()
    commentdao = CommentDAO()

    crawler = CommentCrawler(newsdao, commentdao)
    crawler.crawl_recent_news_comment()
