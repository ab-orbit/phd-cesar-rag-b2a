# V-ANTPC: Value Chain Analysis with Networked Triple-Pattern Cognition

**Versão Auto-Contida do KRAG para Análise de Cadeias de Valor Organizacionais**

## 🎯 Contexto

Este projeto implementa o **Framework RVCS** (Rede de Valor Cognitiva-Sistêmica) proposto para superação da miopia estratégica em cadeias de valor industriais da Indústria 6.0.

### Domínio: Ambientes Organizacionais Complexos em Rede

Diferente do KRAG biomédico, este projeto modela:
- **Cadeias de Valor Globais (GVC)** como Sistemas Adaptativos Complexos
- **Ecossistemas organizacionais** com múltiplos atores (fornecedores, parceiros, competidores)
- **Fluxos de valor** (recursos, capacidades, atividades)
- **Riscos exponenciais** e oportunidades da Indústria 6.0

## 🏗️ Arquitetura RVCS (4 Camadas)

```
┌─────────────────────────────────────────────────────────┐
│  CAMADA 4: INTELIGÊNCIA COGNITIVA                       │
│  (Digital Twin + DIKWP)                                 │
│  - Monitoramento em tempo real                          │
│  - Predição de cenários what-if                         │
│  - Alinhamento com propósito ESG                        │
└────────────────┬────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────┐
│  CAMADA 3: DINÂMICA SISTÊMICA                           │
│  (GVC-CAS + GRASP)                                      │
│  - Modelagem como Sistema Adaptativo Complexo          │
│  - Identificação de pontos de alavancagem              │
│  - Resiliência e antifragilidade                       │
└────────────────┬────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────┐
│  CAMADA 2: CAPACIDADE ESTRATÉGICA                       │
│  (VDML + SCOR)                                          │
│  - Mapeamento de capacidades críticas                  │
│  - Métodos de entrega de valor                         │
│  - Métricas de desempenho e custo                      │
└────────────────┬────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────┐
│  CAMADA 1: ONTOLOGIA ECONÔMICA                          │
│  (e3value + REA)                                        │
│  - Atores e objetos de valor                           │
│  - Reciprocidade e dualidade econômica                 │
│  - Viabilidade financeira de redes                     │
└─────────────────────────────────────────────────────────┘
```

## 📚 Ontologias Implementadas

### Camada 1 - Ontologias de Negócios

| Ontologia | URI Base | Escopo |
|-----------|----------|--------|
| **e3value** | `http://e3value.com/ontology#` | Trocas de valor em redes de negócios, reciprocidade, viabilidade |
| **REA** | `http://www.reo.org/ontology#` | Recursos, Eventos, Agentes - dualidade econômica |
| **VDML** | `http://www.omg.org/spec/VDML/` | Value Delivery Modeling Language (OMG standard) |
| **SCOR** | `http://www.apics.org/scor#` | Supply Chain Operations Reference Model |

### Camada 2 - Ontologias de Infraestrutura

- **PROV-O**: Proveniência de decisões estratégicas
- **ORG**: Estrutura organizacional (W3C)
- **SKOS**: Taxonomias de capacidades
- **Schema.org**: Entidades gerais (Organization, Person, Event)

### Camada 3 - Namespace Customizado

```turtle
@prefix vc:     <http://valuechain.org/ontology#> .
@prefix rvcs:   <http://rvcs-framework.org/ontology#> .
```

## 🚀 Quick Start

### 1. Setup Fuseki

```bash
cd v-antpc
./setup.sh
```

### 2. Executar Tutorial

```bash
jupyter notebook notebooks/Tutorial_ValueChain_Analysis.ipynb
```

### 3. Uso Programático

```python
from knowledge_graph.value_chain_federator import ValueChainFederator
from knowledge_graph.rvcs_analyzer import RVCSAnalyzer

# Carregar ontologias de valor
federator = ValueChainFederator()
federator.load_all_ontologies()

# Analisar cadeia de valor
analyzer = RVCSAnalyzer()
analysis = analyzer.analyze_value_network("automotive_supply_chain.md")

# Gerar relatório de riscos e oportunidades
report = analyzer.generate_rvcs_report()
print(report)
```

## 📊 Casos de Uso

1. **Análise de Viabilidade de Parcerias**: Usar e3value para calcular fluxos de valor
2. **Mapeamento de Capacidades**: VDML para identificar gaps estratégicos
3. **Gestão de Riscos Exponenciais**: Análise CAS de pontos de inflexão
4. **Economia Circular**: Modelar fluxos reversos de recursos (REA)
5. **Digital Twins**: Simulação what-if de mudanças na cadeia

## 📁 Estrutura do Projeto

```
v-antpc/
├── knowledge_graph/
│   ├── ontologies/              # Ontologias em Turtle
│   │   ├── e3value.ttl
│   │   ├── rea.ttl
│   │   ├── vdml.ttl
│   │   ├── scor.ttl
│   │   └── rvcs_custom.ttl
│   ├── models/                  # Modelos Python
│   │   ├── layer1_economic.py
│   │   ├── layer2_strategic.py
│   │   ├── layer3_systemic.py
│   │   └── layer4_cognitive.py
│   ├── value_chain_federator.py
│   ├── rvcs_analyzer.py
│   └── sparql_queries/
├── data/
│   └── automotive_supply_chain_example.md
├── notebooks/
│   └── Tutorial_ValueChain_Analysis.ipynb
├── config/
│   └── fuseki_config.ttl
├── setup.sh
└── README.md
```

## 🎓 Conceitos Pedagógicos

### e3value: Reciprocidade em Redes
- **Interface de Valor**: Trocas atômicas entre atores
- **Folhas de Lucratividade**: Análise de viabilidade financeira
- **Dependências**: Identificação de riscos em parcerias

### REA: Dualidade Econômica
- **Inflow/Outflow**: Para cada recebimento, um fornecimento
- **Scripts Empresariais**: Conversão de recursos
- **Rastreabilidade**: Proveniência de ativos

### VDML: Integração Estratégica
- **CapabilityMethod**: Ponte entre estratégia e processos
- **9 Requisitos**: Framework completo para valor
- **Agregação Multinível**: Do operacional ao estratégico

### GRASP: Alavancagem Sistêmica
- **Goals**: Alinhamento hierárquico de metas
- **Resources**: Habilitadores vs. criadores de valor
- **Actions**: Pontos de alta alavancagem
- **Structure**: Governança de rede
- **People**: Competências e cultura

## 📚 Referências

Baseado no documento:
**"Arquitetura Sistêmica e Ontológica da Cadeia de Valor Industrial: Um Framework Integrado para Superação da Miopia Estratégica, Mitigação de Riscos Exponenciais e Exploração de Oportunidades na Indústria 6.0"**

---

**Projeto Didático — PHD em Ciência de Dados**
César Cunha — 2026
