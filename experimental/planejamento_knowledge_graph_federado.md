# Planejamento: Mecanismo de Knowledge Graph Semântico Federado

**Projeto:** PHD César — RAG com Grafo de Conhecimento Federado
**Data:** 2026-03-15
**Stack:** Python · QLever (RDF/SPARQL) · RDFLib · SPARQLWrapper · LangChain · OpenAI

---

## Visão Geral da Arquitetura

O mecanismo é composto por **cinco subsistemas** que operam em sequência:

```
[Arquivo MD]
     │
     ▼
┌─────────────────┐
│  1. INGESTER    │  Extração de triplas via LLM + mapeamento às ontologias base
└────────┬────────┘
         │  triplas RDF
         ▼
┌─────────────────┐
│  2. FEDERATOR   │  Carrega e federa múltiplas ontologias no QLever
└────────┬────────┘
         │  SPARQL queries
         ▼
┌─────────────────┐
│  3. DETECTOR    │  Identifica entidades/relações fora das ontologias
└────────┬────────┘
         │  candidatos marcados
         ▼
┌─────────────────┐
│  4. VALIDATOR   │  Revisão humana + geração de nova versão da ontologia
└────────┬────────┘
         │  ontologia aprovada
         ▼
┌─────────────────┐
│  5. VISUALIZER  │  Grafo interativo com PyVis / Graphviz
└─────────────────┘
```

---

## Ontologias Federadas Iniciais Sugeridas

O domínio do projeto é **médico-farmacêutico** (dataset AQ-MedAI). As ontologias abaixo são
abertas, disponíveis em RDF/OWL, e coletivamente cobrem os conceitos presentes no corpus.

### Camada 1 — Ontologias de Domínio (Medical/Pharma)

| Ontologia | URI Base | Escopo | Formato | Disponibilidade |
|-----------|----------|--------|---------|-----------------|
| **SNOMED CT** (subconjunto) | `http://snomed.info/id/` | Diagnósticos, procedimentos, anatomia | OWL | Licença gratuita para pesquisa |
| **MeSH RDF** | `http://id.nlm.nih.gov/mesh/` | Indexação biomédica (Pub Med) — doenças, drogas, genes | RDF/Turtle | NLM — totalmente aberto |
| **ChEBI** | `http://purl.obolibrary.org/obo/CHEBI_` | Entidades químicas de interesse biológico (moléculas, drogas) | OWL | EBI — aberto |
| **HPO** (Human Phenotype Ontology) | `http://purl.obolibrary.org/obo/HP_` | Fenótipos clínicos, sintomas | OWL | Open — Monarch Initiative |
| **DRON** (Drug Ontology) | `http://purl.obolibrary.org/obo/DRON_` | Medicamentos, ingredientes, formas farmacêuticas | OWL | OBO Foundry — aberto |

### Camada 2 — Ontologias de Infraestrutura (Transversais)

| Ontologia | URI Base | Escopo |
|-----------|----------|--------|
| **SKOS** | `http://www.w3.org/2004/02/skos/core#` | Organização hierárquica (broader/narrower), mapeamento entre thesauri |
| **PROV-O** | `http://www.w3.org/ns/prov#` | Proveniência dos dados (de onde veio cada tripla, qual arquivo MD originou) |
| **Dublin Core Terms** | `http://purl.org/dc/terms/` | Metadados de documentos (source, creator, date) |
| **OWL / RDFS** | `http://www.w3.org/2002/07/owl#` | Estrutura base de classes, propriedades, hierarquias |
| **Schema.org** | `https://schema.org/` | Entidades gerais (Person, Organization, Dataset, Event) |

### Camada 3 — Namespace Customizado do Projeto

```turtle
@prefix kg:     <http://phd-cesar-rag/kg#> .
@prefix kgmeta: <http://phd-cesar-rag/meta#> .
```

- `kg:` — espaço para entidades do grafo específicas do corpus
- `kgmeta:` — metadados de governança (status, versão, aprovador)

---

## Estrutura de Diretórios do Projeto

```
phd-cesar-rag-b2a/
├── knowledge_graph/
│   ├── __init__.py
│   ├── ontologias/                        # Ontologias locais em Turtle
│   │   ├── mesh_subset.ttl
│   │   ├── chebi_subset.ttl
│   │   ├── hpo_subset.ttl
│   │   ├── dron_subset.ttl
│   │   └── kg_custom.ttl                  # Namespace próprio do projeto
│   ├── ingester.py                        # Fase 1: leitura MD → triplas
│   ├── federator.py                       # Fase 0: carrega ontologias no QLever
│   ├── detector.py                        # Fase 2: identifica candidatos
│   ├── validator.py                       # Fase 2.4: interface de validação
│   ├── visualizer.py                      # Fase 3: renderização do grafo
│   └── sparql_queries/
│       ├── verificar_entidade.sparql
│       ├── listar_candidatos.sparql
│       └── exportar_ontologia.sparql
├── notebooks/
│   └── Tutorial_KG_Federado.ipynb         # Notebook didático principal
└── dados_exemplo/
    └── artigo_medico_exemplo.md           # Arquivo MD de entrada para testes
```

---

## Fase 0 — Criar o Knowledge Graph Semântico Federado

### 0.1 Configurar QLever

```bash
# Via Docker (recomendado para didática)
docker run -p 7001:7001 -v $(pwd)/qlever_data:/data \
    --name qlever-kg adfreiburg/qlever:latest

# Ou via pip (qlever-control)
pip install qlever
qlever setup-config --name kg_federado
qlever index
qlever start
```

### 0.2 Estrutura da Federação

A federação é implementada em dois modelos complementares:

**Modelo A — Federação Local (Ontologias como arquivos RDF carregados no QLever):**
```python
# federator.py
class FederadorOntologias:
    """
    Carrega múltiplas ontologias no mesmo endpoint QLever como
    Named Graphs distintos, permitindo consultas federadas localmente.
    """
    GRAFOS = {
        "mesh":   ("http://id.nlm.nih.gov/mesh/graph", "ontologias/mesh_subset.ttl"),
        "chebi":  ("http://purl.obolibrary.org/obo/chebi", "ontologias/chebi_subset.ttl"),
        "hpo":    ("http://purl.obolibrary.org/obo/hpo",   "ontologias/hpo_subset.ttl"),
        "dron":   ("http://purl.obolibrary.org/obo/dron",  "ontologias/dron_subset.ttl"),
        "kg":     ("http://phd-cesar-rag/kg",              "ontologias/kg_custom.ttl"),
    }
```

**Modelo B — Federação Remota (SERVICE no SPARQL):**
```sparql
# Consulta federada: busca entidade em MeSH remoto + grafo local
SELECT ?entidade ?label WHERE {
    # Grafo local (QLever)
    GRAPH <http://phd-cesar-rag/kg> { ?entidade a kg:Entidade ; rdfs:label ?label }

    # Endpoint remoto MeSH (NLM)
    SERVICE <https://id.nlm.nih.gov/mesh/sparql> {
        ?entidade mesh:concept ?conceito
    }
}
```

### 0.3 Estrutura de um Nó no Grafo

```turtle
# Exemplo: entidade "Ibuprofen" mapeada ao ChEBI
kg:Ibuprofen
    a                    owl:NamedIndividual, chebi:CHEBI_5855 ;
    rdfs:label           "Ibuprofen"@pt, "Ibuprofen"@en ;
    skos:exactMatch      <http://purl.obolibrary.org/obo/CHEBI_5855> ;
    mesh:concept         <http://id.nlm.nih.gov/mesh/D007052> ;
    prov:wasDerivedFrom  kg:Documento_artigo_medico_v1 ;
    dc:source            "artigo_medico_exemplo.md" ;
    kgmeta:status        kgmeta:Confirmado ;
    kgmeta:versaoOntologia "1.0.0" .
```

---

## Fase 1 — Leitura do Arquivo MD e Ingestão

### 1.1 Parser de Markdown

```python
# ingester.py
class IngesterMarkdown:
    """
    Lê um arquivo Markdown, segmenta em chunks contextuais
    e extrai triplas RDF via LLM (estruturado com output_parser).
    """

    def __init__(self, caminho_md: str, ontologias_base: dict):
        self.caminho_md = caminho_md
        self.ontologias_base = ontologias_base  # {nome: grafo_uri}
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)

    def carregar_chunks(self) -> list[str]:
        """Lê MD e segmenta com RecursiveCharacterTextSplitter."""
        ...

    def extrair_triplas(self, chunk: str) -> list[Tripla]:
        """
        Chama LLM com prompt estruturado para extrair:
        (sujeito, predicado, objeto) + tipo_sujeito + tipo_objeto
        Retorna lista de objetos Tripla validados via Pydantic.
        """
        ...

    def mapear_para_ontologia(self, tripla: Tripla) -> TriplamapeadaRDF:
        """
        Para cada entidade extraída, busca via SPARQL se já existe
        em algum dos grafos das ontologias federadas.
        Retorna a URI canônica se encontrada, ou None se candidato novo.
        """
        ...
```

### 1.2 Schema de Extração (Pydantic + LangChain)

```python
from pydantic import BaseModel

class Tripla(BaseModel):
    sujeito: str              # Ex: "Ibuprofen"
    tipo_sujeito: str         # Ex: "Medicamento"
    predicado: str            # Ex: "trata"
    objeto: str               # Ex: "Dor de cabeça"
    tipo_objeto: str          # Ex: "Sintoma"
    trecho_original: str      # Trecho do MD de onde foi extraído (evidência)
    confianca: float          # 0.0-1.0, estimativa do LLM

class ListaTriplas(BaseModel):
    triplas: list[Tripla]
```

### 1.3 Prompt de Extração

```python
PROMPT_EXTRACAO = """
Você é um extrator de conhecimento biomédico. Analise o texto abaixo e extraia
TODAS as relações factuais na forma de triplas (sujeito, predicado, objeto).

REGRAS:
- Use termos médicos padronizados (SNOMED CT, MeSH, ChEBI quando possível)
- Predicados devem ser verbos relacionais: trata, causa, contraindica, interage_com,
  é_subtipo_de, tem_efeito_colateral, é_metabolizado_por, etc.
- Inclua o trecho exato do texto como evidência
- Estime sua confiança de 0.0 a 1.0

TEXTO:
{texto}

Retorne JSON com lista de triplas.
"""
```

---

## Fase 2 — Identificação de Entidades Não Definidas na Ontologia

### 2.1 Detector de Candidatos

```python
# detector.py
class DetectorEntidadesNovas:
    """
    Para cada tripla extraída, verifica via SPARQL se sujeito/objeto
    já existe em algum dos grafos das ontologias federadas.
    Entidades ausentes são marcadas como 'candidatas'.
    """

    QUERY_VERIFICAR_ENTIDADE = """
    SELECT ?uri ?label ?grafo WHERE {
        GRAPH ?grafo {
            ?uri rdfs:label|skos:prefLabel ?label .
            FILTER(LCASE(STR(?label)) = LCASE("%s"))
        }
    } LIMIT 5
    """

    def verificar(self, nome_entidade: str) -> ResultadoVerificacao:
        """
        Retorna: uri_encontrada | None (se candidato)
        """
        ...
```

### 2.2 Marcar Nós Candidatos no Grafo

Entidades novas recebem triplas de metadados explícitas antes de serem inseridas:

```turtle
# Entidade candidata: ainda não confirmada em nenhuma ontologia base
kg:Candidate_SiRNA_Terapeutico
    a                    kg:EntidadeCandidata, owl:NamedIndividual ;
    rdfs:label           "siRNA Terapêutico"@pt ;
    kgmeta:status        kgmeta:Candidato ;          # <<< marcador principal
    kgmeta:revisaoHumana false ;
    kgmeta:origemDado    kg:Documento_artigo_v1 ;
    kgmeta:trechoOrigem  "...terapia com siRNA reduziu expressão..." ;
    kgmeta:dataCriacao   "2026-03-15"^^xsd:date ;
    kgmeta:versaoOntologia "candidato-nao-versionado" .

# Aresta candidata entre entidade conhecida e candidata
kg:Candidate_SiRNA_Terapeutico  kg:trata  mesh:D009103 ;
    kgmeta:statusAresta  kgmeta:CandidatoAresta ;
    kgmeta:revisaoHumana false .
```

**Valores controlados para `kgmeta:status`:**

| Valor | Significado |
|-------|-------------|
| `kgmeta:Confirmado` | Existe em ontologia base — confirmado |
| `kgmeta:Candidato` | Extraído do corpus, aguarda revisão |
| `kgmeta:Aprovado` | Revisado por humano, adicionado à ontologia |
| `kgmeta:Rejeitado` | Revisado e descartado como ruído |

### 2.3 Relatório de Candidatos

```python
# detector.py — método gerar_relatorio_candidatos()
"""
Retorna DataFrame com:
- nome_entidade
- tipo_sugerido
- quantidade_ocorrencias (no corpus)
- exemplos_de_uso (trechos do MD)
- relacoes_sugeridas (predicados e objetos das triplas candidatas)
- confianca_media_llm
"""

QUERY_LISTAR_CANDIDATOS = """
SELECT ?entidade ?label ?trecho ?predicado ?objeto WHERE {
    GRAPH <http://phd-cesar-rag/kg> {
        ?entidade kgmeta:status kgmeta:Candidato ;
                  rdfs:label ?label ;
                  kgmeta:trechoOrigem ?trecho .
        OPTIONAL { ?entidade ?predicado ?objeto }
    }
} ORDER BY ?label
"""
```

Saída exemplo:

```
┌──────────────────────┬──────────────┬──────┬─────────────────────────────────────────┐
│ Entidade Candidata   │ Tipo Sugerido│ Ocor.│ Exemplo de Uso no Corpus                │
├──────────────────────┼──────────────┼──────┼─────────────────────────────────────────┤
│ siRNA Terapêutico    │ Biotecnologia│  3   │ "terapia com siRNA reduziu expressão..." │
│ Nanoemulsão Lipídica │ Farmacotécn. │  2   │ "veiculação via nanoemulsão lipídica..." │
│ CRISPR-Cas9 Ocular   │ Biotecnologia│  1   │ "edição gênica CRISPR para retina..."   │
└──────────────────────┴──────────────┴──────┴─────────────────────────────────────────┘
```

### 2.4 Validação e Geração de Nova Versão da Ontologia

```python
# validator.py
class ValidadorOntologia:
    """
    Interface de revisão de candidatos e geração de nova versão da ontologia.
    Implementa ciclo: Listar → Revisar → Aprovar/Rejeitar → Exportar.
    """

    def listar_candidatos(self) -> pd.DataFrame:
        """Executa SPARQL e retorna tabela de candidatos."""
        ...

    def aprovar_entidade(
        self,
        uri_candidato: str,
        tipo_ontologico: str,           # Ex: "chebi:CHEBI_XXXXX" ou "kg:NovaClasse"
        mapeamento_externo: str | None, # URI em ontologia externa se encontrado
        aprovador: str,
    ) -> None:
        """
        Atualiza kgmeta:status → kgmeta:Aprovado
        Adiciona rdf:type correto e skos:exactMatch se houver mapeamento.
        Registra aprovador e data via PROV-O.
        """
        ...

    def rejeitar_entidade(self, uri_candidato: str, motivo: str) -> None:
        """Marca como kgmeta:Rejeitado com nota explicativa."""
        ...

    def exportar_nova_versao_ontologia(
        self, versao: str, caminho_saida: str
    ) -> None:
        """
        Gera arquivo .ttl com apenas entidades kgmeta:Aprovado,
        incrementando a versão (semver) e registrando changelog
        via dc:description e prov:wasRevisionOf.
        """
        ...
```

**Fluxo de versionamento da ontologia:**

```
kg_custom_v1.0.0.ttl  →  revisão humana de candidatos  →  kg_custom_v1.1.0.ttl
                                                              │
                                                              └─ prov:wasRevisionOf kg_custom_v1.0.0
                                                              └─ dc:date "2026-03-15"
                                                              └─ dc:description "Aprovadas 12 entidades: siRNA..."
```

---

## Fase 3 — Visualização do Knowledge Graph

```python
# visualizer.py
class VisualizadorKG:
    """
    Gera visualização interativa do grafo federado com PyVis.
    Diferencia visualmente entidades por status e ontologia de origem.
    """

    CORES_STATUS = {
        "kgmeta:Confirmado": "#4CAF50",   # Verde — na ontologia base
        "kgmeta:Candidato":  "#FF9800",   # Laranja — aguarda revisão
        "kgmeta:Aprovado":   "#2196F3",   # Azul — aprovado pelo humano
        "kgmeta:Rejeitado":  "#9E9E9E",   # Cinza — descartado
    }

    CORES_ONTOLOGIA = {
        "mesh":  "#E3F2FD",
        "chebi": "#E8F5E9",
        "hpo":   "#FFF3E0",
        "dron":  "#F3E5F5",
        "kg":    "#FAFAFA",
    }

    def gerar_html_interativo(self, caminho_saida: str = "kg_viz.html") -> None:
        """
        Consulta todos os nós/arestas do QLever via SPARQL,
        monta rede PyVis com filtros por status, e exporta HTML interativo.
        """
        ...

    def gerar_subgrafo_entidade(self, uri: str, profundidade: int = 2) -> None:
        """Ego-graph: vizinhança de uma entidade específica."""
        ...
```

---

## Pipeline Completo — Notebook Didático

```python
# Tutorial_KG_Federado.ipynb — Célula principal de orquestração

from knowledge_graph.federator  import FederadorOntologias
from knowledge_graph.ingester   import IngesterMarkdown
from knowledge_graph.detector   import DetectorEntidadesNovas
from knowledge_graph.validator  import ValidadorOntologia
from knowledge_graph.visualizer import VisualizadorKG

# 0. Inicializar federação de ontologias no QLever
federador = FederadorOntologias(endpoint="http://localhost:7001")
federador.carregar_todos_os_grafos()

# 1. Ingerir arquivo MD
ingester = IngesterMarkdown("dados_exemplo/artigo_medico_exemplo.md", federador.grafos)
chunks   = ingester.carregar_chunks()
triplas  = []
for chunk in chunks:
    triplas.extend(ingester.extrair_triplas(chunk))

triplas_mapeadas = [ingester.mapear_para_ontologia(t) for t in triplas]
federador.inserir_triplas(triplas_mapeadas)

# 2. Detectar e marcar candidatos
detector   = DetectorEntidadesNovas(endpoint="http://localhost:7001")
candidatos = detector.identificar_e_marcar(triplas_mapeadas)
relatorio  = detector.gerar_relatorio_candidatos()
print(relatorio.to_markdown())

# 2.4 Validar (loop interativo no notebook)
validador = ValidadorOntologia(endpoint="http://localhost:7001")
for _, candidato in relatorio.iterrows():
    decisao = input(f"Aprovar '{candidato['nome_entidade']}'? [s/n/mapeamento URI]: ")
    if decisao == "s":
        validador.aprovar_entidade(candidato["uri"], tipo_ontologico="kg:NovaClasse",
                                   aprovador="Cesar")
    elif decisao == "n":
        validador.rejeitar_entidade(candidato["uri"], motivo="Ruído/irrelevante")
    else:
        validador.aprovar_entidade(candidato["uri"], mapeamento_externo=decisao,
                                   aprovador="Cesar")

validador.exportar_nova_versao_ontologia(versao="1.1.0", caminho_saida="ontologias/kg_custom_v1.1.0.ttl")

# 3. Visualizar
viz = VisualizadorKG(endpoint="http://localhost:7001")
viz.gerar_html_interativo("kg_viz.html")
print("Visualização disponível em: kg_viz.html")
```

---

## Dependências Python

```bash
pip install \
    rdflib \                    # Manipulação de grafos RDF em Python
    SPARQLWrapper \             # Cliente SPARQL para QLever
    langchain langchain-openai \# Extração de triplas via LLM
    pydantic \                  # Validação de triplas extraídas
    pyvis \                     # Visualização interativa do grafo
    pandas \                    # Relatório de candidatos
    python-dotenv               # Variáveis de ambiente
```

---

## Considerações Pedagógicas e Pontos de Melhoria para Produção

| Aspecto | Implementação Didática (Este Projeto) | Em Produção |
|---------|--------------------------------------|-------------|
| **Volume** | Subconjuntos curados das ontologias (~10k triplas) | Ontologias completas (SNOMED CT: 350k+ conceitos) |
| **QLever** | Docker local, single-node | Cluster distribuído, persistência em volume |
| **Extração** | LLM (GPT-4o-mini) por chunk | NER especializado (BioBERT, PubMedBERT) + LLM para relações |
| **Validação** | Loop interativo no notebook | Interface web (Streamlit/FastAPI) com fluxo de aprovação por equipe |
| **Versionamento** | Arquivo .ttl manual com semver | Sistema de ontologia versionado (Git-like, ex: ontology-git) |
| **Federação** | Named Graphs locais no QLever | SERVICE SPARQL apontando para endpoints externos (NLM, EBI) |
| **Confiança** | Score simples do LLM | Score de confiança calibrado + threshold de aprovação automática |

---

## Roadmap de Implementação

- [ ] **Sprint 1:** Configurar QLever + carregar subconjunto MeSH e ChEBI
- [ ] **Sprint 2:** Implementar `IngesterMarkdown` com extração de triplas via LLM
- [ ] **Sprint 3:** Implementar `DetectorEntidadesNovas` com SPARQL de verificação
- [ ] **Sprint 4:** Implementar marcação de candidatos e relatório
- [ ] **Sprint 5:** Implementar `ValidadorOntologia` e versionamento .ttl
- [ ] **Sprint 6:** Implementar `VisualizadorKG` com PyVis + filtros por status
- [ ] **Sprint 7:** Integrar notebook didático end-to-end com exemplo médico completo
