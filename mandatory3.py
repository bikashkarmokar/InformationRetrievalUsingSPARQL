#Retrieve from WikiData for each some additional information which is not present in
#DBpedia: awards received, IMDB ID (if available), Discogs ID (if available and
#assuming the actor is a musician as well)


import urllib2
from datetime import datetime
from SPARQLWrapper import SPARQLWrapper, JSON, XML, N3, RDF

# sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql = SPARQLWrapper("http://query.wikidata.org/sparql")

sparql.setQuery("""

#prefix hint: <http://www.bigdata.com/queryHints#>
#prefix xs: <http://www.w3.org/2001/XMLSchema#>

select ?actor ?actorLabel ?awardLabel ?imdb 
       ?birthDate ?deathDate ?birthPlaceLabel
       ?deathCauseLabel ?discogsId 
#?starredFilmLabel

where 
{              
       ?actor wdt:P106 wd:Q33999 .
       ?actor wdt:P166 ?award . 
       ?actor wdt:P345 ?imdb .
       ?actor wdt:P569 ?birthDate .
  	   ?actor wdt:P570 ?deathDate . filter (?deathDate > "1949-12-12T00:00:00Z"^^xsd:dateTime) .
       ?actor wdt:P19 ?birthPlace .
       ?actor wdt:P509 ?deathCause .    
       optional { ?actor wdt:P1953 ?discogsId  }
  
         
service wikibase:label { bd:serviceParam wikibase:language "en" . }
  
} order by asc (?deathDate) #DESC (?deathDate)


""")


sparql.setReturnFormat(JSON)
results = sparql.query().convert()

# Create HTML output
print '<html><head><title>Addition to actor information from wikidata</title></head>'


print '<ul>'

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
    if ("awardLabel" in result):
        awardLabel = result["awardLabel"]["value"].encode('ascii', 'ignore')
    else:
        awardLabel = 'NONE'
    if ("imdb" in result):
        imdb = result["imdb"]["value"].encode('ascii', 'ignore')
    else:
        imdb = 'NONE'
    if ("birthDate" in result):
        birthDate = result["birthDate"]["value"].encode('ascii', 'ignore')
    else:
        birthDate = 'NONE'
    if ("deathDate" in result):
        deathDate = result["deathDate"]["value"].encode('ascii', 'ignore')
    else:
        deathDate = ' '
    if ("birthPlaceLabel" in result):
        birthPlaceLabel = result["birthPlaceLabel"]["value"].encode('ascii', 'ignore')
    else:
        actorBirthPlace = ' '
    if ("deathCauseLabel" in result):
        deathCauseLabel = result["deathCauseLabel"]["value"].encode('ascii', 'ignore')
    else:
        deathCauseLabel = ' '
    if ("discogsId" in result):
        discogsId = result["discogsId"]["value"].encode('ascii', 'ignore')
    else:
        discogsId = ' '



    print url, actorLabel, awardLabel, imdb, birthDate, deathDate, birthPlaceLabel, deathCauseLabel, discogsId

print '</ul>'
print '</body></html>'
