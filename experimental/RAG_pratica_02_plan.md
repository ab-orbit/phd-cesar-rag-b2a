# Planejamento: RAG Prática 02 - Sistema Completo com Avaliação

## Objetivo
Implementar um sistema RAG completo e didático utilizando dados reais do HuggingFace, com foco em avaliação de qualidade através de métricas estabelecidas pela literatura (Correctness, Faithfulness e métricas de recuperação).

## Dataset

### Fonte: HuggingFace `AQ-MedAI/RAG-QA-Leaderboard`

**Arquivos Disponíveis em `/final_data`:**

1. **documents_pool.json** (740 MB)
   - Corpus centralizado de documentos derivados da Wikipédia
   - Funciona como base de conhecimento para recuperação
   - Documentos indexados por IDs (ex: "Document_27178")
   - Pré-processados com Contriever para recuperação eficiente

2. **pubmed.jsonl** (583 KB) - **ARQUIVO PRINCIPAL PARA O PROJETO**
   - Domínio: Médico/científico (adequado ao contexto do projeto)
   - Formato: JSON Lines (uma pergunta por linha)
   - Estrutura de cada registro:
     ```json
     {
       "id": "pubmed_123",
       "query": "Pergunta médica/científica",
       "golden_doc": ["Document_XXX", "Document_YYY"],
       "reference": ["Document_ZZZ", ...],
       "ground_truth": "Resposta correta"
     }
     ```

3. **Outros arquivos disponíveis** (uso opcional/comparativo):
   - `2wiki.jsonl` (14,3 MB) - Multi-hop QA
   - `hotpot_distractor.jsonl` (8,55 MB) - QA com distrações
   - `musique.jsonl` (2,89 MB) - Raciocínio multi-hop
   - `popqa.jsonl` (3,43 MB) - Conhecimento popular
   - `triviaqa.jsonl` (746 KB) - Trivia geral

### Estrutura dos Dados

**Campos principais:**
- `query`: Pergunta de entrada do usuário
- `ground_truth`: Resposta(s) correta(s) esperada(s)
- `golden_doc`: Lista de IDs dos documentos "ouro" (contêm evidências corretas)
- `reference`: Lista de IDs de documentos relacionados adicionais
- `id`: Identificador único do caso de teste

**Relação entre arquivos:**
- Os IDs em `golden_doc` e `reference` referenciam documentos em `documents_pool.json`
- Permite avaliação tanto de **retrieval** (encontrar golden_doc) quanto **generation** (produzir ground_truth)

### Abordagem de Implementação

**Para fins didáticos:**
1. Usar **pubmed.jsonl** como fonte principal (domínio médico/científico)
2. Carregar **subset de documents_pool.json** (apenas documentos referenciados pelo pubmed)
3. Trabalhar com amostra de 50-100 perguntas para viabilizar execução
4. Manter código preparado para escalar para dataset completo

**Justificativa:**
- Dataset completo (740 MB de documentos) é muito grande para execução didática
- pubmed.jsonl (583 KB) tem escopo médico/científico alinhado ao projeto
- Subset garante reprodutibilidade e tempo de execução razoável
- Métricas serão estatisticamente significativas mesmo com amostra

## Estrutura do Notebook

### Seção 1: Introdução e Contexto
**Objetivos:**
- Apresentar o problema: Por que RAG é importante na área médica?
- Explicar a arquitetura geral do sistema
- Descrever o dataset e sua estrutura

**Células:**
- Markdown: Introdução ao RAG e sua aplicação em domínio médico
- Markdown: Arquitetura do sistema (diagrama textual)
- Markdown: Estrutura do dataset e métricas de avaliação

### Seção 2: Configuração do Ambiente
**Objetivos:**
- Instalar todas as dependências necessárias
- Configurar credenciais de forma segura
- Validar conectividade com APIs

**Células:**
- Código: Instalação de pacotes (langchain, chromadb, langfuse, deepeval, datasets)
- Código: Carregamento de variáveis de ambiente
- Código: Teste de conectividade com OpenAI e Langfuse

### Seção 3: Aquisição e Exploração de Dados
**Objetivos:**
- Baixar pubmed.jsonl e documents_pool.json do HuggingFace
- Explorar estrutura dos dados (campos, tipos, relações)
- Criar subset otimizado para fins didáticos
- Análise exploratória visual (distribuições, estatísticas)

**Células:**
- Markdown: Explicação sobre o dataset AQ-MedAI/RAG-QA-Leaderboard e estrutura dos arquivos
- Código: Download de pubmed.jsonl usando HuggingFace Hub
- Código: Carregamento e parsing do arquivo JSONL
- Código: Análise inicial (número de queries, campos disponíveis)
- Código: Download de documents_pool.json
- Código: Extração de subset (apenas documentos referenciados por pubmed)
- Código: Análise exploratória visual:
  - Distribuição de tamanho das queries
  - Distribuição de tamanho das respostas (ground_truth)
  - Número de documentos golden vs reference por query
  - Estatísticas de tamanho dos documentos
- Código: Criação de amostra (50-100 queries) para desenvolvimento
- Markdown: Insights sobre a estrutura dos dados e decisões de subset

### Seção 4: Preparação dos Dados e Indexação (Passo 1)
**Objetivos:**
- Preparar documentos do documents_pool.json para indexação
- Implementar estratégia de chunking otimizada
- Gerar embeddings e indexar no vector database
- Preservar metadados (document_id) para validação posterior

**Células:**
- Markdown: Teoria sobre chunking e seus impactos na qualidade do RAG
- Markdown: Explicação sobre preservação de document_id para avaliação de retrieval
- Código: Estruturação dos documentos (texto + metadados com document_id original)
- Código: Implementação do text splitter com parâmetros configuráveis (chunk_size, overlap)
- Código: Visualização de exemplos de chunks gerados
- Código: Estatísticas de chunking (total de chunks, distribuição por documento)
- Markdown: Trade-offs entre chunk_size e qualidade de retrieval
- Código: Geração de embeddings com OpenAI (text-embedding-3-small)
- Código: Criação e população do ChromaDB com metadados preservados
- Código: Validação do índice (query de teste)
- Markdown: Estatísticas finais de indexação (tempo, custo, número de embeddings)

### Seção 5: Implementação do Retriever (Passo 2)
**Objetivos:**
- Implementar função de recuperação
- Testar com diferentes valores de k
- Analisar qualidade dos documentos recuperados

**Células:**
- Markdown: Teoria sobre busca vetorial e similaridade semântica
- Código: Implementação do retriever com decorador @observe (Langfuse)
- Código: Testes com diferentes queries
- Código: Análise de relevância dos documentos recuperados
- Markdown: Discussão sobre parâmetros (k, threshold)

### Seção 6: Gerador de Resposta (Passo 3)
**Objetivos:**
- Criar prompt template restritivo
- Implementar geração de resposta com LLM
- Instrumentar com Langfuse para observabilidade

**Células:**
- Markdown: Estratégias de prompt engineering para evitar alucinações
- Código: Definição do prompt template
- Código: Implementação do gerador com @observe
- Código: Pipeline RAG completo (retrieval + generation)
- Código: Teste end-to-end com exemplos

### Seção 7: Avaliação de Qualidade - Métricas LLM (Passo 4 e 5)
**Objetivos:**
- Implementar métricas Correctness e Faithfulness
- Avaliar respostas geradas vs ground truth
- Visualizar resultados

**Células:**
- Markdown: Teoria sobre LLM-as-a-judge e métricas de qualidade
- Markdown: Explicação detalhada de Correctness (Answer Relevancy)
- Código: Implementação de Answer Relevancy com DeepEval
- Markdown: Explicação detalhada de Faithfulness
- Código: Implementação de Faithfulness com DeepEval
- Código: Execução das avaliações em lote (batch)
- Código: Visualização de resultados (tabelas, gráficos)
- Markdown: Análise dos resultados e insights

### Seção 8: Métricas de Recuperação de Informação (Bônus - Passo 6)
**Objetivos:**
- Implementar Contextual Recall, Precision e Relevancy usando DeepEval
- Avaliar qualidade do retrieval usando golden_doc como referência
- Comparar diferentes configurações (k, chunk_size)
- Análise de Precision@K e Recall@K clássicos

**Células:**
- Markdown: Teoria sobre métricas de recuperação (IR metrics)
- Markdown: Explicação de como usar golden_doc para validação
- Markdown: Diferença entre métricas contextuais (DeepEval) e clássicas (P@K, R@K)
- Markdown: Explicação de Contextual Recall vs Precision vs Relevancy
- Código: Implementação de Contextual Recall com DeepEval
  - Verifica se contexto recuperado cobre informações do expected_output
- Código: Implementação de Contextual Precision com DeepEval
  - Verifica se chunks mais relevantes estão ranqueados no topo
- Código: Implementação de Contextual Relevancy com DeepEval
  - Mede proporção de informação relevante vs ruído
- Código: Implementação de Precision@K e Recall@K clássicos
  - Compara document_ids recuperados com golden_doc
  - Calcula P@K = |retrieved ∩ golden| / K
  - Calcula R@K = |retrieved ∩ golden| / |golden|
- Código: Avaliação comparativa com diferentes valores de k (2, 3, 5, 10)
- Código: Visualização de trade-offs:
  - Curva Precision vs Recall
  - Heatmap de métricas por configuração
  - Gráfico de F1-Score
- Markdown: Análise de resultados:
  - Qual k oferece melhor balanço?
  - Como chunk_size afeta as métricas?
  - Quando usar métricas contextuais vs clássicas?
- Markdown: Recomendações para produção

### Seção 9: Integração com Observabilidade (Langfuse)
**Objetivos:**
- Consolidar traces do Langfuse
- Analisar custos e latências
- Enviar scores do DeepEval para o Langfuse

**Células:**
- Markdown: Modelo de observabilidade (Trace → Span → Generation)
- Código: Execução completa com tracing
- Código: Envio de scores para Langfuse
- Código: Geração de links para dashboard
- Markdown: Instruções para análise no Langfuse Cloud

### Seção 10: Casos Extremos e Limitações
**Objetivos:**
- Demonstrar casos onde o sistema falha
- Mostrar impacto nas métricas
- Discutir limitações e melhorias

**Células:**
- Markdown: Importância de testar edge cases
- Código: Query fora do domínio (teste de alucinação)
- Código: Query ambígua
- Código: Retrieval ruim (k muito baixo)
- Markdown: Análise de métricas nos casos extremos
- Markdown: Limitações do sistema atual

### Seção 11: Pontos de Melhoria para Produção
**Objetivos:**
- Listar melhorias necessárias para produção
- Discutir escalabilidade e performance
- Apresentar alternativas tecnológicas

**Células:**
- Markdown: Diferenças entre protótipo didático e sistema produtivo
- Markdown: Escalabilidade (vector DB distribuído, caching)
- Markdown: Performance (embedding models menores, reranking)
- Markdown: Monitoramento contínuo e A/B testing
- Markdown: Segurança e privacidade em dados médicos

### Seção 12: Conclusões e Próximos Passos
**Objetivos:**
- Resumir resultados obtidos
- Destacar aprendizados principais
- Sugerir extensões do projeto

**Células:**
- Markdown: Resumo dos componentes implementados
- Markdown: Principais aprendizados sobre métricas
- Markdown: Sugestões de próximos passos
- Markdown: Referências e recursos adicionais

## Checklist de Implementação

### Fase 1: Setup Inicial
- [ ] Criar estrutura do notebook com seções
- [ ] Adicionar célula de instalação de dependências
- [ ] Configurar carregamento de variáveis de ambiente

### Fase 2: Dados
- [ ] Implementar download de pubmed.jsonl do HuggingFace
- [ ] Implementar download de documents_pool.json do HuggingFace
- [ ] Parsear pubmed.jsonl e extrair queries, golden_doc, ground_truth
- [ ] Criar dicionário de documents_pool (id -> texto)
- [ ] Extrair subset de documentos (apenas os referenciados por pubmed)
- [ ] Criar amostra de 50-100 queries para desenvolvimento
- [ ] Criar análise exploratória visual
- [ ] Validar integridade dos dados (todos golden_doc existem no pool?)

### Fase 3: Indexação
- [ ] Implementar chunking configurável
- [ ] Gerar e armazenar embeddings
- [ ] Validar índice criado

### Fase 4: RAG Pipeline
- [ ] Implementar retriever com Langfuse
- [ ] Implementar generator com Langfuse
- [ ] Criar pipeline unificado

### Fase 5: Avaliação LLM
- [ ] Implementar Answer Relevancy (Correctness)
- [ ] Implementar Faithfulness
- [ ] Criar visualizações de resultados

### Fase 6: Métricas de Retrieval
- [ ] Implementar Contextual Recall
- [ ] Implementar Contextual Precision
- [ ] Implementar Contextual Relevancy
- [ ] Análise comparativa

### Fase 7: Observabilidade
- [ ] Integrar scores com Langfuse
- [ ] Gerar relatórios de custo/latência
- [ ] Criar links para dashboard

### Fase 8: Refinamento
- [ ] Adicionar casos extremos
- [ ] Documentar limitações
- [ ] Escrever conclusões

## Considerações Técnicas

### Parâmetros Configuráveis
- `chunk_size`: 300-500 caracteres (ajustável)
- `chunk_overlap`: 50-100 caracteres
- `top_k`: 2-5 documentos
- `temperature`: 0.0 (determinístico para avaliação)
- `embedding_model`: text-embedding-3-small

### Visualizações Esperadas
- Distribuição de tamanho de perguntas/respostas
- Distribuição de chunks por documento
- Scores de métricas (barras, heatmaps)
- Trade-off Recall vs Precision
- Custos por query (Langfuse)

### Métricas de Sucesso
- Faithfulness > 0.8 (sem alucinações)
- Answer Relevancy > 0.7 (respostas completas)
- Contextual Recall > 0.6 (contexto suficiente)
- Contextual Precision > 0.5 (chunks relevantes no topo)

## Estilo Didático

### Princípios
1. **Explicar antes de implementar:** Cada conceito tem célula markdown antes do código
2. **Código comentado:** Comentários inline explicando decisões técnicas
3. **Visualização constante:** Mostrar dados, chunks, scores visualmente
4. **Comparações:** Sempre que possível, comparar abordagens diferentes
5. **Casos práticos:** Usar exemplos reais do dataset médico

### Tom de Escrita
- Formal mas acessível
- Evitar jargões sem explicação
- Usar analogias quando apropriado
- Destacar "armadilhas" comuns
- Explicar o "porquê" das decisões técnicas

## Download e Estrutura de Arquivos

### Comandos para Download via HuggingFace Hub

```python
from huggingface_hub import hf_hub_download

# Download de pubmed.jsonl
pubmed_file = hf_hub_download(
    repo_id="AQ-MedAI/RAG-QA-Leaderboard",
    filename="final_data/pubmed.jsonl",
    repo_type="dataset"
)

# Download de documents_pool.json
docs_pool_file = hf_hub_download(
    repo_id="AQ-MedAI/RAG-QA-Leaderboard",
    filename="final_data/documents_pool.json",
    repo_type="dataset"
)
```

### Estrutura Esperada dos Dados

**pubmed.jsonl** (exemplo de registro):
```json
{
  "id": "pubmed_001",
  "query": "What is the role of p53 in cancer?",
  "golden_doc": ["Document_12345", "Document_67890"],
  "reference": ["Document_11111", "Document_22222", "Document_33333"],
  "ground_truth": ["p53 is a tumor suppressor protein that regulates the cell cycle..."]
}
```

**documents_pool.json** (exemplo de estrutura):
```json
{
  "Document_12345": {
    "title": "TP53 Gene",
    "text": "The TP53 gene provides instructions for making a protein called tumor protein p53...",
    "url": "https://en.wikipedia.org/wiki/..."
  },
  "Document_67890": {
    "title": "Cell Cycle Regulation",
    "text": "Cell cycle checkpoints are control mechanisms...",
    "url": "https://en.wikipedia.org/wiki/..."
  }
}
```

### Fluxo de Processamento de Dados

1. **Carregar pubmed.jsonl** → Lista de dicionários com queries
2. **Carregar documents_pool.json** → Dicionário {doc_id: doc_content}
3. **Mapear relações:** Para cada query, resolver golden_doc e reference IDs
4. **Criar subset:** Extrair apenas documentos relevantes para pubmed
5. **Indexar:** Chunkar e embeddar documentos do subset
6. **Avaliar:** Usar golden_doc como ground truth para métricas de retrieval
