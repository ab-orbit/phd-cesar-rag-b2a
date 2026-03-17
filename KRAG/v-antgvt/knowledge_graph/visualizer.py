import pyvis
from pyvis.network import Network
from .federator import FederadorOntologias, KGMETA, URIRef

class VisualizadorKG:
    """
    Gera representações HTML para o grafo usando PyVis.
    """

    CORES_STATUS = {
        str(KGMETA.Confirmado): "#4CAF50",   # Verde
        str(KGMETA.Candidato):  "#FF9800",   # Laranja
        str(KGMETA.Aprovado):   "#2196F3",   # Azul
        str(KGMETA.Rejeitado):  "#9E9E9E",   # Cinza
    }

    CORES_DEFAULT = "#FAFAFA"

    def __init__(self, federador: FederadorOntologias):
        self.federador = federador

    def gerar_html_interativo(self, caminho_saida: str = "kg_viz.html"):
        """Consulta iterativa via rdflib local para gerar PyVis Network."""
        
        net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white", directed=True)
        
        if not self.federador.use_local_rdflib:
            print("Visualização apenas para base in-memory implementada.")
            return

        # Pega todas as triplas pra renderizar
        query = """
        SELECT ?s ?s_label ?s_status ?p ?o ?o_label ?o_status WHERE {
            ?s ?p ?o .
            OPTIONAL { ?s rdfs:label ?s_label }
            OPTIONAL { ?s kgmeta:status ?s_status }
            OPTIONAL { ?o rdfs:label ?o_label }
            OPTIONAL { ?o kgmeta:status ?o_status }
        } LIMIT 200
        """

        res = self.federador.consultar(query)
        nodes_added = set()

        for row in res:
            s_str = str(row.s)
            p_str = str(row.p).split('#')[-1].split('/')[-1]
            o_str = str(row.o)

            # Node 1
            if s_str not in nodes_added:
                s_lbl = str(row.s_label) if row.s_label else s_str.split('#')[-1]
                s_color = self.CORES_STATUS.get(str(row.s_status), self.CORES_DEFAULT)
                net.add_node(s_str, label=s_lbl, color=s_color, title=s_str)
                nodes_added.add(s_str)

            # Node 2
            if hasattr(row.o, 'datatype') or hasattr(row.o, 'language'): # Literal check
                pass # Só faz nodes para URIs visuais ou restringe literals
            elif o_str not in nodes_added:
                o_lbl = str(row.o_label) if row.o_label else o_str.split('#')[-1]
                o_color = self.CORES_STATUS.get(str(row.o_status), self.CORES_DEFAULT)
                net.add_node(o_str, label=o_lbl, color=o_color, title=o_str)
                nodes_added.add(o_str)

            # Edge
            if not (hasattr(row.o, 'datatype') or hasattr(row.o, 'language')):
                net.add_edge(s_str, o_str, title=p_str, label=p_str)

        try:
            net.save_graph(caminho_saida)
            print(f"Grafo visual salvo em {caminho_saida}")
        except Exception as e:
            print(f"Falha ao salvar a visão interativa: {e}")
