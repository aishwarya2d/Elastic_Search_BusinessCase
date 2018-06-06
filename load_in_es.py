import json
import elasticsearch
es = elasticsearch.Elasticsearch()  # use default of localhost, port 9200
id = 1

with open('alldoctors.json') as json_file:
    for line in json_file:
	    data = json.loads(line)
	    print data
	    es.index(index='doctors', doc_type='doctor', id=id, body=data)
	    id = id +1