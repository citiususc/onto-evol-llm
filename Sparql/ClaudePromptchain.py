from rdflib import Graph, URIRef
from rdflib.namespace import RDF, RDFS, OWL

def get_classes(file_path):
    g = Graph()
    g.parse(file_path, format="turtle")  # Adjust format if needed (e.g., "turtle" for .ttl files)
    
    classes = set()
    query = """
    SELECT DISTINCT ?class
    WHERE {
      {
        ?class a owl:Class .
      }
      UNION
      {
        ?class rdfs:subClassOf ?superClass .
      }
      FILTER(!isBlank(?class))
    }
    """
    
    for row in g.query(query):
        classes.add(row[0])  # Access the first (and only) item in the row
    
    return classes

# Paths to your ontology files
version1_path = "/home/citius/onto-evol-llm/epo/v3.1.0/ePO_owl_core_v3.1.0.ttl"
version2_path = "/home/citius/onto-evol-llm/epo/v4.0.0/ePO_owl_core_v4.0.0.ttl"

# Get classes from both versions
classes_v1 = get_classes(version1_path)
classes_v2 = get_classes(version2_path)

# Find new classes in version 2
new_classes = classes_v2 - classes_v1

# Find deleted classes (present in version 1 but not in version 2)
deleted_classes = classes_v1 - classes_v2

# Print results
print("New classes in version 2:")
for cls in new_classes:
    print(cls)

print("\nDeleted classes (present in version 1 but not in version 2):")
for cls in deleted_classes:
    print(cls)


