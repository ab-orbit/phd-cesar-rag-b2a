import os
import json
from dotenv import load_dotenv
from langfuse import Langfuse

# Carregar variáveis de ambiente (LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY, LANGFUSE_HOST)
load_dotenv()

# Inicializar o cliente Langfuse
langfuse = Langfuse()

print("Buscando traces recentes...")
try:
    # Acessar a API para buscar traces (usando o SDK)
    # Procuramos os traces associados ao nome 'Pipeline_AQ_MedAI' ou 'Sessao_AQ_MedAI' que usamos nos scripts
    traces = langfuse.fetch_traces(
        name="Pipeline_AQ_MedAI",
        limit=5 # pegando os 5 testes que fizemos
    )
    
    if traces.data:
        print(f"Encontrados {len(traces.data)} traces com nome Pipeline_AQ_MedAI")
    else:
        print("Buscando por Sessao_AQ_MedAI...")
        traces = langfuse.fetch_traces(
            name="Sessao_AQ_MedAI",
            limit=5
        )
        print(f"Encontrados {len(traces.data)} traces com nome Sessao_AQ_MedAI")
    
    if not traces.data:
        print("Buscando qualquer trace recente...")
        traces = langfuse.fetch_traces(limit=2)
        print(f"Encontrados {len(traces.data)} traces gerais")

    if traces.data:
        first_trace = traces.data[0]
        print(f"\\nExemplo de Trace ID: {first_trace.id}")
        print(f"Tokens In: {first_trace.total_cost}") # só pra ver quais atributos existem
        
        # O SDK v4 pode ter mudado a estrutura do objeto, vamos inspecionar
        print("\\nAtributos disponiveis no objeto Trace:")
        print(dir(first_trace))
        
except Exception as e:
    print(f"Erro ao buscar traces: {e}")

