# Planejamento Didático: Sistema RAG Avaliado com Métricas Reconhecidas e Observabilidade

Este planejamento foi desenhado em um formato de *To-Do List*, com o objetivo de construir, passo a passo, a infraestrutura de Recuperação Aumentada por Geração (RAG), garantindo que todo o código seja extremamente legível, didático e focado na aferição contínua da qualidade das soluções através de métricas estabelecidas pela literatura.

O repositório baseia-se na implementação orientada por **LangChain** ou **LlamaIndex**, aliado ao uso sistemático do framework **DeepEval** para avaliação (LLM-as-a-judge) e do **Langfuse** para observabilidade e rastreabilidade (*traceability*).

---

## 📚 Fase 1: Estudo, Fundamentação e Preparação do Ambiente
O objetivo desta etapa é garantir o embasamento teórico usando os materiais disponíveis e criar um ambiente que favoreça a explicação de cada passo, incluindo as novas ferramentas analíticas.

- [x] **1.1. Revisão da Literatura Base**
  - [x] Ler e extrair conceitos de `anatomia-rag.pdf` (Foco nas etapas: Ingestion, Retrieval, Generation).
  - [x] Revisar `anatomia_recuperacao_informacao.pdf` (Entender busca vetorial/semântica vs léxica).
  - [x] Revisar `guia-fund-como-maquias-encontram-respostas.pdf` (Compreender Embeddings e Espaços Vetoriais).
- [x] **1.2. Revisão da Literatura de Avaliação e Observabilidade**
  - [x] Revisar conceitos do **DeepEval**: Métricas de RAG (Answer Relevancy, Faithfulness, Contextual Precision/Recall/Relevancy).
  - [x] Revisar conceitos do **Langfuse**: Modelo de Dados de Observabilidade (Trace $\rightarrow$ Span $\rightarrow$ Generation).
- [x] **1.3. Configuração do Ambiente Didático**
  - [x] Criar ambiente virtual (`venv` ou `conda`) e documentar instruções no README.
  - [x] Instalar dependências base (`langchain`, `llama-index`, `chromadb`/`faiss-cpu`).
  - [x] Instalar as bibliotecas de LLMOps: `pip install deepeval langfuse`.
  - [x] Configurar chaves de API (OpenAI API Key). Registrar conta no Langfuse Cloud (ou local) e salvar as variáveis de ambiente (`LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, `LANGFUSE_HOST`).

## 🗂️ Fase 2: Aquisição e Preparação de Dados (Data Ingestion)
Lidar com bases de QA do HuggingFace e preparar os *Test Cases* para a avaliação.

- [x] **2.1. Carga dos Dados Referência**
  - [x] Baixar dados do HuggingFace (`AQ-MedAI/RAG-QA-Leaderboard`).
  - [x] Explicar a estrutura do dataset, pontuando a separação lógica em:
    - *Input* (A pergunta original do usuário).
    - *Expected Output / Ground Truth* (A resposta ideal esperada).
    - *Context / Reference* (O corpus de dados sobre o qual a base foi construída).
- [x] **2.2. Chunking e Indexação (Passo 1 da Spec)**
  - [x] Segmentar documentos (Text Chunking). *Didática: Explicar o impacto do `chunk_size` no Contextual Recall*.
  - [x] Gerar Embeddings e persistir numa Vector Database (Ex: ChromaDB).

## 🔍 Fase 3: RAG Core Pipeline com Rastreabilidade (Traceability)
Implementando o encadeamento principal, instrumentando as chamadas com **Langfuse** para evidenciar exatamente o tempo gasto e o custo atrelado a cada componente.

- [x] **3.1. Rastreando a Aplicação (Modelo de Dados Langfuse v4)**
  - [x] Inicializar o cliente e decoradores importando diretamente do `langfuse`.
  - [x] *Didática:* Criar e explicar um **Trace** principal que representará toda a execução da RQA. (No novo Langfuse v4+, o `@observe()` sem `as_type` cria a raiz OpenTelemetry).
- [x] **3.2. Implementar e Rastrear o Retriever (Passo 2 da Spec)**
  - [x] Construir a classe/função de `Retriever`. 
  - [x] *Didática:* Instrumentar a função de busca como um **Span** (ou *Observation*) ligado ao Trace principal, medindo a latência da busca vetorial pura num Vector DB.
- [x] **3.3. Implementar e Rastrear o Gerador de Resposta (Passo 3 da Spec)**
  - [x] Construir o prompt (Template) focado em Restrição de Conhecimento.
  - [x] Instanciar LLM chamando a API (OpenAI ou modelo Local).
  - [x] *Didática:* Instrumentar a chamada do LLM como um **Generation**, atrelado ao Trace, com o `CallbackHandler` em `langfuse.langchain`. Adicionar o passo explícito de `.flush()` no objeto do `Langfuse()` central no término da requisição assíncrona.

## ⚖️ Fase 4: Avaliação Sistêmica Baseada no DeepEval (Passo 4 e 5)
Este é o ápice da aferição de qualidade do modelo que foi arquitetado, agora adotando o Framework estruturado do DeepEval. 

- [x] **4.1. Transição para Test Cases do DeepEval**
  - [x] Transformar os dados recuperados da Fase 2 e os Outputs da Fase 3 em objetos `LLMTestCase` da biblioteca `deepeval`. Estes objetos devem mapear de forma inequívoca o trio: `input`, `actual_output`, `expected_output` e `retrieval_context`.
- [x] **4.2. Métricas Baseadas na Qualidade da Geração (LLM Metrics)**
  - [x] Implementar e rodar o avaliador de **Answer Relevancy**: Medir o grau em que a saída final penaliza respostas incompletas ou excessivamente prolixas em relação à pergunta, independentemente dos construtos factuais (baseado nas docs de *Answer Relevancy*).
  - [x] Implementar e rodar o avaliador de **Faithfulness (Fidelidade)**: Validar contra alucinações. O LLM como Juiz verificará se cada "Claim" contido no `actual_output` é diretamente sustentado pelo `retrieval_context`.
- [x] **4.3. Métricas Qualitativas Baseadas na Recuperação da Informação (Context Metrics)**
  - [x] Implementar **Contextual Recall**: Avaliar se os pedaços (Chunks) retornados e contidos na janela de contexto englobam suficientemente os ensinamentos necessários da resposta ideal (`expected_output`).
  - [x] Implementar **Contextual Precision**: Ponderar qualitativamente se os chunks com maior poder informativo (que satisfazem a resposta teórica) foram colocados nas primeiras posições (*rank-awareness*) comparado aos ruidosos.
  - [x] Implementar **Contextual Relevancy**: Determinar se evitamos "inchar" o context window medindo a proporção de linhas que são de fato úteis aos *retrievals* contra o ruído irrelevante trazido.
- [x] **4.4. Integrar as Avaliações com a Observabilidade Langfuse**
  - [x] Enviar os scores (`Score`, `Reason`) tabulados pelo DeepEval como "Scores" (avaliações quantitativas) de volta à execução (`Trace`) dentro do Langfuse. *Didática: Exibir que testagem unitária contínua e dashboards de monitoramento andam juntos*.

## 🎓 Fase 5: Refinamento Didático Final e Elucidação
Passos voltados puramente a garantir a expansão do conhecimento de terceiros que consumirão este código.

- [x] **5.1. Código Pythônico e Explicativo**
  - [x] Garantir tipagem forte nas funções de rastreamento.
  - [x] Adicionar Docstrings narrando como "Contextual Recall difere do Precision" baseado nas leituras do DeepEval e Evidently.
- [x] **5.2. Casos Extremos (Edge Cases)**
  - [x] Criar um exemplo no notebook forçando um Retriever ruim.
  - [x] Mostrar por métrica: Como o Contextual Recall cai para 0.0 na interface do Langfuse/DeepEval caso não retornemos partes fundamentais.
- [x] **5.3. Dashboardização**
  - [x] Printar os links finais (`UI url` do Langfuse Trace) na saída do código de modo terminal interativo, levando as pessoas até o painel web que mostra todas as fases e tokens de custo, além dos pareceres qualitativos julgados pelo DeepEval.
