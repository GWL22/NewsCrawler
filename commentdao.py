# -*- coding: utf-8 -*-

import sys
import datetime

from model import Comment
from connection import Session

reload(sys)
sys.setdefaultencoding('utf-8')


class CommentDAO(object):
    def __init__(self):
        pass

    def save_comment(self, id, news_id, content):
        session = Session()
        if not self.get_comment_by_id(id):
            print content
            comment = Comment(id=id, news_id=news_id, content=content)

            session.add(comment)
            session.commit()

        session.close()

    def get_comment_by_id(self, comment_id):
        try:
            session = Session()
            row = session.query(Comment) \
                         .filter(Comment.id == comment_id) \
                         .first()
            return row
        except Exception as e:
            print e
        finally:
            session.close()

    def get_comment_by_page(self, keyword, page, pagesize):
        if page <= 0 or pagesize <= 0:
            return []

        data = []
        session = Session()
        row = session.query(Comment) \
                     .filter(Comment.content.like('%' + keyword + '%')) \
                     .offset((page-1)*pagesize) \
                     .limit(pagesize) \
                     .first()

        for row in result:
            comment = {}
            comment['link'] = row.news_id
            comment['content'] = row.content
            comment['written_time'] = row.written_time
            comment['crawl_time'] = row.crawl_time

            data.appen(comment)

        session.close()
        return data
