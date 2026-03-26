# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a didactic RAG (Retrieval-Augmented Generation) system implementation for a PhD data science course. The project focuses on building an evaluated, observable RAG pipeline using medical/pharmaceutical Q&A data, with emphasis on quality metrics and traceability.

**Primary Goal:** Educational implementation demonstrating RAG components with comprehensive evaluation metrics - NOT production-ready scalability or performance optimization.

## Technology Stack

### Core RAG Framework
- **LangChain** (`langchain`, `langchain-openai`): Primary orchestration framework for prompts, chains, and LLM integrations
- **ChromaDB** (`chromadb`): Local vector database for semantic search
- **OpenAI APIs**:
  - Embeddings: `text-embedding-3-small`
  - LLM: `gpt-4o-mini` (temperature=0.0 for deterministic responses)

### LLMOps & Evaluation
- **Langfuse** (`langfuse`): Observability platform for tracing, monitoring costs, and latency
  - Implements hierarchical model: Trace → Span → Generation
  - Tracks token usage and financial costs per request
- **DeepEval** (`deepeval`): LLM-as-a-judge evaluation framework for RAG metrics
  - Answer Relevancy, Faithfulness (hallucination detection)
  - Contextual Recall, Precision, Relevancy

### Data & Utilities
- `datasets`, `pandas`: Dataset loading and manipulation
- `python-dotenv`: Environment variable management

## Environment Setup

### Required Environment Variables
Configure in `.env` file (see `.env.example`):
```
OPENAI_API_KEY=""
LANGFUSE_SECRET_KEY=""
LANGFUSE_PUBLIC_KEY=""
LANGFUSE_HOST=""
```

### Installation
```bash
pip install langchain langchain-openai chromadb langfuse datasets pandas deepeval ratelimit nest_asyncio
```

Or execute the first cell in `Tutorial_RAG_Fases_1_a_3.ipynb`.

## Project Architecture

### RAG Pipeline Flow (Phases 1-3)

1. **Data Ingestion (Fase 2)**
   - Dataset source: HuggingFace `AQ-MedAI/RAG-QA-Leaderboard` (medical Q&A)
   - Structure: `input` (question) + `context` (source text) + `expected_output` (ground truth)
   - **Chunking Strategy:**
     - `RecursiveCharacterTextSplitter` with `chunk_size=150`, `chunk_overlap=30`
     - Overlap prevents semantic loss at chunk boundaries
   - Embeddings generated via `OpenAIEmbeddings` and stored in ChromaDB

2. **Retriever Component (Fase 3.1)**
   - Vector similarity search (cosine similarity)
   - Default: `k=2` top documents retrieved
   - Instrumented as Langfuse **Span** for I/O performance tracking

3. **Generator Component (Fase 3.2)**
   - **Prompt Engineering:** Restrictive template to minimize hallucinations
   - System prompt enforces: "Answer ONLY from provided EVIDENCE, otherwise state insufficient data"
   - Instrumented as Langfuse **Generation** to track token consumption and costs

4. **Unified Pipeline (Fase 3.3)**
   - Orchestrated via `@observe(as_type="trace")` decorator
   - Full request lifecycle: Query → Retrieval → Generation → Response
   - `langfuse_context.flush()` required after execution to send telemetry

### Evaluation Framework (Fase 4 - Planned)

Uses DeepEval with `LLMTestCase` objects mapping:
- `input`: User query
- `actual_output`: RAG-generated response
- `expected_output`: Ground truth from dataset
- `retrieval_context`: Retrieved chunks

**Generation Metrics (LLM-as-judge):**
- **Answer Relevancy**: Measures completeness and conciseness relative to question
- **Faithfulness**: Validates claims in `actual_output` are supported by `retrieval_context`

**Retrieval Metrics (Context Quality):**
- **Contextual Recall**: Do retrieved chunks contain information needed for ideal answer?
- **Contextual Precision**: Are highest-value chunks ranked first? (rank-aware)
- **Contextual Relevancy**: Ratio of useful vs. irrelevant content in context window

Scores sent back to Langfuse Traces for unified dashboard visualization.

## Key Implementation Patterns

### Langfuse Observability Decorators
```python
@observe(as_type="trace", name="Sessao_Usuario_RAG")
def pipeline_rag_unificado(query: str):
    # Entire RAG session

@observe(as_type="span", name="VectorDB_Retrieval_Event")
def buscar_materiais_do_banco(query: str):
    # Isolated retrieval operation

@observe(as_type="generation", name="LLM_Formulator")
def formular_resposta(query: str, evidencias: list):
    # LLM call with callback handler
    config={"callbacks": [handler_de_observabilidade]}
```

### Hallucination Prevention Strategy
- Temperature set to 0.0 for deterministic outputs
- Explicit system prompt constraint: respond only from provided evidence
- Evaluation via Faithfulness metric (Fase 4) to detect knowledge leakage

### Chunking Rationale
- Small chunk size (150 chars) is **intentionally didactic** - creates high multiplicity for learning
- Production systems would use larger chunks (512-1024 tokens)
- Overlap (30 chars) prevents narrative breaks at boundaries

## Development Workflow

### Working with Jupyter Notebook
The main implementation is in `Tutorial_RAG_Fases_1_a_3.ipynb`:
- Executes sequentially from top to bottom
- Markdown cells explain concepts before code cells
- Educational format: concepts → implementation → validation

### Monitoring Executions
1. Run RAG pipeline in notebook
2. Execute `langfuse_context.flush()` to send telemetry
3. Visit [Langfuse Dashboard](https://cloud.langfuse.com/)
4. Navigate to **Traces** → `Sessao_Usuario_RAG`
5. Inspect hierarchical breakdown:
   - Token counts (prompt vs completion)
   - Latency per component
   - Financial cost per request
   - Full prompt/response content

## Reference Documentation

### Foundational PDFs (in `content/`)
- `anatomia-rag.pdf`: RAG stages (Ingestion, Retrieval, Generation)
- `anatomia_recuperacao_informacao.pdf`: Vector vs lexical search theory
- `guia-fund-como-maquias-encontram-respostas.pdf`: Embeddings and vector spaces

### Planning Documents
- `planejamento_didatico_rag.md`: 5-phase didactic roadmap with checklist
- `spec-pratica-02.md`: Project specification and requirements

### External Resources
- RAG Benchmarks: https://www.evidentlyai.com/blog/rag-benchmarks
- Dataset: https://huggingface.co/datasets/AQ-MedAI/RAG-QA-Leaderboard

## Important Constraints

1. **Not Production-Focused:**
   - No scalability requirements
   - No performance optimization expected
   - Intentionally uses small data samples
   - Document points for production improvement

2. **Quality Metrics Are Critical:**
   - DeepEval metrics must be explained in detail
   - All evaluation decisions must be justified
   - Traceability via Langfuse is mandatory

3. **Educational Emphasis:**
   - Code must be extremely readable and well-documented
   - Docstrings should explain conceptual differences (e.g., "Contextual Recall vs Precision")
   - Include edge cases demonstrating metric failures

4. **Project Language:**
   - Code comments and variable names in Portuguese
   - Markdown explanations in Portuguese
   - Technical terms may use English equivalents
