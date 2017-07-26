from datetime import date
import tornado.escape
import tornado.ioloop
import tornado.web
import json
import elasticsearch.exceptions
from elasticsearch import Elasticsearch
from elasticsearch.helpers import parallel_bulk, scan

class search_es(tornado.web.RequestHandler):
	def get(self):
		query = self.request.arguments["query"]
		#resp=self.request
		#args = json.loads(resp)
		
		res = self.es.search(index='course-index', body={"query": {"multi_match": {"query":    query,
                                                                           "fields": [ "*" ],
                                                                           "type":     "cross_fields",
                                                                            "minimum_should_match": "10%",
                                                                           },
                                                           }})
		print("Got %d Hits:" % res['hits']['total'])
		for hit in res['hits']['hits']:
		  self.write("%(timestamp)s %(author)s: %(text)s" % hit["_source"])
		return	

	@property
	def es(self):

		self.elastic = Elasticsearch('127.0.0.1')

		return self.elastic




application = tornado.web.Application([
    (r"/search", search_es)
])
 
if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

