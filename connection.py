# -*- coding: utf-8 -*-

import sys
import redis

from sqlalchemy import create_engine
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy.orm import sessionmaker

reload(sys)
sys.setdefaultencoding('utf-8')

server = 'ec2-52-41-252-180.us-west-2.compute.amazonaws.com'


def r(server):
    return redis.Redis(host=server, port=6379)

connection_string = 'mysql+mysqldb://root:windows48@{}:3306/crawl' \
                    .format(server)
engine = create_engine(connection_string, pool_recycle=3600, encoding='utf-8')
Session = sessionmaker(bind=engine)
