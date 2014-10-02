import time
import feedparser
import json
import feedparser
from  elasticsearch import Elasticsearch
d=feedparser.parse('http://lenta.ru/rss/news')
es=Elasticsearch('http://localhost:9200')

class FeedEncoder(json.JSONEncoder):
    def default(self,obj):
        if isinstance (obj,time.struct_time):
            return time.mktime(obj)
        return json.JSONEncoder.default(self.obj)

fe=FeedEncoder()

for i in d['entries']:
    es.index(index="test-feed",doc_type="feed",body=fe.encode(i))