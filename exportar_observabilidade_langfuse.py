import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
secret_key = os.getenv("LANGFUSE_SECRET_KEY")
# O .env está cadastrado como LANGFUSE_BASE_URL (US Cloud)
host = os.getenv("LANGFUSE_BASE_URL", "https://cloud.langfuse.com")

if not public_key or not secret_key:
    print("ERRO: Chaves do Langfuse não encontradas no .env")
    exit(1)

print(f"📡 Conectando à API REST do Langfuse em {host}...")

# Endpoint para buscar Traces
url = f"{host}/api/public/traces"

# Queremos pegar nossos traces associados à execução do script competitivo
params = {
    "name": "Pipeline_AQ_MedAI",
    "limit": 5, 
    "orderBy": "timestamp.desc"
}

response = requests.get(url, auth=(public_key, secret_key), params=params)

if response.status_code == 200:
    data = response.json()
    traces = data.get("data", [])
    print(f"✅ Encontrados {len(traces)} traces executados!")

    resumo_execucao = []
    
    for t in traces:
        trace_id = t["id"]
        trace_name = t["name"]
        
        # Pega as observations (Gerações LLM e Spans) atreladas a este Trace
        obs_url = f"{host}/api/public/observations?traceId={trace_id}"
        obs_response = requests.get(obs_url, auth=(public_key, secret_key))
        
        obs_data = []
        if obs_response.status_code == 200:
            obs_data = obs_response.json().get("data", [])
        
        # Agregadores de Custos e Tokens para a sessão toda (Trace)
        total_tokens_in = 0
        total_tokens_out = 0
        total_cost_usd = 0.0
        
        for obs in obs_data:
            if obs.get("type") == "GENERATION":
                usage = obs.get("usage", {})
                if usage:
                    total_tokens_in += usage.get("promptTokens", 0)
                    total_tokens_out += usage.get("completionTokens", 0)
                    total_cost_usd += usage.get("totalCost", 0.0)
        
        # Consolidando o relatório
        resumo_execucao.append({
            "trace_id": trace_id,
            "tarefa": trace_name,
            "data_execucao": t.get("timestamp"),
            "input_pergunta": t.get("input"),
            "output_resposta": t.get("output"),
            "latencia_total_segundos": t.get("latency"),
            "custo_openai_usd": total_cost_usd,
            "tokens_in_prompt": total_tokens_in,
            "tokens_out_resposta": total_tokens_out,
            "etapas_rastreadas": [o.get("name") for o in obs_data]
        })

    # Salvando em um JSON formatado
    output_path = "Relatorio_Custos_Langfuse.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(resumo_execucao, f, indent=4, ensure_ascii=False)
        
    print(f"\\n🎉 Relatório de Execução, Custos e Tokens extraído com sucesso!")
    print(f"Arquivo salvo em: {output_path}")

else:
    print(f"❌ Falha na conexão com a API:")
    print(response.status_code, response.text)
