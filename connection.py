# -*- coding: utf-8 -*-

import sys
import redis

from sqlalchemy import create_engine
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy.orm import sessionmaker

reload(sys)
sys.setdefaultencoding('utf-8')

server = '# add your server address'


def r(server):
    return redis.Redis(host=server, port=6379)
my_id = '# add your id'
my_pw = '# add your password'
my_port = '# add your port for mysql'
my_schema = "# add your schema's name"

connection_string = 'mysql+mysqldb://{}:{}@{}:{}/{}' \
                    .format(my_id, my_pw, server, my_port, my_schema)
engine = create_engine(connection_string, pool_recycle=3600, encoding='utf-8')
Session = sessionmaker(bind=engine)
