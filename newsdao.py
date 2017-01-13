# -*- coding: utf-8 -*-

import sys
import datetime

from model import News
from connection import Session
from sqlalchemy import func

reload(sys)
sys.setdefaultencoding('utf-8')


class NewsDAO(object):
    def __init__(self):
        pass

    def save_news(self, news_id, title, content):
        saved = False
        session = Session()
        if not self.get_news_by_id(news_id):
            print news_id
            news = News(link=news_id,
                        title=title,
                        content=content,
                        crawl_time=datetime.datetime.now())
            session.add(news)
            session.commit()
            saved = True
        session.close()

        return saved

    def get_news_by_id(self, news_id):
        try:
            session = Session()
            row = session.query(News) \
                         .filter(News.link == news_id) \
                         .first()
            return row
        except Exception as e:
            print e
        finally:
            session.close()

    def get_news_by_keyword_in_title(self, keyword):
        pass

    def get_news_by_keyword_in_content(self, keyword):
        data = []
        session = Session()
        result = session.query(News) \
                        .filter(News.content.like('%' + keyword + '%')) \
                        .all()
        for row in result:
            news = {}
            news['link'] = row.link
            news['title'] = row.title
            news['content'] = row.content

            data.append(news)

        return data

    def get_recent_news(self, days=7):
        now = datetime.datetime.now()
        from_time = (now - datetime.timedelta(days=days)).date()

        session = Session()
        # list of tuple
        result = session.query(News.link) \
                        .filter(func.date(News.crawl_time) >= from_time) \
                        .all()
        # result = session.query(News.link).filter(News.link == 'http://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=103&oid=421&aid=0002353594').all()
        result = [row[0] for row in result]

        print result
        return result
