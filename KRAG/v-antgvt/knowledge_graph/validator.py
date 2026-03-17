import json
import os
import datetime
from rdflib import URIRef, Literal, RDF, Graph
from .federator import FederadorOntologias, KG, KGMETA, SKOS, DC, PROV

class ValidadorOntologia:
    """
    Interface de revisão de candidatos e geração de nova versão da ontologia.
    """

    def __init__(self, federador: FederadorOntologias):
        self.federador = federador

    def listar_candidatos(self):
        """Retorna uma lista iterável de todas as entidades marcadas como Candidatas"""
        q = """
        SELECT ?uri ?label WHERE {
            ?uri kgmeta:status kgmeta:Candidato ;
                 rdfs:label ?label .
        }
        """
        return self.federador.consultar(q)

    def aprovar_entidade(self, 
                         uri_candidato: str, 
                         aprovador: str,
                         tipo_ontologico: str = None, 
                         mapeamento_externo: str = None):
        """
        Atualiza kgmeta:status para kgmeta:Aprovado.
        """
        # Excluir a tripla antiga e adicionar a nova no backend escolhido
        # Em local in-memory:
        if self.federador.use_local_rdflib:
            uri = URIRef(uri_candidato)
            self.federador.local_graph.remove((uri, KGMETA.status, KGMETA.Candidato))
            self.federador.local_graph.add((uri, KGMETA.status, KGMETA.Aprovado))
            self.federador.local_graph.add((uri, PROV.wasAttributedTo, Literal(aprovador)))

            if tipo_ontologico:
                self.federador.local_graph.add((uri, RDF.type, URIRef(tipo_ontologico)))
            
            if mapeamento_externo:
                self.federador.local_graph.add((uri, SKOS.exactMatch, URIRef(mapeamento_externo)))

    def rejeitar_entidade(self, uri_candidato: str, motivo: str):
        """Marca como Rejeitado"""
        if self.federador.use_local_rdflib:
            uri = URIRef(uri_candidato)
            self.federador.local_graph.remove((uri, KGMETA.status, KGMETA.Candidato))
            self.federador.local_graph.add((uri, KGMETA.status, KGMETA.Rejeitado))
            self.federador.local_graph.add((uri, RDFS.comment, Literal(f"Rejeitado: {motivo}")))

    def exportar_nova_versao_ontologia(self, versao: str, caminho_saida: str):
        """
        Exporta apenas as triplas onde existem entidades aprovadas.
        Gera um arquivo .ttl com semver.
        """
        if not self.federador.use_local_rdflib:
            return

        g_export = Graph()
        self.federador._bind_namespaces(g_export)
        
        # Copiando para exportação tudo que não é candidato rejeitado, etc. 
        # (Lógica simplificada para exportar a ontologia KG nova)
        query = f"""
        CONSTRUCT {{
            ?s ?p ?o
        }} WHERE {{
            ?s kgmeta:status kgmeta:Aprovado .
            ?s ?p ?o .
        }}
        """
        nova_ontologia = self.federador.local_graph.query(query)
        for row in nova_ontologia:
            g_export.add(row)
        
        # Adicionando metadados da ontologia
        ontologia_uri = URIRef(f"http://phd-cesar-rag/kg_custom_v{versao}")
        g_export.add((ontologia_uri, RDF.type, PROV.Entity))
        g_export.add((ontologia_uri, dc_date := DC.date, Literal(str(datetime.date.today()))))
        
        # Salvando
        g_export.serialize(destination=caminho_saida, format="turtle")
        print(f"Exportada nova ontologia v{versao} em {caminho_saida}")
