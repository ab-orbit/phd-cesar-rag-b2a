#!/usr/bin/env python
"""
Value Chain Federator - Gerenciador de Knowledge Graph Federado para Cadeias de Valor

Adaptado do FederadorOntologias para contexto organizacional (v-antpc).
Gerencia ontologias de cadeia de valor: e3value, REA, VDML, SCOR.

Autor: César Cunha
Data: 2026-03-16
"""

import os
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL, XSD
from SPARQLWrapper import SPARQLWrapper, JSON, POST, GET
import requests
from requests.auth import HTTPBasicAuth
import json


class ValueChainFederator:
    """
    Gerenciador de Knowledge Graph Federado para Análise de Cadeias de Valor.

    Integra 4 ontologias fundamentais:
    - e3value: Trocas de valor e reciprocidade econômica
    - REA: Recursos, Eventos, Agentes (dualidade econômica)
    - VDML: Capacidades, propostas de valor, métricas
    - SCOR: Processos de supply chain e KPIs

    Utiliza Apache Jena Fuseki como backend RDF/SPARQL.
    """

    def __init__(
        self,
        endpoint: str = "http://localhost:3030/kg",
        user: str = "admin",
        password: str = "admin"
    ):
        """
        Inicializa conexão com Fuseki e define namespaces.

        Args:
            endpoint: URL do dataset Fuseki (padrão: http://localhost:3030/kg)
            user: Usuário para autenticação
            password: Senha para autenticação
        """
        self.endpoint = endpoint
        self.user = user
        self.password = password

        # SPARQL endpoints
        self.sparql = SPARQLWrapper(f"{endpoint}/sparql")
        self.sparql.setHTTPAuth("BASIC")
        self.sparql.setCredentials(user, password)

        self.update_endpoint = f"{endpoint}/update"

        # Namespaces das ontologias de Value Chain
        self.namespaces = {
            'e3': Namespace('http://e3value.com/ontology#'),
            'rea': Namespace('http://www.reo.org/ontology#'),
            'vdml': Namespace('http://www.omg.org/spec/VDML/'),
            'scor': Namespace('http://www.apics.org/scor#'),
            'vc': Namespace('http://valuechain.org/ontology#'),
            'rvcs': Namespace('http://rvcs-framework.org/ontology#'),
            # Namespaces para dados (instâncias)
            'actor': Namespace('http://valuechain.org/data/actor/'),
            'exchange': Namespace('http://valuechain.org/data/exchange/'),
            'port': Namespace('http://valuechain.org/data/port/'),
            'object': Namespace('http://valuechain.org/data/object/'),
            'capability': Namespace('http://valuechain.org/data/capability/'),
            'metric': Namespace('http://valuechain.org/data/metric/'),
            # Namespaces padrão
            'rdf': RDF,
            'rdfs': RDFS,
            'owl': OWL,
            'xsd': XSD
        }

        # Caminho base do projeto
        self.base_path = Path(__file__).parent.parent
        self.ontologies_path = self.base_path / "knowledge_graph" / "ontologies"
        self.data_path = self.base_path / "data"

    def verificar_conexao(self) -> bool:
        """
        Verifica se Fuseki está acessível.

        Returns:
            True se conectado, False caso contrário
        """
        try:
            ping_url = self.endpoint.replace("/kg", "/$/ping")
            response = requests.get(ping_url, timeout=5)

            if response.status_code == 200:
                print(f"✓ Conectado ao Fuseki: {self.endpoint}")
                return True
            else:
                print(f"✗ Fuseki respondeu com status {response.status_code}")
                return False

        except requests.exceptions.RequestException as e:
            print(f"✗ Erro ao conectar ao Fuseki: {e}")
            print(f"  Certifique-se de que o Fuseki está rodando em {self.endpoint}")
            return False

    def carregar_ontologia(self, ontology_name: str, graph_uri: Optional[str] = None) -> bool:
        """
        Carrega uma ontologia específica no Fuseki (named graph).

        Args:
            ontology_name: Nome do arquivo .ttl (ex: 'e3value', 'rea', 'vdml', 'scor')
            graph_uri: URI do named graph (padrão: http://valuechain.org/ontology/{name})

        Returns:
            True se carregado com sucesso
        """
        ontology_file = self.ontologies_path / f"{ontology_name}.ttl"

        if not ontology_file.exists():
            print(f"✗ Ontologia não encontrada: {ontology_file}")
            return False

        # Named graph URI
        if graph_uri is None:
            graph_uri = f"http://valuechain.org/ontology/{ontology_name}"

        try:
            # Ler ontologia
            g = Graph()
            g.parse(ontology_file, format='turtle')

            # Serializar como N-Triples para upload
            data = g.serialize(format='nt')

            # Upload para Fuseki (named graph)
            upload_url = f"{self.endpoint}/data?graph={graph_uri}"

            response = requests.post(
                upload_url,
                data=data,
                headers={'Content-Type': 'application/n-triples'},
                auth=HTTPBasicAuth(self.user, self.password)
            )

            if response.status_code in [200, 201, 204]:
                print(f"✓ Ontologia '{ontology_name}' carregada: {len(g)} triplas no grafo {graph_uri}")
                return True
            else:
                print(f"✗ Erro ao carregar ontologia: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            print(f"✗ Erro ao processar ontologia '{ontology_name}': {e}")
            return False

    def carregar_todas_ontologias(self) -> Dict[str, bool]:
        """
        Carrega todas as 4 ontologias de Value Chain.

        Returns:
            Dicionário com status de cada ontologia
        """
        ontologies = ['e3value', 'rea', 'vdml', 'scor']
        results = {}

        print("\n=== Carregando Ontologias de Value Chain ===\n")

        for ont in ontologies:
            results[ont] = self.carregar_ontologia(ont)

        print("\n=== Resumo do Carregamento ===")
        success = sum(1 for v in results.values() if v)
        print(f"Sucesso: {success}/{len(ontologies)} ontologias")

        return results

    def inserir_triplas(self, triplas: str, graph_uri: str = "http://valuechain.org/data/instances") -> bool:
        """
        Insere triplas RDF no grafo (dados de instância, não ontologia).

        Args:
            triplas: String com triplas em formato Turtle
            graph_uri: URI do named graph para dados

        Returns:
            True se inserido com sucesso
        """
        # Construir query SPARQL INSERT
        prefixes = "\n".join([
            f"PREFIX {prefix}: <{str(ns)}>"
            for prefix, ns in self.namespaces.items()
        ])

        sparql_update = f"""
        {prefixes}

        INSERT DATA {{
            GRAPH <{graph_uri}> {{
                {triplas}
            }}
        }}
        """

        try:
            response = requests.post(
                self.update_endpoint,
                data={'update': sparql_update},
                auth=HTTPBasicAuth(self.user, self.password)
            )

            if response.status_code in [200, 204]:
                print(f"✓ Triplas inseridas no grafo {graph_uri}")
                return True
            else:
                print(f"✗ Erro ao inserir triplas: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            print(f"✗ Erro na inserção: {e}")
            return False

    def consultar(self, query: str, formato: str = 'json') -> Optional[Dict]:
        """
        Executa query SPARQL SELECT.

        Args:
            query: Query SPARQL
            formato: Formato de retorno ('json', 'xml', 'csv')

        Returns:
            Resultados da query ou None em caso de erro
        """
        # Adicionar prefixes automaticamente
        prefixes = "\n".join([
            f"PREFIX {prefix}: <{str(ns)}>"
            for prefix, ns in self.namespaces.items()
        ])

        full_query = f"{prefixes}\n\n{query}"

        try:
            self.sparql.setQuery(full_query)

            if formato == 'json':
                self.sparql.setReturnFormat(JSON)

            results = self.sparql.query().convert()
            return results

        except Exception as e:
            print(f"✗ Erro na consulta SPARQL: {e}")
            return None

    def listar_atores(self) -> List[Dict]:
        """
        Lista todos os atores da rede de valor (e3value + REA).

        Returns:
            Lista de atores com tipo e descrição
        """
        query = """
        SELECT DISTINCT ?ator ?tipo ?descricao
        WHERE {
            GRAPH ?g {
                {
                    ?ator a e3:Actor .
                    ?ator a ?tipo .
                    OPTIONAL { ?ator rdfs:comment ?descricao }
                }
                UNION
                {
                    ?ator a rea:Agent .
                    ?ator a ?tipo .
                    OPTIONAL { ?ator rdfs:comment ?descricao }
                }
                FILTER(?tipo != e3:Actor && ?tipo != rea:Agent && ?tipo != owl:Thing)
            }
        }
        ORDER BY ?ator
        """

        results = self.consultar(query)

        if results and 'results' in results:
            atores = []
            for binding in results['results']['bindings']:
                atores.append({
                    'uri': binding['ator']['value'],
                    'tipo': binding.get('tipo', {}).get('value', 'N/A'),
                    'descricao': binding.get('descricao', {}).get('value', 'N/A')
                })
            return atores

        return []

    def listar_trocas_valor(self) -> List[Dict]:
        """
        Lista todas as trocas de valor (e3:ValueExchange).

        Returns:
            Lista de trocas com atores envolvidos
        """
        query = """
        SELECT ?troca ?provedor ?receptor ?valorObjeto
        WHERE {
            GRAPH ?g {
                ?troca a e3:ValueExchange .
                ?troca e3:connects ?porta1 .
                ?troca e3:connects ?porta2 .

                ?porta1 e3:offers ?valorObjeto .
                ?ator1 e3:has_value_port ?porta1 .

                ?porta2 e3:requests ?valorObjeto .
                ?ator2 e3:has_value_port ?porta2 .

                BIND(?ator1 AS ?provedor)
                BIND(?ator2 AS ?receptor)
            }
        }
        """

        results = self.consultar(query)

        if results and 'results' in results:
            trocas = []
            for binding in results['results']['bindings']:
                trocas.append({
                    'troca': binding['troca']['value'],
                    'provedor': binding['provedor']['value'],
                    'receptor': binding['receptor']['value'],
                    'valor_objeto': binding['valorObjeto']['value']
                })
            return trocas

        return []

    def calcular_lucratividade_ator(self, ator_uri: str) -> Optional[Dict]:
        """
        Calcula lucratividade de um ator (e3value profitability sheet).

        Args:
            ator_uri: URI do ator

        Returns:
            Dicionário com receitas, custos e lucro
        """
        query = f"""
        SELECT
            (SUM(?valorEntrada) AS ?receitaTotal)
            (SUM(?valorSaida) AS ?custoTotal)
        WHERE {{
            GRAPH ?g {{
                {{
                    <{ator_uri}> e3:has_value_port ?portaEntrada .
                    ?portaEntrada e3:direction "in" .
                    ?portaEntrada e3:offers ?objEntrada .
                    ?objEntrada e3:economic_value ?valorEntrada .
                }}
                UNION
                {{
                    <{ator_uri}> e3:has_value_port ?portaSaida .
                    ?portaSaida e3:direction "out" .
                    ?portaSaida e3:offers ?objSaida .
                    ?objSaida e3:economic_value ?valorSaida .
                }}
            }}
        }}
        """

        results = self.consultar(query)

        if results and 'results' in results and len(results['results']['bindings']) > 0:
            binding = results['results']['bindings'][0]
            receita = float(binding.get('receitaTotal', {}).get('value', 0))
            custo = float(binding.get('custoTotal', {}).get('value', 0))
            lucro = receita - custo
            margem = (lucro / receita * 100) if receita > 0 else 0

            return {
                'ator': ator_uri,
                'receita': receita,
                'custo': custo,
                'lucro': lucro,
                'margem_percentual': round(margem, 2)
            }

        return None

    def listar_capacidades(self, apenas_core: bool = False) -> List[Dict]:
        """
        Lista capacidades organizacionais (VDML).

        Args:
            apenas_core: Se True, retorna apenas capacidades core (diferenciadoras)

        Returns:
            Lista de capacidades
        """
        filter_core = "FILTER(?isCore = true)" if apenas_core else ""

        query = f"""
        SELECT ?capacidade ?descricao ?nivel ?isCore
        WHERE {{
            GRAPH ?g {{
                ?capacidade a vdml:Capability .
                OPTIONAL {{ ?capacidade rdfs:comment ?descricao }}
                OPTIONAL {{ ?capacidade vdml:capability_level ?nivel }}
                OPTIONAL {{ ?capacidade vdml:is_core ?isCore }}
            }}
        }}
        {filter_core}
        ORDER BY DESC(?isCore) ?capacidade
        """

        results = self.consultar(query)

        if results and 'results' in results:
            capacidades = []
            for binding in results['results']['bindings']:
                capacidades.append({
                    'uri': binding['capacidade']['value'],
                    'descricao': binding.get('descricao', {}).get('value', 'N/A'),
                    'nivel': binding.get('nivel', {}).get('value', 'N/A'),
                    'is_core': binding.get('isCore', {}).get('value', 'false')
                })
            return capacidades

        return []

    def listar_metricas_scor(self) -> List[Dict]:
        """
        Lista métricas SCOR e seus valores atuais.

        Returns:
            Lista de métricas com valores
        """
        query = """
        SELECT ?metrica ?unidade ?valorAtual ?valorAlvo
        WHERE {
            GRAPH ?g {
                ?metrica a scor:Metric .
                OPTIONAL { ?metrica scor:metric_unit ?unidade }
                OPTIONAL { ?metrica scor:actual_value ?valorAtual }
                OPTIONAL { ?metrica scor:target_value ?valorAlvo }
            }
        }
        ORDER BY ?metrica
        """

        results = self.consultar(query)

        if results and 'results' in results:
            metricas = []
            for binding in results['results']['bindings']:
                metricas.append({
                    'metrica': binding['metrica']['value'],
                    'unidade': binding.get('unidade', {}).get('value', 'N/A'),
                    'valor_atual': binding.get('valorAtual', {}).get('value', 'N/A'),
                    'valor_alvo': binding.get('valorAlvo', {}).get('value', 'N/A')
                })
            return metricas

        return []

    def analisar_dualidade_rea(self) -> List[Dict]:
        """
        Verifica dualidade econômica REA (todo incremento tem decremento dual).

        Returns:
            Lista de pares de eventos duais
        """
        query = """
        SELECT ?eventoIncremento ?eventoDecremento ?recurso ?quantidade
        WHERE {
            GRAPH ?g {
                ?eventoIncremento a rea:IncrementEvent .
                ?eventoDecremento a rea:DecrementEvent .

                ?eventoIncremento rea:duality ?eventoDecremento .

                ?eventoIncremento rea:increments ?recurso .
                ?eventoDecremento rea:decrements ?recurso .

                OPTIONAL { ?eventoIncremento rea:quantity ?quantidade }
            }
        }
        """

        results = self.consultar(query)

        if results and 'results' in results:
            pares = []
            for binding in results['results']['bindings']:
                pares.append({
                    'incremento': binding['eventoIncremento']['value'],
                    'decremento': binding['eventoDecremento']['value'],
                    'recurso': binding['recurso']['value'],
                    'quantidade': binding.get('quantidade', {}).get('value', 'N/A')
                })
            return pares

        return []

    def estatisticas_grafo(self) -> Dict:
        """
        Retorna estatísticas gerais do knowledge graph.

        IMPORTANTE: Busca em TODOS os named graphs, não apenas no default graph.
        As ontologias são carregadas em grafos nomeados, então é necessário
        usar GRAPH ?g { ... } para acessá-las.

        Returns:
            Dicionário com contagens de triplas, classes, etc.
        """
        # Queries modificadas para buscar em TODOS os named graphs
        query_triplas = "SELECT (COUNT(*) AS ?total) WHERE { GRAPH ?g { ?s ?p ?o } }"
        query_classes = "SELECT (COUNT(DISTINCT ?classe) AS ?total) WHERE { GRAPH ?g { ?s a ?classe } }"
        query_atores = """
            PREFIX e3: <http://e3value.com/ontology#>
            SELECT (COUNT(DISTINCT ?ator) AS ?total) WHERE { GRAPH ?g { ?ator a e3:Actor } }
        """
        query_capacidades = """
            PREFIX vdml: <http://www.omg.org/spec/VDML/>
            SELECT (COUNT(DISTINCT ?cap) AS ?total) WHERE { GRAPH ?g { ?cap a vdml:Capability } }
        """

        stats = {}

        # Total de triplas
        r = self.consultar(query_triplas)
        if r and 'results' in r and len(r['results']['bindings']) > 0:
            stats['total_triplas'] = int(r['results']['bindings'][0]['total']['value'])

        # Total de classes
        r = self.consultar(query_classes)
        if r and 'results' in r and len(r['results']['bindings']) > 0:
            stats['total_classes'] = int(r['results']['bindings'][0]['total']['value'])

        # Total de atores
        r = self.consultar(query_atores)
        if r and 'results' in r and len(r['results']['bindings']) > 0:
            stats['total_atores'] = int(r['results']['bindings'][0]['total']['value'])

        # Total de capacidades
        r = self.consultar(query_capacidades)
        if r and 'results' in r and len(r['results']['bindings']) > 0:
            stats['total_capacidades'] = int(r['results']['bindings'][0]['total']['value'])

        return stats

    def limpar_grafo(self, graph_uri: Optional[str] = None) -> bool:
        """
        Remove todos os dados de um grafo específico ou de todos.

        Args:
            graph_uri: URI do grafo a limpar (None = limpa todos)

        Returns:
            True se limpeza bem-sucedida
        """
        if graph_uri:
            sparql_update = f"CLEAR GRAPH <{graph_uri}>"
        else:
            sparql_update = "CLEAR ALL"

        try:
            response = requests.post(
                self.update_endpoint,
                data={'update': sparql_update},
                auth=HTTPBasicAuth(self.user, self.password)
            )

            if response.status_code in [200, 204]:
                print(f"✓ Grafo limpo: {graph_uri if graph_uri else 'TODOS'}")
                return True
            else:
                print(f"✗ Erro ao limpar grafo: {response.status_code}")
                return False

        except Exception as e:
            print(f"✗ Erro: {e}")
            return False


# Exemplo de uso
if __name__ == "__main__":
    print("=== Value Chain Federator - Knowledge Graph para Cadeias de Valor ===\n")

    # Inicializar
    federator = ValueChainFederator()

    # Verificar conexão
    if not federator.verificar_conexao():
        print("\n❌ Fuseki não está acessível. Execute:")
        print("   docker run -d --name fuseki -p 3030:3030 -e ADMIN_PASSWORD=admin stain/jena-fuseki")
        exit(1)

    # Carregar ontologias
    federator.carregar_todas_ontologias()

    # Mostrar estatísticas
    print("\n=== Estatísticas do Grafo ===")
    stats = federator.estatisticas_grafo()
    for key, value in stats.items():
        print(f"{key}: {value}")
