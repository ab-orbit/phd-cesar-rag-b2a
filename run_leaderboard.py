import os
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

# Setup Langfuse
langfuse = Langfuse()
handler_de_observabilidade = CallbackHandler()

print("1. Baixando e preparando amostra de dados...")
# Lendo 5 perguntas do dataset Pubmed (AQ-MedAI/RAG-QA-Leaderboard final_data)
df_pubmed = pd.read_json('hf://datasets/AQ-MedAI/RAG-QA-Leaderboard/final_data/pubmed.jsonl', lines=True)
amostra_qa = df_pubmed.head(5).to_dict(orient='records')
print(f"-> {len(amostra_qa)} perguntas selecionadas.")

# Precisamos do pool de documentos para as referências dessas perguntas
todas_referencias = set()
for item in amostra_qa:
    # item['reference'] contém a lista dos IDs reais de documentos atrelados a resposta
    for doc_id in item.get('reference', []):
        todas_referencias.add(doc_id)

print(f"-> Buscando textos de {len(todas_referencias)} documentos relevantes no pool gigante...")

documents_map = {}
with fsspec.open('hf://datasets/AQ-MedAI/RAG-QA-Leaderboard/final_data/documents_pool.json', 'r') as f:
    pool_gigante = json.load(f)
    for doc_id in todas_referencias:
        if doc_id in pool_gigante:
            # O JSON aparentemente tem 'title' e 'content'
            documents_map[doc_id] = pool_gigante[doc_id].get('content', '')

print(f"-> Textos recuperados. Iniciando o Pipeline RAG...")

# Preparando o ChromaDB
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
textos_brutos = list(documents_map.values())
CHUNKS = text_splitter.create_documents(textos_brutos)

motor_de_embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vector_db = Chroma.from_documents(CHUNKS, motor_de_embeddings)
buscador = vector_db.as_retriever(search_kwargs={"k": 3})

# Pipeline
@observe(as_type="span", name="Busca_Chroma")
def buscar_materiais(query: str):
    chunks = buscador.invoke(query)
    return [c.page_content for c in chunks]

@observe(as_type="generation", name="Gerador_Resposta")
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

@observe(name="Sessao_AQ_MedAI")
def rodar_teste_unitario(query: str):
    evs = buscar_materiais(query)
    ans = formular_resposta(query, evs)
    return evs, ans

print("\n2. Avaliando Amostras e Gerando Test Cases para DeepEval...")
test_cases = []

for idx, item in enumerate(amostra_qa):
    q = item['query']
    ground_truth = str(item['ground_truth'])
    print(f"\n[{idx+1}/5] Pergunta: {q[:50]}...")
    
    # RAG Execution
    evs_recover, generated_ans = rodar_teste_unitario(q)
    print(f"     Resposta Esperada: {ground_truth[:50]}...")
    print(f"     Resposta do LLM: {generated_ans[:50]}...")
    
    tc = LLMTestCase(
        input=q,
        actual_output=generated_ans,
        expected_output=ground_truth,
        retrieval_context=evs_recover
    )
    test_cases.append(tc)

langfuse.flush()

print("\n3. Executando Juízes LLM (DeepEval)...")
metrica_relev = AnswerRelevancyMetric(threshold=0.5, model="gpt-4o")
metrica_faith = FaithfulnessMetric(threshold=0.5, model="gpt-4o")
metrica_recall = ContextualRecallMetric(threshold=0.5, model="gpt-4o")
metrica_precis = ContextualPrecisionMetric(threshold=0.5, model="gpt-4o")

resultados = evaluate(
    test_cases=test_cases,
    metrics=[metrica_relev, metrica_faith, metrica_recall, metrica_precis],
    print_results=False
)

print("\n==== RESUMO DA AVALIAÇÃO DA AMOSTRA ====")
try:
    for res in resultados:
        print(f"\nItem Baseado na Pergunta: {res.input[:30]}...")
        if res.success:
            print(" ✅ STATUS GERAL: SUCESSO")
        else:
            print(" ❌ STATUS GERAL: FALHA")
            
        for d in res.metrics_data:
            print(f"   -> {d.name} | Score: {d.score} | Sucesso: {d.is_successful}")
        print("-" * 50)
except Exception as e:
    print(f"Não foi possível imprimir o formato do DeepEval 1.4: {e}")
    print(resultados)

