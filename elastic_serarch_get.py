import json
import elasticsearch
es = elasticsearch.Elasticsearch()  # use default of localhost, port 9200

doc1= es.get(index='doctors', doc_type='doctor', id=1)
print doc1

doc1= es.get(index='doctors', doc_type='doctor', id=2)
print doc1