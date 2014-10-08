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


       q= { "filter" : {         
            "term" : {
                "username" : self.username,
		"password" : self.password, 
                "_cache" : False
            }}}
       print q
       user = es.search(index='users',doc_type='user',body=q)
       print user       
       try:
          user = es.search(index='users',doc_type='user',body=q)['hits']['hits'][0]['_source']
	  print user
          return True
       except Exception:
          print 'User not found!'
          return False 

    def get(self,userid):
        #self.username=userid
        q= {
            "query" : {
            "filtered" : { 
            "query" : {
                "match_all" : {} 
            },
            "filter" : {         
            "term" : {
                "username" : "dixon3@yandex.ru" 
            }}}}}
        print q
        user = es.search(index='users',doc_type='user',body=q)
      ##  result=User(user.username,user.password)
        print "From Get user:",user 
        return None

    def is_active(self):
       return True
    def is_anonymous(self):
       return False
    def get_id(self):
       """

       :return:
       """
       return self.username