from rdflib import Graph, URIRef, ConjunctiveGraph, BNode
from rdflib.plugins.stores.memory import Memory

store = Memory()
# Create a dataset (graph store)
dataset = ConjunctiveGraph(store=store)

# Define the named graph URIs
ontology1_uri = URIRef("http://example.org/ontology1")
ontology2_uri = URIRef("http://example.org/ontology2")

# Create named graphs
ontology1_graph = Graph(store=store, identifier=ontology1_uri)
ontology2_graph = Graph(store=store, identifier=ontology2_uri)

# Load the OWL files into the respective named graphs
ontology1_graph.parse("/home/citius/onto-evol-llm/epo/v3.1.0/ePOv3.1.0.ttl", format="turtle")
ontology2_graph.parse("/home/citius/onto-evol-llm/epo/v4.0.0/ePOv4.0.0.ttl", format="turtle")

# Debugging: Print the number of triples in each graph
print(f"Number of triples in ontology1: {len(ontology1_graph)}")
print(f"Number of triples in ontology2: {len(ontology2_graph)}")

# Original query to find new properties in Ontology 2
print("\nNew properties in Ontology 2:")
query = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
PREFIX owl: <http://www.w3.org/2002/07/owl#> 
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 

SELECT DISTINCT ?property ?class 

WHERE { 
  # Query the second ontology 
  GRAPH <http://example.org/ontology2> { 
    ?property rdf:type ?propertyType . 
    FILTER (?propertyType IN (owl:ObjectProperty, owl:DatatypeProperty)) 
    ?property rdfs:domain ?class . 
  } 
   
  # Check if the property doesn't exist in the first ontology 
  FILTER NOT EXISTS { 
    GRAPH <http://example.org/ontology1> { 
      ?property rdf:type ?propertyType . 
    } 
  } 
} 

ORDER BY ?property 
"""
for row in dataset.query(query):
    print(f"New property: {row.property}, Domain class: {row['class']}")




