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
ontology1_graph.parse("/home/citius/onto-evol-llm/epo/v3.1.0/ePO_owl_core_v3.1.0.ttl", format="turtle")
ontology2_graph.parse("/home/citius/onto-evol-llm/epo/v4.0.0/ePO_owl_core_v4.0.0.ttl", format="turtle")

# Print the number of triples in each graph to verify data loading
print(f"Number of triples in ontology1: {len(ontology1_graph)}")
print(f"Number of triples in ontology2: {len(ontology2_graph)}")

# Original query to find new classes in Ontology 2
print("\nNew classes in Ontology 2:")
query = """
PREFIX owl: <http://www.w3.org/2002/07/owl#> 
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 

SELECT ?newclass WHERE { 
  GRAPH <http://example.org/ontology2> { 
    ?newclass a owl:Class . 
  } 
  MINUS { 
    GRAPH <http://example.org/ontology1> { 
      ?newclass a owl:Class . 
    } 
  } 
}
"""

# Execute the query and print the results
for row in dataset.query(query):
    print(f"{row.newclass}")

