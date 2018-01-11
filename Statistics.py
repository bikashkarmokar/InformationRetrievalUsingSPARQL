#statistics

import urllib2
from datetime import datetime
from SPARQLWrapper import SPARQLWrapper, JSON, XML, N3, RDF

# sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql = SPARQLWrapper("http://query.wikidata.org/sparql")

sparql.setQuery("""


prefix dbo: <http://dbpedia.org/ontology/>
prefix dbp: <http://dbpedia.org/property/>
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
prefix umbel: <http://umbel.org/umbel/rc/Actor> 
prefix owl:  <http://www.w3.org/2002/07/owl#>


select ?totalActor ?totalActorDb ?totalActorDbWiki ?totalActorMusician ?myocardialDeathNumber 
where 
{
  {
      select distinct (count(?actor) as ?totalActor) 
      where
      {
        ?actor wdt:P106 wd:Q33999 . 
      }
  }
  
  {
       select distinct (count(?actordb) as ?totalActorDb)
       where 
       {  
         service <http://dbpedia.org/sparql> 
         {
           ?actordb rdf:type <http://umbel.org/umbel/rc/Actor> .
           ?actordb rdfs:label ?actorName .  filter(langMatches(lang(?actorName),"en")) . 
   
         }   
  
       }
  }
  {
       select (count(distinct ?actor) as ?totalActorDbWiki)
       where 
       {  
         service <http://dbpedia.org/sparql> 
         {
           ?actor rdf:type <http://umbel.org/umbel/rc/Actor> . #<http://umbel.org/umbel/rc/Actor> . #dbo:Actor . 
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
   
         }   
  
       }
  }
  
  {
      select distinct (count(?actorMusician) as ?totalActorMusician)  
      where 
      {
        ?actorMusician wdt:P106 wd:Q33999 .
        ?actorMusician wdt:P1953 ?discogsId  	  
      }
  }
  
  {
       select distinct (count(?myocardialDeath) as ?myocardialDeathNumber)
       where
       {
         ?myocardialDeath wdt:P509 wd:Q12152 . 
       }
  }
  


      
}    


""")

sparql.setReturnFormat(JSON)
results = sparql.query().convert()

# Create HTML output


with open('statistics.html', 'w') as myFile:
    myFile.write('<html>')
    myFile.write('<head>')
    myFile.write('<link rel="stylesheet" href="stylesheet.css">')
    myFile.write('</head>')
    myFile.write('<body>')

    # myFile.write('<table border="1">')
    myFile.write('<table>')

    myFile.write('<tr>')
    myFile.write(
        '<td colspan="8" style="background-color:gray;text-align:center;padding:2px;"><h1>KESW Home Project</h1>'
        '</br><h4>Bikash Chandra Karmokar</h4></td>')
    myFile.write('</tr>')

    myFile.write('<tr>')
    myFile.write('<td colspan="3" style="background-color:gray;text-align:center;padding:2px;">My observations from both dbpedia and wikidata</td>')
    myFile.write('</tr>')

    myFile.write('<tr>')

    myFile.write('<td class=tableheader>Obsevations</td>')
    myFile.write('<td class=tableheader> Counts</td>')
    myFile.write('<td class=tableheader>Data Source</td>')


    myFile.write('</tr>')

    for result in results["results"]["bindings"]:
        if ("totalActor" in result):
            totalActor = result["totalActor"]["value"].encode('ascii', 'ignore')
        else:
            totalActor = ' '
        if ("totalActorDb" in result):
            totalActorDb = result["totalActorDb"]["value"].encode('ascii', 'ignore')
        else:
            totalActorDb = ' '
        if ("totalActorDbWiki" in result):
            totalActorDbWiki = result["totalActorDbWiki"]["value"].encode('ascii', 'ignore')
        else:
            totalActorDbWiki = ' '
        if ("totalActorMusician" in result):
            totalActorMusician = result["totalActorMusician"]["value"].encode('ascii', 'ignore')
        else:
            totalActorMusician = ' '
        if ("myocardialDeathNumber" in result):
            myocardialDeathNumber = result["myocardialDeathNumber"]["value"].encode('ascii', 'ignore')
        else:
            myocardialDeathNumber = ' '


    myFile.write('<tr>')
    myFile.write('<td>Total wikidata actors</td>')
    myFile.write('<td>%s</td>' % (totalActor))
    myFile.write('<td>Wikidata</td>')
    myFile.write('</tr>')


    myFile.write('<tr>')
    myFile.write('<td>Total dbpedia actors</td>')
    myFile.write('<td>%s</td>' % (totalActorDb))
    myFile.write('<td>Dbpedia</td>')

    myFile.write('</tr>')

    myFile.write('<tr>')
    myFile.write('<td>Total actors both from Dbpedia and Wikidata</td>')
    myFile.write('<td>%s</td>' % (totalActorDbWiki))
    myFile.write('<td>Dbpedia and Wikidata</td>')
    myFile.write('</tr>')

    myFile.write('<tr>')
    myFile.write('<td>Total actors who are also musician</td>')
    myFile.write('<td>%s</td>' % (totalActorMusician))
    myFile.write('<td>Wikidata</td>')
    myFile.write('</tr>')

    myFile.write('<tr>')
    myFile.write('<td>Myocardial Infarction is the most frequent cause of death and </br> total dead people</td>')
    myFile.write('<td>%s</td>' % (myocardialDeathNumber))
    myFile.write('<td>Wikidata</td>')
    myFile.write('</tr>')

    myFile.write('</table >')
    myFile.write('</body>')
    myFile.write('</html>')

    print '\nPlease check the statistics.html file in the project folder for the result.'