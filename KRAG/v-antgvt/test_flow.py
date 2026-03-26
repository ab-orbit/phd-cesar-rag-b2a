import os
from knowledge_graph.federator import FederadorOntologias
from knowledge_graph.ingester import IngesterMarkdown
from knowledge_graph.detector import DetectorEntidadesNovas
from knowledge_graph.visualizer import VisualizadorKG

os.environ["OPENAI_API_KEY"] = ""

f = FederadorOntologias(use_local_rdflib=True, base_dir='.')
f.carregar_todos_os_grafos()

ingester = IngesterMarkdown("dados_exemplo/apl_textil_pe_parte1.md", base_dir='.')
chunks = ingester.carregar_chunks()
triplas = []
for chunk in chunks:
    try:
        ts = ingester.extrair_triplas(chunk)
        triplas.extend(ts)
    except Exception as e:
        print("Erro", e)

triplas_mapeadas = [ingester.mapear_para_ontologia(t) for t in triplas]
f.inserir_triplas(triplas_mapeadas)

d = DetectorEntidadesNovas(f)
d.identificar_e_marcar(triplas_mapeadas)
print(d.gerar_relatorio_candidatos())

query = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX kgmeta: <http://phd-cesar-rag/meta#>

SELECT ?s ?s_label ?s_status ?p ?o ?o_label ?o_status WHERE {
    ?s kgmeta:status ?s_status .
    ?s ?p ?o .
    ?o kgmeta:status ?o_status .
    FILTER (?p NOT IN (rdf:type, rdfs:label, rdfs:comment, rdfs:domain, rdfs:range, kgmeta:status))
}
"""
res = list(f.consultar(query))
print("Results inst:", len(res))
for r in res:
    print(r)
