from typing import List, Tuple
from pydantic import BaseModel
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from rdflib import URIRef, Literal
from .federator import KG, KGMETA, MESH, CHEBI, HPO, DRON

class Tripla(BaseModel):
    sujeito: str
    tipo_sujeito: str
    predicado: str
    objeto: str
    tipo_objeto: str
    trecho_original: str
    confianca: float

class ListaTriplas(BaseModel):
    triplas: list[Tripla]

class IngesterMarkdown:
    """
    Lê um arquivo Markdown, segmenta em chunks contextuais
    e extrai triplas RDF via LLM
    """

    def __init__(self, caminho_md: str, base_dir: str = "."):
        import os
        self.caminho_md = os.path.join(base_dir, caminho_md)
        # Using a default or mock LLM configuration. In production, need API key.
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)

    def carregar_chunks(self) -> List[str]:
        """Lê MD e segmenta."""
        with open(self.caminho_md, "r", encoding="utf-8") as f:
            texto = f.read()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100
        )
        return splitter.split_text(texto)

    def extrair_triplas(self, chunk: str) -> List[Tripla]:
        """
        Extrai triplas usando o LLM com output estruturado.
        """
        prompt = f"""
Você é um extrator de conhecimento de arquitetura empresarial e cadeia de valor industrial. Analise o texto abaixo e extraia
TODAS as relações factuais na forma de triplas (sujeito, predicado, objeto).

REGRAS:
- Use termos padronizados de ontologias de negócios (VDML, e3value, REA) quando possível
- Predicados devem ser relacionais e adequados a arquitetura empresarial: consome, produz, fornece, recebe, integra, mitiga, etc.
- Inclua o trecho exato do texto
- Estime sua confiança de 0.0 a 1.0

TEXTO:
{{chunk}}
"""
        llm_with_tools = self.llm.with_structured_output(ListaTriplas)
        try:
            resultado = llm_with_tools.invoke(prompt)
            return resultado.triplas
        except Exception as e:
            print(f"Erro na extração: {e}")
            return []

    def mapear_para_ontologia(self, tripla: Tripla) -> Tuple:
        """
        Mapeia a Tripla Pydantic para tupla RDFLib simples.
        Na implementação completa, buscaria via SPARQL.
        """
        # Mapeamento estático e simples para o exemplo didático
        s = URIRef(KG[tripla.sujeito.replace(" ", "_")])
        p = URIRef(KG[tripla.predicado.replace(" ", "_")])
        o = URIRef(KG[tripla.objeto.replace(" ", "_")])
        
        return (s, p, o)
