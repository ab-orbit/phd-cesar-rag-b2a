import pandas as pd
from typing import List, Tuple
from rdflib import URIRef, Literal, RDF, RDFS
from .federator import FederadorOntologias, KG, KGMETA

class DetectorEntidadesNovas:
    """
    Identifica se entidades existem na ontologia; caso não,
    são marcadas como 'candidatas'
    """

    def __init__(self, federador: FederadorOntologias):
        self.federador = federador

    def identificar_e_marcar(self, triplas: List[Tuple]) -> List[Tuple]:
        """
        No exemplo curado, marcamos todas as novas URIs derivadas 
        do ingester como candidatas se não existirem no grafo.
        """
        triplas_resultado = []
        for s, p, o in triplas:
            self._marcar_candidato(s)
            self._marcar_candidato(o)
            triplas_resultado.append((s, p, o))
        return triplas_resultado

    def _marcar_candidato(self, uri: URIRef):
        """
        Verifica se a URI existe no grafo como rdfs:label. Se não, marca como candidato.
        """
        # Consulta simples usando rdflib para verificar se o nó já está definido
        if self.federador.use_local_rdflib:
            # Verifica se o nó já está definido formalmente na ontologia (tem rdf:type ou rdfs:label provindo da base)
            # Ignora as próprias marcações temporárias de kg:EntidadeCandidata
            q = f"""
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX kg: <http://phd-cesar-rag/kg#>
            ASK {{
                <{uri}> rdf:type ?type .
                FILTER(?type != kg:EntidadeCandidata)
            }}
            """
            res = self.federador.consultar(q)
            for r in res:
                if not r: # Se não encontrou tipo formal, é novo candidato
                    nome = str(uri).split('#')[-1].replace("_", " ")
                    self.federador.inserir_triplas([
                        (uri, RDF.type, KG.EntidadeCandidata),
                        (uri, RDFS.label, Literal(nome, lang="pt")),
                        (uri, KGMETA.status, KGMETA.Candidato)
                    ])

    def gerar_relatorio_candidatos(self) -> pd.DataFrame:
        """
        Retorna DF com os candidatos no grafo local.
        """
        if self.federador.use_local_rdflib:
            query = """
            SELECT ?entidade ?label WHERE {
                ?entidade kgmeta:status kgmeta:Candidato ;
                          rdfs:label ?label .
            }
            """
            res = self.federador.consultar(query)
            data = []
            for row in res:
                data.append({"uri": str(row.entidade), "nome_entidade": str(row.label)})
            
            return pd.DataFrame(data)
        
        return pd.DataFrame()
