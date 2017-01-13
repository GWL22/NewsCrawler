# -*- coding: utf-8 -*-

import os
import sys

from sqlalchemy.dialects.mysql import INTEGER, BIT, TINYINT, TIME, DOUBLE, TEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, CHAR, Date, String, Time,
Index, DateTime, TIMESTAMP, func


Base = declarative_base()


class News(Base):
    __tablename__ = 'news'

    link            = Column(String(200), primary_key=True, nullable=False)
    title           = Column(String(100), nullable=False)
    content         = Column(TEXT, nullable=False)
    crawl_time      = Column(DateTime, nullable=False)
    comments        = Column(Integer, nullable=False)


class Comment(Base):
    __tablename__ = 'comments'

    id              = Column(String(50), primary_key=True, nullable=False)
    news_id         = Column(String(200), nullable=True)
    content         = Column(TEXT, nullable=True)
    written_time    = Column(DateTime, nullable=True)
    sympathy_count  = Column(Integer, nullable=True, default=0)
    antipathy_count = Column(Integer, nullable=True, default=0)
    crawl_time      = Column(DateTime, nullable=False)
