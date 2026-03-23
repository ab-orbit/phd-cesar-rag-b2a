from knowledge_graph.federator import FederadorOntologias
from knowledge_graph.ingester import IngesterMarkdown
from knowledge_graph.detector import DetectorEntidadesNovas
import os

f = FederadorOntologias(use_local_rdflib=True, base_dir='.')
f.carregar_todos_os_grafos()

# simulate triplas
triplas = [
    # Mocking what the ingester would do:
    # (s, p, o)
]
# Let's just run SPARQL directly since the in-memory graph has candidates!
query = """
PREFIX kgmeta: <http://phd-cesar-rag/meta#>
SELECT ?s ?p ?o WHERE {
    ?s kgmeta:status ?s_status .
    ?s ?p ?o .
    ?o kgmeta:status ?o_status .
    FILTER (?p NOT IN (rdf:type, rdfs:label, rdfs:comment, rdfs:domain, rdfs:range, kgmeta:status))
}
"""
