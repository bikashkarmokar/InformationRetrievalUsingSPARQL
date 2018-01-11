#Question 4
#Create ranking 1: rank your set of actors according to the amount of awards received
#(descending order).


import urllib2
from datetime import datetime
from SPARQLWrapper import SPARQLWrapper, JSON, XML, N3, RDF

# sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql = SPARQLWrapper("http://query.wikidata.org/sparql")

sparql.setQuery("""

select ?actor ?actorLabel ?awardsNumber where {
{
    select ?actor (count(distinct ?award) as ?awardsNumber) 
    where {
       ?actor wdt:P106 wd:Q33999 .
       ?actor wdt:P166 ?award . 
       ?actor wdt:P570 ?deathDate . filter (?deathDate > "1949-12-12T00:00:00Z"^^xsd:dateTime) .
    }   
    group by ?actor
}         
service wikibase:label { bd:serviceParam wikibase:language "en" . }
}
order by desc(?awardsNumber)


""")

sparql.setReturnFormat(JSON)
results = sparql.query().convert()

# Create HTML output
print '<html><head><title>Ranking of actors according to the amount of awards received</title></head>'

print '<ul>'

rank=0
tmp=0

for result in results["results"]["bindings"]:
    if ("actor" in result):
        # Create Wikipedia Link
        url = result["actor"]["value"].encode('ascii', 'ignore')
    else:
        url = 'NONE'
    if ("actorLabel" in result):
        actorLabel = result["actorLabel"]["value"].encode('ascii', 'ignore')
    else:
        actorLabel = 'NONE'
    if ("awardsNumber" in result):
        awardsNumber = result["awardsNumber"]["value"].encode('ascii', 'ignore')
    else:
        awardsNumber = 'NONE'

    if (tmp==awardsNumber):
        rank= rank
    else:
        rank=rank+1
        tmp=awardsNumber

    print url, actorLabel, awardsNumber, rank

print '</ul>'
print '</body></html>'
