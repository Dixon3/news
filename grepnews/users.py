from elasticsearch import Elasticsearch

es = Elasticsearch()


class User(object):

    username =''
    password =''

    def __init__(self,username,password):
       self.username=username
       self.password=password

    def is_authenticated(self):
       
       q= {"query":{"bool":{"must":[{"query_string":{"default_field":"user.username","query":self.username}},
                            {"query_string":{"default_field":"user.password","query":self.password}}]}}}
       print q
       try:
          user = es.search(index='users',doc_type='user',body=q)['hits']['hits'][0]['_source']
          return True
       except Exception:
          print 'User not found!'
          return False 

    def get(self,userid):
        self.username=userid
        return self

    def is_active(self):
       return True
    def is_anonymous(self):
       return False

    def get_id(self):
       """


       :return:
       """
       return self.username