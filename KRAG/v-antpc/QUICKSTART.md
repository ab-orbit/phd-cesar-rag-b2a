# 🚀 V-ANTPC Quick Start Guide

**Value Chain Analysis with Networked Triple-Pattern Cognition**

Guia rápido para começar a usar o sistema de Knowledge Graph para análise de cadeias de valor organizacionais.

---

## ⚡ Setup em 3 Passos

### 1. Inicializar Fuseki e Carregar Ontologias

```bash
cd v-antpc
./setup.sh
```

**O que acontece**:
- Inicia Apache Jena Fuseki (Docker) na porta 3030
- Cria dataset RDF chamado `kg`
- Carrega 4 ontologias: e3value, REA, VDML, SCOR

**Resultado esperado**:
```
✓ Fuseki iniciado (porta 3030)
✓ Ontologia 'e3value' carregada: 151 triplas
✓ Ontologia 'rea' carregada: 187 triplas
✓ Ontologia 'vdml' carregada: 203 triplas
✓ Ontologia 'scor' carregada: 165 triplas
✅ SUCESSO!
```

### 2. Explorar a Interface Web

Abra no navegador: **http://localhost:3030**

- **Usuário**: `admin`
- **Senha**: `admin`

**Ações na interface**:
1. Clique em `kg` → **query**
2. Cole uma query SPARQL de `knowledge_graph/sparql_queries/`
3. Clique **Execute** para ver resultados

### 3. Usar via Python

```python
from knowledge_graph.value_chain_federator import ValueChainFederator

# Inicializar
fed = ValueChainFederator()

# Verificar conexão
fed.verificar_conexao()  # ✓ Conectado ao Fuseki

# Listar atores da rede
atores = fed.listar_atores()
for ator in atores:
    print(f"- {ator['uri']}: {ator['tipo']}")

# Executar query SPARQL customizada
results = fed.consultar("""
    SELECT ?ator ?nome
    WHERE {
        ?ator a e3:Actor .
        OPTIONAL { ?ator rdfs:label ?nome }
    }
    LIMIT 10
""")

print(results)
```

---

## 📊 Datasets de Exemplo (APL Têxtil de Pernambuco)

O projeto inclui **3 datasets incrementais** com dados reais do APL Têxtil:

### Parte 1: Camada Econômica (`data/apl_textil_pe_parte1_economico.md`)
- **Ontologias**: e3value + REA
- **Conteúdo**: 9 atores, 9 objetos de valor, 4 trocas, 6 eventos econômicos
- **Casos de Uso**: Análise de fluxos de valor, lucratividade de atores

### Parte 2: Capacidades Estratégicas (`data/apl_textil_pe_parte2_capacidades.md`)
- **Ontologias**: VDML
- **Conteúdo**: 5 capacidades, 2 propostas de valor, 8 atividades, 6 métricas
- **Casos de Uso**: Análise de gaps de desempenho, mapeamento de práticas

### Parte 3: Dinâmica Sistêmica (`data/apl_textil_pe_parte3_sistemica.md`)
- **Ontologias**: SCOR + RVCS
- **Conteúdo**: 4 riscos exponenciais, 3 oportunidades Indústria 6.0, métricas SCOR
- **Casos de Uso**: Simulações what-if, análise de resiliência

---

## 🔍 Queries SPARQL Prontas

### Análise Econômica

**Listar todas as trocas de valor:**
```bash
cat knowledge_graph/sparql_queries/analise_economica.sparql
```

Queries disponíveis:
- ✅ Mapa de atores e trocas
- ✅ Folha de lucratividade por ator
- ✅ Caminhos de dependência
- ✅ Dualidade econômica REA
- ✅ Saldos de recursos
- ✅ Concentração de fornecedores
- ✅ Ciclo caixa-a-caixa

### Análise de Capacidades

```bash
cat knowledge_graph/sparql_queries/analise_capacidades.sparql
```

Queries disponíveis:
- ✅ Mapa de capacidades (core vs support)
- ✅ Propostas de valor
- ✅ Gaps de desempenho
- ✅ Métodos de realização
- ✅ Atividades e recursos
- ✅ Colaborações na rede

### Análise de Supply Chain

```bash
cat knowledge_graph/sparql_queries/analise_supply_chain.sparql
```

Queries disponíveis:
- ✅ Métricas SCOR por atributo
- ✅ Perfect Order Fulfillment
- ✅ Order Cycle Time
- ✅ Flexibilidade upward
- ✅ Fluxo de materiais
- ✅ Análise de estoque
- ✅ Taxa de entrega no prazo

---

## 🎯 Casos de Uso Típicos

### Caso 1: Calcular Lucratividade de um Ator

```python
fed = ValueChainFederator()

# Exemplo: Rota do Mar (fabricante de referência)
resultado = fed.calcular_lucratividade_ator("http://apl-textil.pe/actor/RotaDoMar")

print(f"Receita: R$ {resultado['receita']:,.2f}")
print(f"Custo: R$ {resultado['custo']:,.2f}")
print(f"Lucro: R$ {resultado['lucro']:,.2f}")
print(f"Margem: {resultado['margem_percentual']}%")
```

### Caso 2: Identificar Capacidades Core

```python
capacidades_core = fed.listar_capacidades(apenas_core=True)

for cap in capacidades_core:
    print(f"✓ {cap['descricao']} (Nível {cap['nivel']}/5)")
```

### Caso 3: Analisar Métricas SCOR

```python
metricas = fed.listar_metricas_scor()

for metrica in metricas:
    atual = float(metrica['valor_atual'])
    alvo = float(metrica['valor_alvo'])
    gap = alvo - atual

    print(f"{metrica['metrica']}: {atual} {metrica['unidade']} (meta: {alvo}, gap: {gap})")
```

### Caso 4: Verificar Dualidade Econômica REA

```python
pares_duais = fed.analisar_dualidade_rea()

for par in pares_duais:
    print(f"Incremento: {par['incremento']}")
    print(f"  ↔ Decremento: {par['decremento']}")
    print(f"Recurso: {par['recurso']} ({par['quantidade']})")
    print("---")
```

---

## 📁 Estrutura do Projeto

```
v-antpc/
├── knowledge_graph/
│   ├── ontologies/               # 4 ontologias em Turtle
│   │   ├── e3value.ttl           # Trocas de valor e reciprocidade
│   │   ├── rea.ttl               # Recursos, Eventos, Agentes
│   │   ├── vdml.ttl              # Capacidades e propostas de valor
│   │   └── scor.ttl              # Processos de supply chain
│   ├── sparql_queries/           # Queries prontas
│   │   ├── analise_economica.sparql
│   │   ├── analise_capacidades.sparql
│   │   └── analise_supply_chain.sparql
│   └── value_chain_federator.py  # API Python
├── data/
│   ├── apl_textil_pe_parte1_economico.md
│   ├── apl_textil_pe_parte2_capacidades.md
│   └── apl_textil_pe_parte3_sistemica.md
├── setup.sh                      # Setup automatizado
├── README.md                     # Documentação completa
└── QUICKSTART.md                 # Este arquivo
```

---

## 🛠️ Comandos Úteis

### Verificar status do Fuseki
```bash
curl http://localhost:3030/$/ping
```

### Ver logs do Fuseki
```bash
docker logs -f fuseki
```

### Parar Fuseki
```bash
docker stop fuseki
```

### Reiniciar Fuseki
```bash
docker restart fuseki
```

### Limpar todos os dados (reset total)
```bash
docker rm -f fuseki
./setup.sh
```

### Estatísticas do grafo
```python
from knowledge_graph.value_chain_federator import ValueChainFederator

fed = ValueChainFederator()
stats = fed.estatisticas_grafo()

print(f"Total de triplas: {stats['total_triplas']}")
print(f"Classes: {stats['total_classes']}")
print(f"Atores: {stats['total_atores']}")
print(f"Capacidades: {stats['total_capacidades']}")
```

---

## 🆘 Troubleshooting

### Problema: "Connection refused" ao conectar ao Fuseki

**Solução**: Verificar se Docker está rodando e se Fuseki iniciou corretamente
```bash
docker ps | grep fuseki
# Se não aparecer nada, execute:
./setup.sh
```

### Problema: Ontologias não carregam (0 triplas)

**Solução**: Verificar se arquivos .ttl existem
```bash
ls -lh knowledge_graph/ontologies/
# Devem aparecer: e3value.ttl, rea.ttl, vdml.ttl, scor.ttl
```

### Problema: Query retorna vazio mesmo com dados

**Solução**: Verificar prefixes na query
```sparql
PREFIX e3: <http://e3value.com/ontology#>
PREFIX rea: <http://www.reo.org/ontology#>
PREFIX vdml: <http://www.omg.org/spec/VDML/>
PREFIX scor: <http://www.apics.org/scor#>
```

---

## 📚 Próximos Passos

1. **Carregar dados do APL**: Converter datasets .md para triplas RDF
2. **Criar visualizações**: Usar PyVis para grafos interativos
3. **Implementar análises RVCS**: Camadas 3 e 4 do framework
4. **Criar Digital Twin**: Simulações what-if em tempo real

---

**Projeto Didático — PHD em Ciência de Dados**
César Cunha — 2026
