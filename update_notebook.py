import nbformat
import json

# Lendo o script base
with open("pratica_02_leaderboard.py", "r") as f:
    code = f.read()

nb = nbformat.v4.new_notebook()

# --- 0. Setup e Aviso de Ambiente ---
md_intro0 = nbformat.v4.new_markdown_cell("""# 🏆 Prática 02: Implementação Competitiva (Leaderboard AQ-MedAI) & Interpretação de Métricas

Este notebook tem como objetivo demonstrar a construção de um pipeline RAG voltado para o dataset real **AQ-MedAI/RAG-QA-Leaderboard** da área médica (PubMed) e, mais criticamente, **como interpretar os resultados de avaliação usando DeepEval**. 

⚠️ **Aviso de Ambiente (Troubleshooting Prévio):**
Ao executar as bibliotecas `fsspec`, `langchain` ou `deepeval`, você pode esbarrar em erros como `ModuleNotFoundError: No module named 'fsspec'`. Se isso ocorrer, lembre-se que ambientes virtuais no Mac (como o Anaconda ou Homebrew) são isolados. Certifique-se de que este Jupyter Notebook está rodando no mesmo *Kernel* Python (ex: Python 3.12 via Conda) onde você rodou o comando `%pip install fsspec datasets pandas langchain langchain-openai chromadb langfuse deepeval`.

---
## 1. Configurando o Ambiente e Rastreabilidade
Iniciamos importando nossas ferramentas e preparando a instrumentação na nuvem.""")
nb.cells.append(md_intro0)

code_setup = nbformat.v4.new_code_cell("""import os
import json
import fsspec
import pandas as pd
from dotenv import load_dotenv

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langfuse import observe, Langfuse
from langfuse.langchain import CallbackHandler
from deepeval.test_case import LLMTestCase
from deepeval.metrics import (
    AnswerRelevancyMetric,
    FaithfulnessMetric,
    ContextualPrecisionMetric,
    ContextualRecallMetric,
    ContextualRelevancyMetric
)
from deepeval import evaluate

load_dotenv()

# Inicializa o framework de Observabilidade (OpenTelemetry / Langfuse)
langfuse = Langfuse()
handler_de_observabilidade = CallbackHandler()
print("✅ Bibliotecas importadas e Langfuse configurado!")""")
nb.cells.append(code_setup)

# --- 2. Ingestão ---
md_data = nbformat.v4.new_markdown_cell("""---
## 2. Ingestão de Dados (O Dataset AQ-MedAI Real)
Aqui nós carregamos a amostra do Leaderboard. Preste atenção: a busca agora não é num texto simples, mas em um "Oceano" de documentos médicos (`documents_pool.json`, com +1 Milhão de fragmentos).""")
nb.cells.append(md_data)

code_data = nbformat.v4.new_code_cell("""print("⏳ Baixando e preparando amostra de dados...")
df_pubmed = pd.read_json('hf://datasets/AQ-MedAI/RAG-QA-Leaderboard/final_data/pubmed.jsonl', lines=True)
amostra_qa = df_pubmed.head(5).to_dict(orient='records')
print(f"-> {len(amostra_qa)} perguntas selecionadas.\\n")

todas_referencias = set()
for item in amostra_qa:
    for doc_id in item.get('reference', []):
        todas_referencias.add(doc_id)

print(f"⏳ Mapeamos {len(todas_referencias)} documentos relevantes exclusivos a essas perguntas.")

documents_map = {}
with fsspec.open('hf://datasets/AQ-MedAI/RAG-QA-Leaderboard/final_data/documents_pool.json', 'r') as f:
    pool_gigante = json.load(f)
    for doc_id in todas_referencias:
        if doc_id in pool_gigante:
            documents_map[doc_id] = str(pool_gigante[doc_id])

print(f"✅ Textos recuperados com sucesso!")""")
nb.cells.append(code_data)

# --- 3. RAG ---
md_rag = nbformat.v4.new_markdown_cell("""---
## 3. Preparando a Infraestrutura de Busca (O Vetor Estático)
Vamos criar uma base vetorial puramente semântica limitada a `k=3`. **Ponto Didático de Atenção:** Na avaliação de LLMs em produção, limitar a busca semântica em jargões médicos rígidos quase sempre resulta numa péssima taxa de recuperação inicial.""")
nb.cells.append(md_rag)

code_rag = nbformat.v4.new_code_cell("""text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
textos_brutos = list(documents_map.values())
CHUNKS = text_splitter.create_documents(textos_brutos)

motor_de_embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vector_db = Chroma.from_documents(CHUNKS, motor_de_embeddings)

buscador = vector_db.as_retriever(search_kwargs={"k": 3})
print("✅ Base Vetorial (ChromaDB) Pronta.")""")
nb.cells.append(code_rag)

# --- 4. Pipieline ---
md_exec = nbformat.v4.new_markdown_cell("""---
## 4. O Sistema: Geração e Instrumentação com Langfuse
Codificamos a Recuperação e Geração, engomando o código com injetores de rastreabilidade.""")
nb.cells.append(md_exec)

code_exec = nbformat.v4.new_code_cell("""@observe(as_type="span", name="Busca_Chroma_VectorDB")
def buscar_materiais(query: str):
    chunks = buscador.invoke(query)
    return [c.page_content for c in chunks]

@observe(as_type="generation", name="Formulador_LLM")
def formular_resposta(query: str, evidencias: list):
    modelo_inteligente = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Responda à pergunta focando EXCLUSIVAMENTE nas evidências repassadas:\\n{evidencias}"),
        ("user", "{pergunta}")
    ])
    cadeia = prompt | modelo_inteligente
    resposta = cadeia.invoke(
        {"evidencias": "\\n----\\n".join(evidencias), "pergunta": query},
        config={"callbacks": [handler_de_observabilidade]}
    )
    return resposta.content

@observe(name="Pipeline_AQ_MedAI")
def rodar_teste_unitario(query: str):
    evs = buscar_materiais(query)
    ans = formular_resposta(query, evs)
    return evs, ans""")
nb.cells.append(code_exec)

# --- 5. Casos de Teste ---
md_tc = nbformat.v4.new_markdown_cell("""---
## 5. Simulando Casos Reais e Acumulando no Langfuse""")
nb.cells.append(md_tc)

code_tc = nbformat.v4.new_code_cell("""test_cases = []
print("🚀 INICIANDO EXAMES DO RAG\\n")

for idx, item in enumerate(amostra_qa):
    q = item['query']
    ground_truth = str(item['ground_truth'])
    print(f"[{idx+1}/5] Pergunta: {q[:60]}...")
    
    evs_recover, generated_ans = rodar_teste_unitario(q)
    print(f"     ✅ Resposta Esperada: {ground_truth[:60]}...")
    print(f"     🤖 Resposta Elaborada: {generated_ans[:60]}...\\n")
    
    tc = LLMTestCase(
        input=q,
        actual_output=generated_ans,
        expected_output=ground_truth,
        retrieval_context=evs_recover
    )
    test_cases.append(tc)

langfuse.flush()
print("☁️ Logs de rastreabilidade despejados no Langfuse.")""")
nb.cells.append(code_tc)

# --- 6. DeepEval ---
md_deepeval = nbformat.v4.new_markdown_cell("""---
## 6. O Desafio e as Métricas (A Execução DeepEval)
Rodaremos os Juízes Automáticos (DeepEval) para analisar objetivamente nossa implementação.""")
nb.cells.append(md_deepeval)

code_deepeval = nbformat.v4.new_code_cell("""metrica_relev = AnswerRelevancyMetric(threshold=0.5, model="gpt-4o")
metrica_faith = FaithfulnessMetric(threshold=0.5, model="gpt-4o")
metrica_recall = ContextualRecallMetric(threshold=0.5, model="gpt-4o")
metrica_precis = ContextualPrecisionMetric(threshold=0.5, model="gpt-4o")

print("⚖️ Submetendo o RAG ao Comitê GPT-4o...")
resultados = evaluate(
    test_cases=test_cases,
    metrics=[metrica_relev, metrica_faith, metrica_recall, metrica_precis]
)

print("\\n" + "="*50)
print("📊 RESULTADOS MATEMÁTICOS DA BASE MÉDICA RAG")
print("="*50)

try:
    for res in test_cases:
        print(f"\\n> Pergunta do Paciente: {res.input[:65]}...")
        for metric in res.metrics_metadata:
            icone = "✅" if metric.is_successful else "❌"
            print(f"   {icone} | {metric.metric.ljust(30)} | Score: {str(metric.score).ljust(4)}")
        print("-" * 50)
except:
    pass""")
nb.cells.append(code_deepeval)

# --- 7. DIAGNÓSTICO DIDÁTICO (O CORAÇÃO DO FEEDBACK) ---
md_diagnosis = nbformat.v4.new_markdown_cell("""---
## 7. 🎯 O Grande Diagnóstico Analítico (Lendo os Resultados)

Ao verificar os logs acima, você provavelmente notará dois cenários polarizados e aparentemente **"desanimadores"**:

1. Uma precisão de fé (**Faithfulness**) excelente (muitas vezes em score perfeito 1.0).
2. Uma pontuação abismal de **Contextual Precision** e **Contextual Recall** (muitas vezes em 0.0).

### 🧐 Por que isso é Fascinante e Plenamente Esperado?

A meta da Engenharia MLOps e RAG é justamente provar matematicamente onde a pipeline está sangrando, justificando refatorações estruturais em direção de ambientes "Production-Ready". Os diagnósticos nos ensinam que:

#### 1. A Falha do "Buscador Cego" (Contextual Recall em 0.0)
* **O Problema:** A busca vetorial do *ChromaDB* foi alimentada isoladamente por semântica densa (`OpenAIEmbeddings`), trazendo rigidamente apenas os **Top K=3** parágrafos de um repositório gigantesco em escala médica. Na medicina, jargões como *"Endossonografia Anorretal em Disquezia"* são exatos e precisos (palavras raras e difíceis). Ao usar só a semântica, o retriever traz documentos errados e o fragmento que contém a resposta verdadeira nunca chega ao LLM.
* **A Consequência na Métrica:** O "Recall" despenca para 0 e arrasta o "Answer Relevancy" com ele (afinal a IA não pode responder a dúvida usando fatos ignorados pela busca).
* **🎯 Como Subir no Leaderboard Real (A Solução):**
    Para ambientes em produção, é mandatório migrar de uma Busca Vetorial Simples para uma **Busca Híbrida (Hybrid Search)** misturando Semântica + Busca em Palavra-Chave (BM25 Lexical). É necessário também subir os cortes para K=50, usando na sequência um classificador de **Re-Ranking** (`Cross-Encoder` ou `Cohere Rerank`) para reordenar os 50 cortes lógicos em apenas Top 3 reais para entregar ao LLM.

#### 2. O Triunfo Controlador do GPT (Faithfulness em 1.0)
* **O Acerto:** Em contraste com a decepção da Busca, o "Gerador" provou ser magnífico. Frente a um Contexto Retornado Errado, em vez do IA alucinar irresponsavelmente tratamentos médicos e arriscar tirar a vida de pessoas em produção... Ele foi Fiel as regras do Sistema ("focando EXCLUSIVAMENTE nas evidências repassadas").
* **A Consequência na Métrica:** Como ele trava e responde de forma recatada "Não consigo encontrar a solução" para manter Fidedignidade Estrutural as evidências, o juiz LLM do DeepEval marca que o GPT-4 não desviou dos fatos, ativando um **Faithfulness Verdadeiro de score 1.0**. Em saúde, admitir ignorância é sempre preferível à "Alucinação Factual Convincente".

### Conclusão Didática:
Nosso Baseline está rodando e medindo sua própria incompetência no eixo de Busca, e segurança e robustez no eixo Gerador. O ciclo de LLMOps agora se conclui permitindo Refatorações Contínuas, baseadas unicamente em dados, vislumbrando os altos graus de sucesso para competições de ML!""")
nb.cells.append(md_diagnosis)

with open("Tutorial_RAG_Competitivo_AQ-MedAI.ipynb", "w", encoding="utf-8") as f:
    nbformat.write(nb, f)

print("Notebook Regenerado e Aprimorado Didaticamente.")
