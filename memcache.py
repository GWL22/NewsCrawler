from connection import r


class MemCache(object):
    def __init__(self):
        self.r = r

    def get_crawl_urls(self):
        urls = self.r.lrange('urls', 0, -1)
        return urls

    def cache_news(self, title, content):
        self.r.lpush('recent_titles', title)
        self.r.lpush('recent_contents', content)

        self.r.ltrim('recent_titles', 0, 9)
        self.r.ltrim('recent_contents', 0, 9)

    def get_cached_news(self):
        return zip(self.r.lrange('recent_titles', 0, -1),
                   self.r.lrange('recent_contents', 0, -1))

    def hold_user_key(self, user_id, apikey):
        self.r.hset('id_list', user_id, apikey)

    def auth_user(user_id, apikey):
        if user_id or apikey not in self.r.hget('id_list'):
            return False
        return True
