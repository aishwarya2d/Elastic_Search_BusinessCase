import elasticsearch

print("Elastic search1")
es = elasticsearch.Elasticsearch()  # use default of localhost, port 9200

print "\nTotal number of doctors by city"
citybody={
 "size": 0,
 "aggs": {
    "group_by": {
      "terms": {
        "field": "city_name.keyword"      
        }
    }
  }
}

req = es.search(index="doctors", body=citybody)
dict_city = req['aggregations']['group_by']['buckets']
for key in dict_city:
    print key['key'], key['doc_count']

print "\nTotal number of doctors by Specialities"
specialitiesbody={
 "size": 0,
 "aggs": {
    "group_by": {
      "terms": {
        "field": "speciality_name.keyword"      
        }
    }
  }
}
req={}
req = es.search(index="doctors", body=specialitiesbody)
dict_speciality = req['aggregations']['group_by']['buckets']
for key in dict_speciality:
    print key['key'], key['doc_count']

print "\nTotal number of doctors by Experience"
experiencebody={
 "size": 0,
 "aggs": {
    "group_byexperience": {
        "range":{
            "field":"years_in_practise",
            "ranges":[
               { 
                   "from":0,
                    "to":4
               },
               { 
                   "from":5,
                    "to":10
               },
               { 
                   "from":10,
                    "to":20
               },
               { 
                   "from":20
               }
            ]

        }      
        }
    }
  }

req={}
req = es.search(index="doctors", body=experiencebody)
dict_exp = req['aggregations']['group_byexperience']['buckets']
for key in dict_exp:
    print key['key'],':', key['doc_count']

print "\nTotal number of doctors by Zipcode"
zipbody={
 "size": 0,
 "aggs": {
    "group_by": {
      "terms": {
        "field": "zipcode.keyword"      
        }
    }
  }
}
req = es.search(index="doctors", body=zipbody)
dict_zipcode = req['aggregations']['group_by']['buckets']
for key in dict_zipcode:
    print key['key'],':', key['doc_count']