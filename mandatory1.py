#Retrieve all actors who died since 1950 according to DBpedia

import urllib2
from datetime import datetime
from SPARQLWrapper import SPARQLWrapper, JSON, XML, N3, RDF

#sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql = SPARQLWrapper("http://query.wikidata.org/sparql")

sparql.setQuery("""
#Retrieve all actors who died since 1950 according to DBpedia 

#query 
prefix dbo: <http://dbpedia.org/ontology/>
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
prefix umbel: <http://umbel.org/umbel/rc/Actor> 
prefix dbp: <http://dbpedia.org/property/>

prefix owl:  <http://www.w3.org/2002/07/owl#>
#prefix hint: <http://www.bigdata.com/queryHints#>

select distinct 
?actor ?actorName ?actorBirthDate ?actorBirthPlace 
?actorDeathDate ?actorDeathCause ?starred  ?wikiActor 
#?awardName  

where 
{ 

  
  service <http://dbpedia.org/sparql> 
  {
    ?actor rdf:type dbo:Actor . #<http://umbel.org/umbel/rc/Actor> . #dbo:Actor . 
    ?actor rdfs:label ?actorName .  filter(langMatches(lang(?actorName),"en")) .   
    ?actor dbo:birthDate ?actorBirthDate . filter(langMatches(lang(?actorName),"en")) . 
    ?actor dbo:birthPlace ?actorBirthPlacelink . 
    ?actorBirthPlacelink rdfs:label ?actorBirthPlace .  filter(langMatches(lang(?actorBirthPlace),"en")) .
    ?actor dbo:deathDate ?actorDeathDate . filter(?actorDeathDate > "1949-12-12"^^xsd:date) .
    ?actor dbp:deathCause ?actorDeathCauselink .   
    ?actorDeathCauselink rdfs:label ?actorDeathCause .  filter(langMatches(lang(?actorDeathCause),"en")) .
    ?starredlink dbo:starring ?actor .  
    ?starredlink rdfs:label ?starred .  filter(langMatches(lang(?starred),"en")) .   
    ?actor owl:sameAs ?wikiActor .
    filter strstarts(str(?wikiActor), "http://www.wikidata.org") .    
    
    #?wikiActor wdt:P166 ?awardName
  } 


     
}order by asc(?actorDeathDate) #desc(?actorDeathDate) 


""")


sparql.setReturnFormat(JSON)
results = sparql.query().convert()

# Create HTML output
print '<html><head><title>Actors who died since 1950 according to DBpedia</title></head>'


print '<ul>'

for result in results["results"]["bindings"]:
	if ("actor" in result):
	    #Create Wikipedia Link
  		url = result["actor"]["value"].encode('ascii', 'ignore')
	else:
		url = 'NONE'
	if ("actorName" in result):
		actorName = result["actorName"]["value"].encode('ascii', 'ignore')
	else:
		actorName = 'NONE'
	if ("actorBirthDate" in result):
		actorBirthDate = result["actorBirthDate"]["value"].encode('ascii', 'ignore')
	else:
		actorBirthDate = 'NONE'
	if ("actorBirthPlace" in result):
		actorBirthPlace = result["actorBirthPlace"]["value"].encode('ascii', 'ignore')
	else:
		actorBirthPlace = ' '
	if ("actorDeathDate" in result):
		actorDeathDate = result["actorDeathDate"]["value"].encode('ascii', 'ignore')
	else:
		actorDeathDate = ' '
	if ("actorDeathCause" in result):
		actorDeathCause = result["actorDeathCause"]["value"].encode('ascii', 'ignore')
	else:
		actorDeathCause = ' '
	if ("starred" in result):
		starred = result["starred"]["value"].encode('ascii', 'ignore')
	else:
		starred = ' '
	if ("wikiActor" in result):
		wikiActor = result["wikiActor"]["value"].encode('ascii', 'ignore')
	else:
		wikiActor = ' '


	print url, actorName, actorBirthDate, actorBirthPlace, actorDeathDate, actorDeathCause, starred, wikiActor

print '</ul>'
print '</body></html>'
