from langfuse import observe, Langfuse
from langfuse.langchain import CallbackHandler
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

import os
from dotenv import load_dotenv
load_dotenv()

handler = CallbackHandler()

@observe(as_type="span", name="VectorDB_Retrieval_Event")
def buscar(query):
    return ["Evidencia 1"]

@observe(as_type="generation", name="LLM_Formulator")
def formular(query, evidences):
    modelo = ChatOpenAI(model="gpt-4o-mini", temperature=0.0) 
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Responda a pergunta com base nas evidencias: {informacao_bruta}"),
        ("user", "{duvida}")
    ])
    cadeia = prompt | modelo
    resposta = cadeia.invoke(
        {"informacao_bruta": "\\n".join(evidences), "duvida": query},
        config={"callbacks": [handler]}
    )
    return resposta.content

@observe(as_type="trace", name="Sessao_Usuario_RAG")
def pipeline(query):
    ev = buscar(query)
    ans = formular(query, ev)
    return ans

print(pipeline("Test?"))
Langfuse().flush()
print("Done")
