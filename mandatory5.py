#Question 5



import urllib2
from datetime import datetime
from SPARQLWrapper import SPARQLWrapper, JSON, XML, N3, RDF

# sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql = SPARQLWrapper("http://query.wikidata.org/sparql")

sparql.setQuery("""

select ?actorLabel ?filmLabel (count(distinct ?award) as ?awardsNumber) 
 where 
{
       ?actor wdt:P106 wd:Q33999 .       
       ?actor wdt:P570 ?deathDate . filter (?deathDate > "1949-12-12T00:00:00Z"^^xsd:dateTime) .
      
       ?film wdt:P31 wd:Q11424 .        
       ?film wdt:P166 ?award . 
       ?film wdt:P161 ?actor . 
      
       service wikibase:label { bd:serviceParam wikibase:language "en" . }
      
}   group by ?actorLabel ?filmLabel
order by desc(?awardsNumber)


""")

sparql.setReturnFormat(JSON)
results = sparql.query().convert()

# Create HTML output
print '<html><head><title>Ranking of actors according to received movie awards</title></head>'

print '<ul>'

rank=0
tmp=0

for result in results["results"]["bindings"]:
    if ("actorLabel" in result):
        actorLabel = result["actorLabel"]["value"].encode('ascii', 'ignore')
    else:
        actorLabel = 'NONE'
    if ("filmLabel" in result):
        filmLabel = result["filmLabel"]["value"].encode('ascii', 'ignore')
    else:
        filmLabel = 'NONE'
    if ("awardsNumber" in result):
        awardsNumber = result["awardsNumber"]["value"].encode('ascii', 'ignore')
    else:
        awardsNumber = 'NONE'

    if (tmp==awardsNumber):
        rank= rank
    else:
        rank=rank+1
        tmp=awardsNumber

    print actorLabel, filmLabel, awardsNumber, rank

print '</ul>'
print '</body></html>'
