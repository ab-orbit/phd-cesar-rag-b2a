# Planejamento Didático Avançado: Comparação de Estratégias RAG e Knowledge Graph

**Disciplina:** Ciência de Dados — Doutorado
**Objetivo:** Exploração incremental e comparativa de estratégias de indexação, recuperação e representação do conhecimento para RAG em corpus contínuos (Wikipedia), com avaliação rigorosa e uniforme entre todas as abordagens.

---

## 1. Visão Geral e Motivação Pedagógica

O ciclo anterior (Práticas 01 e 02) utilizou o dataset médico `AQ-MedAI/RAG-QA-Leaderboard` com perguntas e respostas pré-definidas, onde cada questão já vinha emparelhada com seu contexto de resposta. Embora útil como introdução, esse modelo oculta a parte mais difícil do RAG real: **como lidar com um corpus não estruturado e contínuo**, onde o sistema precisa decidir autonomamente como segmentar, representar e recuperar o conhecimento.

Este planejamento propõe um experimento comparativo com **seis abordagens de indexação** (três de chunking vetorial e três de Knowledge Graph), todas avaliadas com o **mesmo conjunto de métricas**, sobre um corpus de artigos da Wikipédia — um domínio não-médico com linguagem contínua, hierarquia de seções e riqueza de entidades nomeadas.

### Princípio Didático: Incremental e Comparativo

```
Corpus Wikipedia
       │
       ├── Módulo A: Chunking Vetorial ──┬── A1. Tamanho Fixo + Overlap (baseline)
       │                                 ├── A2. Estruturas Sintáticas (seções/parágrafos)
       │                                 └── A3. Contextual Chunking (LLM pré-sumariza)
       │
       └── Módulo B: Knowledge Graph ────┬── B1. NER puro (sem ontologia)
                                         ├── B2. Ontologia pré-definida + extração
                                         └── B3. Estrutura semântica (comunidades)

                    ↓ (todas as 6 abordagens)

         ┌─────────────────────────────────────┐
         │   Suite Unificada de Métricas RAG   │
         │  (DeepEval + IR clássico + custo)   │
         └─────────────────────────────────────┘
                    ↓
         Dashboard Comparativo (Langfuse)
```

---

## 2. Dataset Selecionado

### 2.1 Por que mudar o dataset?

O dataset `pubmed.jsonl` utilizado anteriormente é adequado para introdução, mas apresenta limitações para este estudo avançado:
- Perguntas isoladas, sem dependências entre documentos
- Contexto já fornecido (sem necessidade real de recuperação complexa)
- Vocabulário altamente técnico dificulta a intuição sobre chunking

### 2.2 Dataset Recomendado: 2WikiMultiHopQA + HotpotQA (já disponíveis no repositório)

**Fonte:** `AQ-MedAI/RAG-QA-Leaderboard/final_data/`
- **`2wiki.jsonl`** (14,3 MB) — 2WikiMultiHopQA
- **`hotpot_distractor.jsonl`** (8,55 MB) — HotpotQA com distratores
- **`documents_pool.json`** (740 MB) — corpus Wikipedia compartilhado

#### Por que esses datasets são pedagogicamente superiores?

| Critério | pubmed.jsonl (anterior) | 2wiki + hotpot (proposto) |
|----------|------------------------|---------------------------|
| Tipo de raciocínio | Pergunta direta | **Multi-hop** (2+ artigos) |
| Corpus | Textos médicos isolados | **Artigos Wikipedia contínuos** |
| Distratores | Não | **Sim** (hotpot) — testa precisão |
| Relação entre entidades | Fraca | **Rica** — ideal para KG |
| Tipos de pergunta | Factual simples | Comparison, Inference, Bridge |
| Relevância para KG | Baixa | **Alta** — entidades nomeadas abundantes |

#### Estrutura dos Dados

**`2wiki.jsonl`** — questões que cruzam dois artigos Wikipedia via entidade ponte:
```json
{
  "id": "2wiki_001",
  "query": "Who is the father of the director of 'Titanic'?",
  "golden_doc": ["Document_A", "Document_B"],
  "reference": ["Document_C", "Document_D", "Document_E"],
  "ground_truth": "James Cameron's father is Philip Cameron"
}
```
Tipos de questão no 2WikiMultiHopQA:
- **bridge**: "Quem fundou a cidade onde nasceu X?"
- **comparison**: "Quem nasceu primeiro, X ou Y?"
- **inference**: "Em que país fica a cidade onde Z foi fundado?"
- **bridge-comparison**: Híbrido das anteriores

**`hotpot_distractor.jsonl`** — questões multi-hop com documentos de distração deliberados:
```json
{
  "id": "hotpot_001",
  "query": "Were Scott Derrickson and Ed Wood of the same nationality?",
  "golden_doc": ["Document_scott", "Document_ed"],
  "reference": ["Document_distractor_1", "Document_distractor_2"],
  "ground_truth": "Yes"
}
```

### 2.3 Subconjunto para Execução Didática

Para viabilizar a execução no ambiente do curso:
- **50 questões** de `2wiki.jsonl` (10 de cada tipo)
- **50 questões** de `hotpot_distractor.jsonl`
- **Documentos necessários**: apenas os `golden_doc` + `reference` das 100 questões
- **Resultado**: ~300–500 documentos do pool de 740 MB → factível

```python
# Proporção recomendada de amostragem
amostra = {
    "2wiki_bridge": 15,          # maioria: cenário mais comum
    "2wiki_comparison": 10,
    "2wiki_inference": 10,
    "2wiki_bridge_comparison": 5,
    "hotpot_distractor": 30,     # incluir distratores para testar precisão
    "hotpot_fullwiki": 20
}
```

---

## 3. Arquitetura Unificada de Avaliação

Antes de descrever cada abordagem, é fundamental definir a **interface comum** que permitirá comparação justa. Todas as 6 abordagens devem implementar a mesma API:

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

@dataclass
class DocumentoRecuperado:
    conteudo: str
    metadados: dict
    score_similaridade: float
    origem: str  # ID do documento original no pool

@dataclass
class ResultadoRAG:
    query: str
    resposta: str
    documentos_recuperados: List[DocumentoRecuperado]
    latencia_recuperacao_ms: float
    latencia_geracao_ms: float
    tokens_prompt: int
    tokens_resposta: int
    custo_estimado_usd: float

class EstrategiaRAG(ABC):
    """Interface base para todas as 6 estratégias."""

    @abstractmethod
    def indexar(self, documentos: List[dict]) -> None:
        """Indexa o corpus na estrutura da estratégia."""

    @abstractmethod
    def recuperar(self, query: str, k: int = 5) -> List[DocumentoRecuperado]:
        """Recupera documentos relevantes para a query."""

    @abstractmethod
    def gerar_resposta(self, query: str, documentos: List[DocumentoRecuperado]) -> str:
        """Gera resposta a partir dos documentos recuperados."""

    def executar_pipeline(self, query: str, k: int = 5) -> ResultadoRAG:
        """Pipeline completo: recuperar + gerar."""
        # Implementação base compartilhada por todas as estratégias
        ...
```

---

## 4. Módulo A: Estratégias de Chunking Vetorial

Todas as três abordagens A1, A2 e A3 usam ChromaDB + OpenAI Embeddings como armazenamento vetorial. A diferença está **na forma como os documentos são segmentados antes da indexação**.

### Abordagem A1 — Chunking de Tamanho Fixo com Overlap (Baseline)

**Conceito:** Divide o texto em janelas deslizantes de tamanho fixo, com sobreposição para evitar perda semântica nas bordas.

**Parâmetros:**
```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter_fixo = RecursiveCharacterTextSplitter(
    chunk_size=512,        # ~100 palavras — balanceia granularidade e contexto
    chunk_overlap=64,      # ~12% de overlap — previne cortes abruptos
    length_function=len,
    separators=["\n\n", "\n", ". ", " ", ""]
)
```

**Didática — o que observar:**
- Chunks podem cortar no meio de uma frase ou argumento
- Overlap ajuda, mas não resolve ambiguidade semântica
- Muito fácil de implementar; serve como **linha de base**
- Ver nas métricas: Contextual Precision tende a ser baixa (chunks ruidosos)

**Visualizações propostas:**
```
┌──────────────────────────────────────────────────────────┐
│  Artigo Wikipedia: "James Cameron"                       │
│                                                          │
│  chunk_1: [chars 0-511]    ████████████████████▓▓▓▓▓▓  │
│  chunk_2: [chars 448-959]      ▓▓▓▓▓▓████████████████  │
│  chunk_3: [chars 896-1407]         ▓▓▓▓▓▓██████████   │
│                    ↑ overlap        ↑ overlap           │
└──────────────────────────────────────────────────────────┘
```

---

### Abordagem A2 — Chunking por Estruturas Sintáticas

**Conceito:** Respeita a estrutura natural do documento — artigos Wikipedia têm seções, subseções e parágrafos bem definidos. Chunks alinham-se com unidades de significado.

**Implementação com LangChain:**
```python
from langchain.text_splitter import MarkdownHeaderTextSplitter

# Wikipedia exportado como Markdown mantém hierarquia de títulos
headers_para_dividir = [
    ("#", "titulo_artigo"),
    ("##", "secao"),
    ("###", "subsecao"),
    ("####", "topico"),
]

splitter_sintatico = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers_para_dividir,
    strip_headers=False,   # manter cabeçalhos no chunk para contexto
    return_each_line=False
)

# Para textos sem markdown: usar NLTK/spaCy para detectar parágrafos
from langchain.text_splitter import NLTKTextSplitter
splitter_paragrafo = NLTKTextSplitter(chunk_size=1000)
```

**Hierarquia de Granularidade:**
```
Nível 0 (maior): Artigo inteiro
    │
    ├── Nível 1: Seção principal (##)
    │       ├── Nível 2: Subseção (###)
    │       │       └── Nível 3: Parágrafo (unidade atômica)
    │       └── Nível 2: Subseção (###)
    └── Nível 1: Seção principal (##)
```

**Metadados enriquecidos:**
```python
{
    "texto": "James Cameron foi o diretor...",
    "titulo_artigo": "James Cameron",
    "secao": "Carreira",
    "subsecao": "Titanic (1997)",
    "posicao_no_artigo": 3,   # índice ordinal da seção
    "nivel_hierarquico": 2,
    "num_tokens": 87
}
```

**Didática — o que observar:**
- Seções Wikipedia são semanticamente coesas → Contextual Relevancy tende a ser superior
- Chunks de tamanho variado dificultam batch processing uniforme
- Multi-hop fica mais natural: chunk A da seção "Carreira" + chunk B da seção "Vida Pessoal"
- Comparar com A1: qual tem maior Contextual Recall nas questões do tipo "bridge"?

---

### Abordagem A3 — Contextual Chunking

**Conceito:** Técnica introduzida pela Anthropic em 2024 ("Contextual Retrieval"). Antes de indexar cada chunk, um LLM gera uma breve descrição do **contexto maior** em que aquele chunk se insere. Esse contexto é **pré-pendado ao texto do chunk** antes de gerar o embedding.

**Por que funciona?**
```
Problema com chunks fixos:
  Chunk isolado: "Ele ganhou o prêmio em 1998."
  Pergunta: "Quando Cameron ganhou o Oscar?"
  → Sem contexto, o embedding do chunk é fraco!

Com Contextual Chunking:
  Chunk enriquecido: "[Do artigo sobre James Cameron, seção Prêmios:] Ele ganhou o prêmio em 1998."
  → O embedding agora é semanticamente completo!
```

**Implementação:**
```python
PROMPT_CONTEXTO = """Você receberá um trecho de um artigo e o artigo completo.
Gere uma frase curta (máx. 2 linhas) que situa o trecho no contexto do artigo.
Esta frase será pré-pendada ao trecho para melhorar a busca semântica.

Artigo completo:
<artigo>
{artigo_completo}
</artigo>

Trecho a contextualizar:
<trecho>
{trecho}
</trecho>

Responda APENAS com a frase de contexto, sem aspas ou formatação."""

def gerar_contexto_do_chunk(artigo_completo: str, trecho: str) -> str:
    """
    Chama o LLM para situar o trecho no contexto do artigo.
    Custo: ~200 tokens por chunk (considerar cache de prompt).
    """
    resposta = llm.invoke(PROMPT_CONTEXTO.format(
        artigo_completo=artigo_completo[:3000],  # janela truncada para custo
        trecho=trecho
    ))
    return resposta.content

def indexar_com_contexto(documentos: List[dict]) -> None:
    chunks_base = splitter_fixo.split_documents(documentos)

    chunks_contextualizados = []
    for chunk in chunks_base:
        artigo_fonte = obter_artigo_completo(chunk.metadata["doc_id"])
        contexto = gerar_contexto_do_chunk(artigo_fonte, chunk.page_content)

        # Chunk enriquecido = contexto + texto original
        chunk_enriquecido = f"{contexto}\n\n{chunk.page_content}"
        chunks_contextualizados.append(
            Document(page_content=chunk_enriquecido, metadata=chunk.metadata)
        )

    vector_store.add_documents(chunks_contextualizados)
```

**Didática — o que observar:**
- Custo: ~N×200 tokens extras por chunk na indexação (calcular e mostrar)
- Qualidade: Melhor Contextual Recall em questões tipo "inference" e "comparison"
- Trade-off: custo de indexação vs. qualidade de recuperação
- Usar `cache_control` da API Anthropic para reduzir custo em artigos longos

---

## 5. Módulo B: Knowledge Graph como Base de Recuperação

As abordagens B1, B2 e B3 substituem o ChromaDB por um grafo de conhecimento. A **recuperação** deixa de ser por similaridade vetorial e passa a ser por **traversal de grafo**.

### Conceito Base: GraphRAG

```
Documentos Wikipedia
        │
   Extração de ──► Entidades (nós) + Relações (arestas)
   Conhecimento
        │
        ▼
   Grafo de Conhecimento (NetworkX + opcional: Neo4j)
        │
   Query → Identificar entidades na query
        │
   Traversal → Expandir subgrafo relevante
        │
   Recuperar textos associados aos nós do subgrafo
        │
   Gerador (mesmo LLM das abordagens A)
```

**Dependências adicionais para Módulo B:**
```bash
pip install spacy networkx neo4j pyvis  # visualização do grafo
python -m spacy download pt_core_news_lg  # ou en_core_web_trf
pip install gliner  # NER moderno baseado em LLMs (GLiNER)
```

---

### Abordagem B1 — Knowledge Graph via NER (sem ontologia pré-definida)

**Conceito:** Extrai entidades nomeadas do corpus usando spaCy e cria um grafo onde os nós são entidades e as arestas representam co-ocorrência no mesmo parágrafo ou sentenças consecutivas.

**Sem ontologia** significa: o sistema não sabe de antemão que tipos de entidades existem nem como se relacionam — aprende tudo dos dados.

**Implementação:**
```python
import spacy
import networkx as nx

nlp = spacy.load("en_core_web_trf")  # modelo transformer para NER preciso

def extrair_entidades_e_relacoes(texto: str, doc_id: str) -> list:
    """
    Extração de co-ocorrência simples:
    - Nó: cada entidade nomeada (PERSON, ORG, GPE, DATE, WORK_OF_ART...)
    - Aresta: entidades no mesmo parágrafo compartilham aresta de co-ocorrência
    """
    doc = nlp(texto)
    triplas = []

    for sent in doc.sents:
        entidades_sentenca = [(ent.text, ent.label_) for ent in sent.ents]

        # Criar par para cada combinação de entidades na mesma sentença
        for i, (ent_a, tipo_a) in enumerate(entidades_sentenca):
            for ent_b, tipo_b in entidades_sentenca[i+1:]:
                triplas.append({
                    "sujeito": ent_a, "tipo_sujeito": tipo_a,
                    "relacao": "CO_OCORRE_COM",
                    "objeto": ent_b, "tipo_objeto": tipo_b,
                    "contexto": sent.text,
                    "doc_id": doc_id
                })
    return triplas

def construir_grafo_ner(documentos: List[dict]) -> nx.DiGraph:
    G = nx.DiGraph()
    for doc in documentos:
        triplas = extrair_entidades_e_relacoes(doc["texto"], doc["id"])
        for t in triplas:
            G.add_node(t["sujeito"], tipo=t["tipo_sujeito"])
            G.add_node(t["objeto"], tipo=t["tipo_objeto"])
            G.add_edge(t["sujeito"], t["objeto"],
                      relacao=t["relacao"],
                      contexto=t["contexto"],
                      doc_id=t["doc_id"])
    return G
```

**Recuperação via Grafo:**
```python
def recuperar_via_grafo_ner(query: str, G: nx.DiGraph, k_hops: int = 2) -> List[str]:
    """
    1. Identifica entidades da query no grafo
    2. Expande k saltos a partir dessas entidades
    3. Coleta os contextos das arestas do subgrafo
    """
    entidades_query = [ent.text for ent in nlp(query).ents]

    subgrafo_nos = set()
    for entidade in entidades_query:
        if entidade in G:
            vizinhos = nx.single_source_shortest_path_length(G, entidade, cutoff=k_hops)
            subgrafo_nos.update(vizinhos.keys())

    # Coletar contextos das arestas do subgrafo
    contextos = []
    for u, v, dados in G.edges(data=True):
        if u in subgrafo_nos or v in subgrafo_nos:
            contextos.append(dados["contexto"])

    return contextos[:k_hops * 10]  # limitar retorno
```

**Didática — o que observar:**
- Grafo muito esparso se o corpus for pequeno
- Muitas arestas de co-ocorrência não têm significado semântico real
- Multi-hop fica natural: James Cameron → (CO_OCORRE_COM) → Titanic → (CO_OCORRE_COM) → 1997 Oscar
- Ver: como Contextual Precision cai quando as arestas são apenas co-ocorrência?

---

### Abordagem B2 — Knowledge Graph com Ontologia Pré-definida

**Conceito:** Antes de processar o corpus, define-se um esquema ontológico — os tipos de entidades e os tipos de relações possíveis. A extração via LLM é guiada por esse esquema, produzindo triplas mais significativas.

**Ontologia para corpus Wikipedia (domínio geral):**
```python
ONTOLOGIA = {
    "tipos_entidade": {
        "Pessoa": "Indivíduo nomeado (historiador, político, artista, etc.)",
        "Organizacao": "Empresa, instituição, partido, time esportivo",
        "Local": "País, cidade, região, endereço",
        "Obra": "Filme, livro, música, pintura, obra de arte",
        "Evento": "Guerra, eleição, festival, acidente",
        "Data": "Ano, período, era histórica",
        "Conceito": "Ideia abstrata, disciplina, teoria"
    },
    "tipos_relacao": {
        "NASCEU_EM": ("Pessoa", "Local"),
        "FUNDOU": ("Pessoa|Organizacao", "Organizacao|Local"),
        "CRIOU": ("Pessoa", "Obra"),
        "DIRIGIU": ("Pessoa", "Obra|Organizacao"),
        "PREMIADO_COM": ("Pessoa|Obra", "Obra"),     # Oscar, Grammy, etc.
        "OCORREU_EM": ("Evento", "Local|Data"),
        "PARTE_DE": ("*", "*"),
        "PRECEDIDO_POR": ("Pessoa|Evento", "Pessoa|Evento"),
        "SUCEDIDO_POR": ("Pessoa|Evento", "Pessoa|Evento"),
        "NACIONALIDADE": ("Pessoa", "Local"),
        "AFILIADO_A": ("Pessoa", "Organizacao")
    }
}
```

**Extração via LLM com schema:**
```python
PROMPT_EXTRACAO_ONTOLOGICA = """Extraia triplas de conhecimento do texto abaixo.
Use APENAS os tipos de entidade e relação do esquema fornecido.

ESQUEMA:
Entidades: {tipos_entidade}
Relações: {tipos_relacao}

TEXTO:
{texto}

Retorne JSON no formato:
[
  {{"sujeito": "...", "tipo_sujeito": "...", "relacao": "...", "objeto": "...", "tipo_objeto": "...", "evidencia": "trecho exato do texto"}}
]

IMPORTANTE: Use SOMENTE relações do esquema. Se não houver relação clara, omita a tripla."""
```

**Vantagem sobre B1:**
```
B1 (co-ocorrência bruta):
  "Cameron" --CO_OCORRE_COM--> "1998" --CO_OCORRE_COM--> "Oscar"
  (não diz nada sobre a natureza da relação)

B2 (ontologia):
  "James Cameron" --CRIOU--> "Titanic (1997)"
  "Titanic (1997)" --PREMIADO_COM--> "Oscar de Melhor Filme"
  "James Cameron" --PREMIADO_COM--> "Oscar de Melhor Diretor"
  (triplas semanticamente ricas e consultáveis)
```

**Didática — o que observar:**
- LLM pode "alucinar" relações não existentes no texto → checar com Faithfulness
- Ontologia reduz ruído mas pode perder relações incomuns (problema de cobertura)
- Ideal para domínios bem definidos (história, ciência, biologia)
- Comparar B1 vs B2: qual produz maior Contextual Precision?

---

### Abordagem B3 — Knowledge Graph com Estrutura Semântica

**Conceito:** Inspirado no **Microsoft GraphRAG** (2024). Após construir o grafo (podendo partir de B1 ou B2), aplica-se detecção de comunidades para identificar **clusters temáticos**. Cada comunidade recebe um **sumário semântico** gerado pelo LLM. A recuperação opera em dois níveis: global (busca no sumário de comunidades) e local (traversal dentro da comunidade).

**Arquitetura em camadas:**
```
Nível 3 (Global):  Sumários de Comunidades
                   ["Filmes de Ficção Científica", "Diretores Hollywodianos", ...]
                        ↑ gerado pelo LLM
Nível 2 (Meso):    Comunidades detectadas via Louvain/Leiden
                   [Comunidade_A: {Cameron, Spielberg, Kubrick...},
                    Comunidade_B: {Titanic, Avatar, Aliens...}]
                        ↑ detecção de comunidades
Nível 1 (Local):   Grafo base de entidades e relações (de B1 ou B2)
```

**Implementação:**
```python
import community as community_louvain   # pip install python-louvain
from langchain_core.prompts import PromptTemplate

def detectar_comunidades(G: nx.Graph) -> dict:
    """
    Algoritmo de Louvain para detecção de comunidades.
    Retorna: {node_id: community_id}
    """
    G_undirected = G.to_undirected()
    return community_louvain.best_partition(G_undirected)

def sumarizar_comunidade(nos_comunidade: list, G: nx.Graph, llm) -> str:
    """
    Para cada comunidade, gera um sumário narrativo usando o LLM.
    Esse sumário serve como "contexto global" para buscas de alto nível.
    """
    # Coletar todos os contextos de arestas dentro da comunidade
    triplas_texto = []
    for u, v, dados in G.edges(data=True):
        if u in nos_comunidade and v in nos_comunidade:
            triplas_texto.append(f"{u} → {dados.get('relacao', '?')} → {v}")

    prompt = f"""Dadas as seguintes relações entre entidades:
    {chr(10).join(triplas_texto[:50])}

    Escreva um parágrafo coeso (3-5 frases) descrevendo o tema central
    e as entidades principais deste grupo de conhecimento."""

    return llm.invoke(prompt).content

def recuperar_via_estrutura_semantica(query: str, nivel: str = "global") -> List[str]:
    """
    Recuperação em dois níveis:
    - "global": busca nos sumários de comunidades (responde perguntas de visão geral)
    - "local": traversal dentro da comunidade mais relevante
    """
    if nivel == "global":
        # Encontrar comunidade mais similar à query (via embedding)
        comunidade_id = encontrar_comunidade_relevante(query)
        return [sumarios_comunidades[comunidade_id]]
    else:
        # Traversal local dentro da comunidade
        comunidade_id = encontrar_comunidade_relevante(query)
        nos_da_comunidade = obter_nos_comunidade(comunidade_id)
        return recuperar_via_grafo_ner(query, subgrafo_comunidade)
```

**Didática — o que observar:**
- Recuperação global é útil para questões do tipo "comparison" (comparar dois personagens)
- Recuperação local é melhor para questões do tipo "bridge" (cadeia de entidades)
- Detecção de comunidades pode revelar estruturas temáticas não óbvias no corpus
- Comparar B3 global vs. local vs. B1/B2 vs. A1/A2/A3 no dashboard final

---

## 6. Suite Unificada de Métricas

**Princípio:** A mesma suite de métricas é executada para todas as 6 abordagens, permitindo comparação direta em tabela e visualizações heatmap.

### 6.1 Métricas de Geração (LLM-as-Judge via DeepEval)

Medem a qualidade da **resposta gerada**, independente de como foi feita a recuperação:

| Métrica | Ferramenta | O que mede | Fórmula conceitual |
|---------|-----------|------------|-------------------|
| **Answer Relevancy** | DeepEval | A resposta é completa e não prolixa em relação à pergunta? | `score = f(relevância, completude, concisão)` |
| **Faithfulness** | DeepEval | Cada afirmação na resposta é suportada pelo contexto recuperado? | `score = claims_suportados / total_claims` |
| **Correctness** | DeepEval/custom | A resposta está factualmente correta vs. ground truth? | `LLM-as-judge(resposta, ground_truth)` |

```python
from deepeval.metrics import (
    AnswerRelevancyMetric,
    FaithfulnessMetric,
    GEval  # para Correctness customizado
)

metrica_relevancia = AnswerRelevancyMetric(
    threshold=0.7,
    model="gpt-4o-mini",
    include_reason=True
)

metrica_fidelidade = FaithfulnessMetric(
    threshold=0.8,
    model="gpt-4o-mini",
    include_reason=True
)

metrica_correcao = GEval(
    name="Correcao_Factual",
    criteria="A resposta contém a informação factual esperada do ground truth?",
    evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT, LLMTestCaseParams.EXPECTED_OUTPUT],
    threshold=0.7
)
```

### 6.2 Métricas de Recuperação Contextual (DeepEval)

Medem a qualidade do **contexto recuperado**, antes mesmo de chegar no gerador:

| Métrica | O que mede | Importância Multi-hop |
|---------|-----------|----------------------|
| **Contextual Recall** | O contexto recuperado cobre as informações necessárias para a resposta ideal? | Alta — multi-hop requer múltiplos documentos |
| **Contextual Precision** | Os chunks mais relevantes estão ranqueados nas primeiras posições? | Alta — com distratores (hotpot), order importa |
| **Contextual Relevancy** | Qual a proporção de informação útil vs. ruído no contexto? | Crítica — distratores inflam o ruído |

```python
from deepeval.metrics import (
    ContextualRecallMetric,
    ContextualPrecisionMetric,
    ContextualRelevancyMetric
)
```

### 6.3 Métricas Clássicas de Recuperação de Informação (IR)

Baseadas nos `golden_doc` como ground truth. Medem se os documentos **exatos** foram recuperados:

```python
def calcular_metricas_ir_classicas(
    docs_recuperados: List[str],   # IDs dos documentos recuperados
    golden_docs: List[str],        # IDs dos documentos corretos (ground truth)
    k_valores: List[int] = [1, 3, 5, 10]
) -> dict:
    """
    Precision@K: |recuperados ∩ golden| / K
    Recall@K:    |recuperados ∩ golden| / |golden|
    F1@K:        2 × (P@K × R@K) / (P@K + R@K)
    MRR:         1 / posição_do_primeiro_doc_correto
    NDCG@K:      Normalized Discounted Cumulative Gain (premia ranking correto)
    Hit@K:       1 se ao menos 1 golden_doc está no top-K, 0 caso contrário
    """
    resultados = {}

    for k in k_valores:
        top_k = docs_recuperados[:k]
        relevantes_no_top_k = set(top_k) & set(golden_docs)

        precision_k = len(relevantes_no_top_k) / k
        recall_k = len(relevantes_no_top_k) / len(golden_docs) if golden_docs else 0
        f1_k = 2 * precision_k * recall_k / (precision_k + recall_k + 1e-9)

        resultados[f"P@{k}"] = precision_k
        resultados[f"R@{k}"] = recall_k
        resultados[f"F1@{k}"] = f1_k
        resultados[f"Hit@{k}"] = 1.0 if relevantes_no_top_k else 0.0

    # MRR
    mrr = 0.0
    for i, doc_id in enumerate(docs_recuperados, 1):
        if doc_id in golden_docs:
            mrr = 1.0 / i
            break
    resultados["MRR"] = mrr

    # NDCG@5
    resultados["NDCG@5"] = calcular_ndcg(docs_recuperados[:5], golden_docs)

    return resultados
```

### 6.4 Métricas de Eficiência Operacional

Para avaliar custo-benefício de cada abordagem:

| Métrica | Unidade | Coleta |
|---------|---------|--------|
| `latencia_indexacao_total_s` | segundos | medido na fase de indexação |
| `latencia_media_recuperacao_ms` | milissegundos | Langfuse Span |
| `latencia_media_geracao_ms` | milissegundos | Langfuse Generation |
| `tokens_prompt_medio` | tokens | Langfuse / OpenAI callback |
| `tokens_resposta_medio` | tokens | Langfuse / OpenAI callback |
| `custo_indexacao_total_usd` | USD | `tokens × preço_embedding` |
| `custo_por_query_usd` | USD | `tokens_prompt × preço_entrada + tokens_resposta × preço_saída` |
| `tamanho_indice_mb` | MB | tamanho do diretório ChromaDB ou nós/arestas do grafo |

### 6.5 Métricas Específicas para Multi-hop (2wiki + hotpot)

```python
def calcular_metricas_multihop(resposta: str, ground_truth: str) -> dict:
    """
    Exact Match (EM): resposta normalizada == ground_truth normalizado
    Token F1: F1 baseado em overlap de tokens (palavra a palavra)
    Subset Match: ground_truth contido como substring na resposta
    """
    def normalizar(texto):
        # Remover pontuação, lowercase, artigos
        import re, string
        texto = texto.lower().strip()
        texto = re.sub(r'\b(a|an|the)\b', ' ', texto)
        texto = texto.translate(str.maketrans('', '', string.punctuation))
        return ' '.join(texto.split())

    resp_norm = normalizar(resposta)
    gt_norm = normalizar(ground_truth)

    # Exact Match
    em = float(resp_norm == gt_norm)

    # Token F1
    resp_tokens = set(resp_norm.split())
    gt_tokens = set(gt_norm.split())
    if not resp_tokens or not gt_tokens:
        token_f1 = 0.0
    else:
        common = resp_tokens & gt_tokens
        precision = len(common) / len(resp_tokens)
        recall = len(common) / len(gt_tokens)
        token_f1 = 2 * precision * recall / (precision + recall + 1e-9)

    return {"EM": em, "Token_F1": token_f1}
```

### 6.6 Tabela Resumo de Métricas

```
┌─────────────────────────┬──────┬──────┬──────┬──────┬──────┬──────┐
│ Métrica                 │  A1  │  A2  │  A3  │  B1  │  B2  │  B3  │
├─────────────────────────┼──────┼──────┼──────┼──────┼──────┼──────┤
│ Answer Relevancy        │  —   │  —   │  —   │  —   │  —   │  —   │
│ Faithfulness            │  —   │  —   │  —   │  —   │  —   │  —   │
│ Correctness             │  —   │  —   │  —   │  —   │  —   │  —   │
├─────────────────────────┼──────┼──────┼──────┼──────┼──────┼──────┤
│ Contextual Recall       │  —   │  —   │  —   │  —   │  —   │  —   │
│ Contextual Precision    │  —   │  —   │  —   │  —   │  —   │  —   │
│ Contextual Relevancy    │  —   │  —   │  —   │  —   │  —   │  —   │
├─────────────────────────┼──────┼──────┼──────┼──────┼──────┼──────┤
│ Precision@5             │  —   │  —   │  —   │  —   │  —   │  —   │
│ Recall@5                │  —   │  —   │  —   │  —   │  —   │  —   │
│ MRR                     │  —   │  —   │  —   │  —   │  —   │  —   │
│ NDCG@5                  │  —   │  —   │  —   │  —   │  —   │  —   │
├─────────────────────────┼──────┼──────┼──────┼──────┼──────┼──────┤
│ EM (multi-hop)          │  —   │  —   │  —   │  —   │  —   │  —   │
│ Token F1 (multi-hop)    │  —   │  —   │  —   │  —   │  —   │  —   │
├─────────────────────────┼──────┼──────┼──────┼──────┼──────┼──────┤
│ Latência recuperação ms │  —   │  —   │  —   │  —   │  —   │  —   │
│ Custo/query USD         │  —   │  —   │  —   │  —   │  —   │  —   │
└─────────────────────────┴──────┴──────┴──────┴──────┴──────┴──────┘
```

---

## 7. Estrutura dos Notebooks

A implementação será dividida em notebooks modulares para evitar notebooks gigantes e facilitar execução incremental:

```
notebooks/
├── 00_exploracao_dados.ipynb          # Análise dos datasets 2wiki + hotpot
├── 01_modulo_metricas_compartilhado.ipynb  # Define a suite de métricas (rodar 1x)
├── 02_A1_chunking_fixo.ipynb          # Abordagem A1
├── 03_A2_chunking_sintatico.ipynb     # Abordagem A2
├── 04_A3_contextual_chunking.ipynb    # Abordagem A3
├── 05_B1_kg_ner.ipynb                 # Abordagem B1
├── 06_B2_kg_ontologia.ipynb           # Abordagem B2
├── 07_B3_kg_semantico.ipynb           # Abordagem B3
└── 08_dashboard_comparativo.ipynb     # Consolida resultados e gera visualizações
```

### Notebook 00 — Exploração dos Dados (notebook âncora)

Executado uma única vez, gera o subconjunto compartilhado por todos os outros notebooks.

**Células:**
1. Download dos arquivos (2wiki.jsonl, hotpot_distractor.jsonl, documents_pool.json)
2. Análise exploratória:
   - Distribuição dos tipos de questão no 2wiki (bridge/comparison/inference)
   - Comprimento médio de query e ground truth
   - Número de golden_docs por questão (1-hop vs 2-hop)
   - Nuvem de entidades mais frequentes
3. Criação e serialização do subconjunto (`subset_100q.pkl`):
   - 100 questões balanceadas
   - ~400 documentos do pool resolvidos
4. Análise de dificuldade:
   - Identificar questões "fáceis" (1 golden_doc) vs "difíceis" (2+)
   - Comprimento médio dos documentos relevantes
   - Presença de distratores (hotpot)

### Notebooks 02–07 (cada abordagem)

Estrutura idêntica em todos para facilitar comparação:

```
Célula 1 — Markdown: Motivação teórica da abordagem
Célula 2 — Código: Carregamento do subconjunto compartilhado
Célula 3 — Código: Indexação (parte específica de cada abordagem)
Célula 4 — Markdown: O que foi criado? (estatísticas do índice)
Célula 5 — Código: Teste de recuperação em 3 exemplos manuais
Célula 6 — Código: Execução pipeline RAG nas 100 questões
Célula 7 — Código: Cálculo das métricas (via módulo compartilhado)
Célula 8 — Código: Envio de scores ao Langfuse
Célula 9 — Código: Serialização dos resultados (`resultados_A1.pkl`, etc.)
Célula 10 — Markdown: Análise dos resultados desta abordagem
```

### Notebook 08 — Dashboard Comparativo

```python
# Carrega resultados de todas as abordagens
resultados = {
    "A1": pd.read_pickle("resultados_A1.pkl"),
    "A2": pd.read_pickle("resultados_A2.pkl"),
    "A3": pd.read_pickle("resultados_A3.pkl"),
    "B1": pd.read_pickle("resultados_B1.pkl"),
    "B2": pd.read_pickle("resultados_B2.pkl"),
    "B3": pd.read_pickle("resultados_B3.pkl"),
}

# Visualizações:
# 1. Heatmap: abordagem × métrica (radar chart)
# 2. Trade-off: custo × qualidade (scatter)
# 3. Análise por tipo de questão: qual abordagem é melhor para "bridge"? para "comparison"?
# 4. Curva Precision-Recall comparativa
# 5. Tabela ranqueada por métrica agregada
```

---

## 8. Roadmap de Implementação

### Fase 0 — Preparação (pré-requisito)
- [ ] Verificar disponibilidade das chaves de API (OpenAI, Langfuse)
- [ ] Instalar dependências adicionais: `spacy`, `networkx`, `gliner`, `python-louvain`, `pyvis`
- [ ] Baixar modelos spaCy: `en_core_web_trf`
- [ ] Executar `00_exploracao_dados.ipynb` e gerar `subset_100q.pkl`

### Fase 1 — Módulo de Métricas Compartilhado
- [ ] Implementar `calcular_metricas_ir_classicas()` com P@K, R@K, MRR, NDCG@K, Hit@K
- [ ] Implementar `calcular_metricas_multihop()` com EM e Token F1
- [ ] Configurar métricas DeepEval (Answer Relevancy, Faithfulness, Contextual trio)
- [ ] Configurar GEval para Correctness
- [ ] Implementar `registrar_metricas_langfuse()` — envia todos os scores para o trace correspondente
- [ ] Validar com 2–3 exemplos manuais
- [ ] Executar `01_modulo_metricas_compartilhado.ipynb`

### Fase 2 — Módulo A: Chunking Vetorial
- [ ] **A1** — Implementar chunking fixo + ChromaDB + pipeline completo → avaliar → serializar
- [ ] **A2** — Implementar chunking sintático (MarkdownHeaderTextSplitter) → avaliar → serializar
- [ ] **A3** — Implementar contextual chunking (LLM pré-sumariza) → avaliar → serializar
- [ ] Análise parcial A1 vs A2 vs A3

### Fase 3 — Módulo B: Knowledge Graph
- [ ] **B1** — Implementar extração NER (spaCy) + grafo NetworkX + traversal → avaliar → serializar
- [ ] **B2** — Definir ontologia + extração LLM guiada + grafo → avaliar → serializar
- [ ] **B3** — Detecção de comunidades (Louvain) + sumários semânticos (LLM) + recuperação em 2 níveis → avaliar → serializar

### Fase 4 — Comparação e Síntese
- [ ] Consolidar resultados no notebook 08
- [ ] Gerar visualizações comparativas
- [ ] Análise estratificada por tipo de questão (bridge, comparison, inference)
- [ ] Análise de custo-benefício
- [ ] Redigir conclusões: quando usar cada abordagem?

---

## 9. Hipóteses a Verificar

As questões de pesquisa que o experimento comparativo responde:

1. **H1 — Contextual Chunking (A3) supera Fixed Chunking (A1) em Contextual Recall?**
   - Hipótese: Sim, especialmente em questões "bridge" onde a entidade-ligação está em meio a um parágrafo

2. **H2 — Chunking Sintático (A2) tem melhor Contextual Precision que Fixed (A1)?**
   - Hipótese: Sim, pois seções Wikipedia são semanticamente coesas; A1 fragmenta o raciocínio

3. **H3 — Knowledge Graph (B2) supera Vector RAG (A*) em questões de comparação?**
   - Hipótese: Sim, pois comparação de duas entidades é natural em grafo (buscar propriedades de dois nós)

4. **H4 — KG sem ontologia (B1) tem baixa Contextual Precision?**
   - Hipótese: Sim, pois co-ocorrência gera muitas arestas irrelevantes

5. **H5 — Estrutura Semântica (B3) tem melhor performance em perguntas globais?**
   - Hipótese: Sim, mas pior em perguntas específicas de fato (trade-off global vs. local)

6. **H6 — A3 tem custo de indexação 10× maior que A1 por chunk?**
   - Hipótese: Sim (~200 tokens por chunk para o contexto via LLM), mas custo de query similar

---

## 10. Referências e Recursos

### Técnicas e Papers
- **Contextual Retrieval (Anthropic)**: https://www.anthropic.com/news/contextual-retrieval
- **GraphRAG (Microsoft)**: https://microsoft.github.io/graphrag/
- **2WikiMultiHopQA**: Ho et al. (2020), COLING 2020
- **HotpotQA**: Yang et al. (2018), EMNLP 2018
- **MuSiQue**: Trivedi et al. (2022), TACL

### Avaliação e Benchmarks
- **Evidently AI — RAG Benchmarks**: https://www.evidentlyai.com/blog/rag-benchmarks
- **DeepEval Docs**: https://docs.confident-ai.com/
- **RAGAS Framework**: https://docs.ragas.io/

### Ferramentas
- **GraphRAG (Microsoft)**: https://github.com/microsoft/graphrag
- **GLiNER (NER moderno)**: https://github.com/urchade/GLiNER
- **Langfuse Docs**: https://langfuse.com/docs
- **NetworkX**: https://networkx.org/

### Datasets disponíveis no repositório
| Arquivo | Tipo | Questões | Corpus |
|---------|------|----------|--------|
| `2wiki.jsonl` | Multi-hop Wikipedia | ~5k | documents_pool.json |
| `hotpot_distractor.jsonl` | Multi-hop + distratores | ~7k | documents_pool.json |
| `musique.jsonl` | 2–4 hops | ~2k | documents_pool.json |
| `popqa.jsonl` | Conhecimento popular | ~14k | documents_pool.json |
| `triviaqa.jsonl` | Trivia | ~17k | documents_pool.json |

**Recomendação:** Para implementação inicial, usar `2wiki.jsonl` + `hotpot_distractor.jsonl`. Para estudo de escalabilidade, adicionar `musique.jsonl`.

---

## 11. Considerações de Custo Estimado

Todos os custos baseados em preços OpenAI (março 2026):
- `text-embedding-3-small`: $0.02/1M tokens
- `gpt-4o-mini` input: $0.15/1M tokens | output: $0.60/1M tokens

| Fase | Abordagem | Operação | Custo Estimado |
|------|-----------|----------|----------------|
| Indexação | A1/A2 | ~500 chunks × 200 tokens embedding | ~$0.002 |
| Indexação | A3 | ~500 chunks × 500 tokens LLM contexto | ~$0.04 |
| Indexação | B1 | spaCy local — sem custo API | $0.00 |
| Indexação | B2 | ~200 docs × 600 tokens LLM extração | ~$0.02 |
| Indexação | B3 | B2 + ~30 comunidades × 400 tokens sumário | ~$0.024 |
| Avaliação | Todas | 100 questões × 5 métricas DeepEval × 2k tokens | ~$0.15 |
| Pipeline | Todas | 100 queries × 1k tokens prompt+resposta | ~$0.075 |
| **Total estimado** | | | **~$0.50–$1.00** |

*Nota: Custo pode variar. Usar `gpt-4o-mini` nas métricas DeepEval para controle de custo. Recomenda-se testar com 10 questões antes de escalar para 100.*

---

*Planejamento elaborado em 2026-03-14 para a disciplina de Doutorado em Ciência de Dados.*
*Versão 1.0 — Estratégias RAG Avançadas: Chunking e Knowledge Graph*
