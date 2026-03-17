# Knowledge Graph Federado (v-antgvt)

Este diretório contém a implementação do mecanismo de **Knowledge Graph Semântico Federado** concebido para a estruturação e análise de domínios organizacionais, focado em Cadeias de Valor Industriais (com dados de exemplo do APL Têxtil de Pernambuco).

A arquitetura extrai conhecimento de textos (arquivos Markdown), converte em triplas (Sujeito-Predicado-Objeto) através de LLMs, identifica o alinhamento com ontologias de negócios globais (VDML, REA, e3value), e permite a validação humana e visualização dessas redes.

---

## 🏗 Arquitetura do Sistema

O mecanismo opera em uma esteira de cinco subsistemas sequenciais:

1. **`ingester.py` (Ingestão e Extração):** 
   Lê roteiros e documentações Markdown (`.md`), os quebra em partes menores (*chunks*) e utiliza o LangChain acoplado ao modelo da OpenAI para extrair triplas estruturadas respeitando os vocabulários da arquitetura empresarial (consome, produz, fomenta, etc.).
   
2. **`federator.py` (Federação de Ontologias):**
   Mapeia e carrega múltiplas bibliotecas e ontologias num único construto (RDFLib ou endpoint SPARQL). As ontologias integradas neste escopo são:
   * **e3value:** Focado na reciprocidade e modelo de negócio (Ator, Objeto de valor).
   * **REA:** Focado na dualidade das trocas (Recurso, Evento, Agente).
   * **VDML:** Focado nas promessas e capacidades da rede (Capability, Business Network).
   * **kg_custom:** Ontologia própria para metadados de governança.

3. **`detector.py` (Detecção de Ocorrências e Novidades):**
   Checa cada termo extraído no texto via SPARQL contra as ontologias do `federator.py`. Se a entidade não constar nos catálogos formais (ex: "Facção de Costura" ou "Sebrae"), ela é inserida no grafo e classificada com o *status* de `Candidato`.

4. **`validator.py` (Governança e Validação):**
   Recupera a lista de nós `Candidatos`. Permite que um humano ou analista valide, conecte essa entidade a uma classe pai oficial (`skos:exactMatch`) e emita uma atualização (`kgmeta:Aprovado`). Permite também a exportação da nova versão da ontologia formatada (`.ttl`).

5. **`visualizer.py` (Renderização de Grafos):**
   Consulta todas as arestas e nós em memória, gerando uma interface gráfica HTML interativa utilizando a biblioteca *PyVis*, diferenciando a coloração por status (e.g. validado, candidato, etc).

---

## 📂 Visão Geral dos Diretórios

```text
v-antgvt/
├── dados_exemplo/               # Textos de entrada (Raw text info)
│   ├── contexto_cadeia_valor.md # Resumo base de Cadeia de Valor 
│   ├── apl_textil_pe_parte1.md  # Roteiro: Governança do APL
│   ├── apl_textil_pe_parte2.md  # Roteiro: Facções e Produção
│   └── apl_textil_pe_parte3.md  # Roteiro: Comercialização e Eventos
├── knowledge_graph/             # Core da solução semântica
│   ├── ontologias/              # Arquivos locais TTL carregados no Federador
│   ├── ingester.py
│   ├── federator.py
│   ├── detector.py
│   ├── validator.py
│   └── visualizer.py
└── notebooks/
    └── Tutorial_KG_Federado.ipynb # Jupyter Notebook auto-explicativo do pipeline
```

---

## 🚀 Como Executar

### Pré-requisitos
Certifique-se de que o Python esteja instalado e suas dependências estejam presentes (idealmente em um ambiente virtual):

```bash
pip install -r requirements.txt
```

### Orquestração via Pipeline (Jupyter)
O fluxo principal é orquestrado através do Jupyter Notebook, que documenta cada etapa do carregamento à renderização gráfica.

1. Exporte sua API Key da OpenAI, que será necessária na etapa do `ingester`:
   ```bash
   export OPENAI_API_KEY="sk-SuaChaveAqui"
   ```
2. Inicialize a interface visual:
   ```bash
   jupyter notebook notebooks/Tutorial_KG_Federado.ipynb
   ```
3. Acompanhe a execução por blocos (Shift + Enter). 
4. Ao final, a célula **Visualização Interativa** vai salvar o mapa em formato `kg_viz.html` na raiz deste diretório e projetá-lo no celular/tela do Jupyter. 

### Customizando a Base (APL Têxtil)
O Notebook aponta por padrão para `dados_exemplo/contexto_cadeia_valor.md`. Para extrair informações complexas da governança do Pólo Têxtil de Pernambuco, edite a célula de extração no Jupyter alterando a leitura para:

```python
ingester = IngesterMarkdown("dados_exemplo/apl_textil_pe_parte2.md", ...)
```

E veja em tempo real as relações entre Atacadistas, Facções Familiares e Lavanderias se formando no Grafo Visual.

---

## Notas de Evolução (Próximos Passos)
A implementação local atua via `rdflib` para ser independente, garantindo escalabilidade didática. Para clusters em produção massiva de dados (extending into Indústria 6.0), sugere-se acoplar a classe `FederadorOntologias` com endereçamentos a Data Stores orientados a Grafos robustos (Jena Fuseki, QLever, Blazegraph) via parâmetro de endpoint.
