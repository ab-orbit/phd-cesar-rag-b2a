from typing import Dict, List, Tuple
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL, SKOS, DC, PROV
import os
from . import KG, KGMETA, E3VALUE, REA, VDML

class FederadorOntologias:
    """
    Carrega múltiplas ontologias para consultas federadas.
    Pode usar rdflib local (memória) ou QLever.
    """

    GRAFOS = {
        "e3value":   ("http://www.e3value.com/graph", "ontologias/e3value_subset.ttl"),
        "rea":       ("http://www.rea.com/graph", "ontologias/rea_subset.ttl"),
        "vdml":      ("http://www.omg.org/spec/VDML/graph", "ontologias/vdml_subset.ttl"),
        "kg":        ("http://phd-cesar-rag/kg", "ontologias/kg_custom.ttl"),
    }

    def __init__(self, endpoint: str = None, use_local_rdflib: bool = True, base_dir: str = "."):
        self.endpoint = endpoint
        self.use_local_rdflib = use_local_rdflib
        self.base_dir = base_dir
        self.local_graph = None

        if self.use_local_rdflib:
            self.local_graph = Graph()
            self._bind_namespaces(self.local_graph)

    def _bind_namespaces(self, g: Graph):
        g.bind("kg", KG)
        g.bind("kgmeta", KGMETA)
        g.bind("e3value", E3VALUE)
        g.bind("rea", REA)
        g.bind("vdml", VDML)
        g.bind("skos", SKOS)
        g.bind("prov", PROV)
        g.bind("dc", DC)

    def carregar_todos_os_grafos(self):
        """Carrega arquivos TTL locais se existirem."""
        if not self.use_local_rdflib:
            print("Federação configurada para endpoint externo. Ignorando carga local.")
            return

        for name, (uri, rel_path) in self.GRAFOS.items():
            # Adjust path to look for ontologias directory relative to this file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            full_path = os.path.join(current_dir, rel_path)
            if os.path.exists(full_path):
                print(f"Carregando {name} de {full_path}")
                try:
                    self.local_graph.parse(full_path, format="turtle")
                except Exception as e:
                    print(f"Erro ao carregar {path}: {e}")
            else:
                print(f"Arquivo não encontrado (ignorando): {full_path}")

    def inserir_triplas(self, triplas_rdf: List[Tuple]):
        """Insere triplas no grafo local ou no endpoint."""
        if self.use_local_rdflib:
            for t in triplas_rdf:
                self.local_graph.add(t)
            print(f"Inseridas {len(triplas_rdf)} triplas no grafo local.")
        else:
            # TODO: Lógica de INSERT via SPARQL Update para o QLever ou outro endpoint
            pass

    def consultar(self, query: str):
        """Executa consulta SPARQL."""
        if self.use_local_rdflib:
            return self.local_graph.query(query)
        else:
            from SPARQLWrapper import SPARQLWrapper, JSON
            sparql = SPARQLWrapper(self.endpoint)
            sparql.setQuery(query)
            sparql.setReturnFormat(JSON)
            return sparql.query().convert()
