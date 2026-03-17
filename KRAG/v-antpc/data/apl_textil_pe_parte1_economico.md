# APL Têxtil de Pernambuco - Parte 1: Camada Econômica
## Dataset Incremental para Knowledge Graph Federado

> **Fonte de Dados**: Pesquisa sobre o Arranjo Produtivo Local (APL) Têxtil do Agreste de Pernambuco
> **Ontologias Aplicadas**: e3value (trocas de valor) + REA (fluxos econômicos)
> **Objetivo**: Modelar atores, objetos de valor, trocas e eventos econômicos da cadeia têxtil

---

## 1. ATORES DA REDE DE VALOR

### 1.1 Fabricantes (Manufacturers)

**Rota do Mar** (`actor:RotaDoMar`)
- **Tipo**: e3:Actor, rea:Manufacturer
- **Localização**: Santa Cruz do Capibaribe, PE
- **Descrição**: Empresa de referência no setor de confecções do Agreste, fundada em 1996
- **Produção Anual**: 1.000.000 de peças
- **Especialização**: Moda casual, jeans, moda praia
- **Porte**: Médio
- **Responsabilidade P&L**: Independente

**Polo Toritama Jeans** (`actor:PoloToritamaJeans`)
- **Tipo**: e3:MarketSegment, rea:Manufacturer
- **Localização**: Toritama, PE
- **Descrição**: Agregação de 3.000+ empresas de moda especializadas em jeans
- **Produção Anual**: 60.000.000 de peças de jeans (15% da produção nacional)
- **Especialização**: Jeans, denim, lavanderia industrial (50+ lavanderias)
- **Porte**: Cluster
- **Número de Empresas**: >3.000

**Confecções Caruaru Ltda** (`actor:ConfecoesCaruaru`)
- **Tipo**: e3:Actor, rea:Manufacturer
- **Localização**: Caruaru, PE
- **Descrição**: Fabricante de moda infantil e lingerie
- **Produção Anual**: 500.000 peças
- **Especialização**: Moda infantil, lingerie, moda íntima
- **Porte**: Pequeno-Médio

### 1.2 Fornecedores (Suppliers)

**Tecelagem São Paulo SA** (`actor:TecelagemSP`)
- **Tipo**: e3:Actor, rea:Supplier, scor:Supplier
- **Localização**: São Paulo, SP (Região Sudeste)
- **Descrição**: Fornecedor de tecidos planos de algodão e poliéster
- **Participação de Mercado**: Parte dos 86,5% de fornecedores de tecidos do Sudeste/Sul
- **Produtos Principais**: Tecidos planos, popeline, brim, sarja

**Linhas & Elásticos Catarinense** (`actor:LinhasElasticosSC`)
- **Tipo**: e3:Actor, rea:Supplier, scor:Supplier
- **Localização**: Santa Catarina, SC (Região Sul)
- **Descrição**: Fornecedor de linhas de costura e elásticos
- **Participação de Mercado**: Parte dos 82,5% de fornecedores de linhas e 76,6% de elásticos do Sul/Sudeste
- **Produtos Principais**: Linhas de poliéster, elásticos de cós, elásticos de acabamento

**Embalagens Nordeste** (`actor:EmbalagemNordeste`)
- **Tipo**: e3:Actor, rea:Supplier
- **Localização**: Recife, PE
- **Descrição**: Fornecedor regional de embalagens plásticas e etiquetas
- **Produtos Principais**: Sacos plásticos, etiquetas, tags

### 1.3 Distribuidores e Varejo

**Feira da Sulanca Caruaru** (`actor:FeiraSulancaCaruaru`)
- **Tipo**: e3:Actor, scor:Distributor
- **Localização**: Caruaru, PE
- **Descrição**: Centro de compras atacadista que comercializa 800 milhões de peças/ano do APL
- **Modelo**: Atacado para lojistas de todo Brasil
- **Volume Anual**: ~800.000.000 de peças (APL inteiro)

**Distribuidora Nacional de Moda** (`actor:DistribuidoraNacional`)
- **Tipo**: e3:Actor, scor:Distributor
- **Descrição**: Distribuidor atacadista com alcance nacional
- **Mercados Atendidos**: Norte, Nordeste, Centro-Oeste
- **Volume de Compra Mensal**: 100.000 peças

### 1.4 Clientes Finais

**Lojistas Regionais** (`actor:LojistasRegionais`)
- **Tipo**: e3:MarketSegment, scor:Customer
- **Descrição**: Agregação de pequenos lojistas que compram no atacado para revenda
- **Quantidade Estimada**: 50.000+ lojistas
- **Ticket Médio de Compra**: R$ 5.000 a R$ 20.000

**Consumidor Final** (`actor:ConsumidorFinal`)
- **Tipo**: e3:MarketSegment, scor:Customer
- **Descrição**: Consumidor final de produtos do APL em todo território nacional

### 1.5 Entidades de Governança

**NTCPE - Núcleo Gestor da Cadeia Têxtil** (`actor:NTCPE`)
- **Tipo**: e3:Actor (não econômico, mas coordenador)
- **Localização**: Pernambuco
- **Descrição**: Entidade que desenvolve estratégias para crescimento sustentável da cadeia têxtil de PE
- **Papel**: Governança, articulação, desenvolvimento de políticas públicas
- **Responsabilidades**: Coordenação de ações, fomento à formalização, acesso a mercados

---

## 2. OBJETOS DE VALOR (Value Objects)

### 2.1 Matérias-Primas (Inputs)

**Tecido Plano de Algodão** (`valueObject:TecidoPlanoAlgodao`)
- **Tipo**: e3:ValueObject, rea:RawMaterial, scor:RawMaterial
- **Unidade de Medida**: metros
- **Valor Econômico Médio**: R$ 12,00/metro
- **Origem**: 86,5% Sudeste/Sul
- **Aplicação**: Camisas, vestidos, calças sociais

**Tecido Denim (Jeans)** (`valueObject:TecidoDenim`)
- **Tipo**: e3:ValueObject, rea:RawMaterial, scor:RawMaterial
- **Unidade de Medida**: metros
- **Valor Econômico Médio**: R$ 18,00/metro
- **Origem**: Sudeste/Sul
- **Aplicação**: Calças jeans, jaquetas jeans

**Linhas de Costura** (`valueObject:LinhasCostura`)
- **Tipo**: e3:ValueObject, rea:RawMaterial
- **Unidade de Medida**: cones (5000 metros/cone)
- **Valor Econômico Médio**: R$ 25,00/cone
- **Origem**: 82,5% Sul/Sudeste

**Elástico de Cós** (`valueObject:ElasticoCos`)
- **Tipo**: e3:ValueObject, rea:RawMaterial
- **Unidade de Medida**: metros
- **Valor Econômico Médio**: R$ 3,50/metro
- **Origem**: 76,6% Sul/Sudeste

**Embalagens Plásticas** (`valueObject:EmbalagemPlastica`)
- **Tipo**: e3:ValueObject, rea:RawMaterial
- **Unidade de Medida**: unidades
- **Valor Econômico Médio**: R$ 0,20/unidade
- **Origem**: 84,7% Sul/Sudeste (mas NTCPE tem fornecedor regional)

### 2.2 Produtos Acabados (Outputs)

**Calça Jeans Acabada** (`valueObject:CalcaJeans`)
- **Tipo**: e3:Product, rea:FinishedGood, scor:FinishedGood
- **Unidade de Medida**: peças
- **Custo de Produção**: R$ 35,00/peça
- **Preço de Venda (Atacado)**: R$ 55,00/peça
- **Margem de Valor**: R$ 20,00/peça
- **Volume Anual (Toritama)**: 60.000.000 peças

**Roupa Casual (Camisetas, Vestidos)** (`valueObject:RoupaCasual`)
- **Tipo**: e3:Product, rea:FinishedGood, scor:FinishedGood
- **Unidade de Medida**: peças
- **Custo de Produção**: R$ 15,00/peça
- **Preço de Venda (Atacado)**: R$ 25,00/peça
- **Margem de Valor**: R$ 10,00/peça
- **Volume Anual (APL)**: ~400.000.000 peças (estimativa)

**Moda Infantil** (`valueObject:ModaInfantil`)
- **Tipo**: e3:Product, rea:FinishedGood
- **Unidade de Medida**: peças
- **Custo de Produção**: R$ 12,00/peça
- **Preço de Venda (Atacado)**: R$ 20,00/peça
- **Margem de Valor**: R$ 8,00/peça

**Lingerie** (`valueObject:Lingerie`)
- **Tipo**: e3:Product, rea:FinishedGood
- **Unidade de Medida**: peças
- **Custo de Produção**: R$ 8,00/peça
- **Preço de Venda (Atacado)**: R$ 15,00/peça
- **Margem de Valor**: R$ 7,00/peça

### 2.3 Dinheiro (Money)

**Real Brasileiro (BRL)** (`valueObject:DinheiroBRL`)
- **Tipo**: e3:Money, rea:Cash
- **Unidade de Medida**: BRL (R$)
- **Função**: Meio de troca nas transações econômicas

---

## 3. TROCAS DE VALOR (Value Exchanges)

### 3.1 Troca 1: Compra de Tecido Denim

**Troca**: `exchange:CompraTecidomDenimRotaDoMar`
- **Tipo**: e3:ValueExchange, rea:Exchange
- **Atores Envolvidos**:
  - **Provedor (outflow)**: `actor:TecelagemSP`
  - **Receptor (inflow)**: `actor:RotaDoMar`

**Interface de Valor do Fornecedor** (`valueInterface:TecelagemSP_VendaDenim`):
- **Porta de Saída 1**: Oferece `valueObject:TecidoDenim` (10.000 metros/mês)
- **Porta de Entrada 1**: Solicita `valueObject:DinheiroBRL` (R$ 180.000,00/mês)

**Interface de Valor do Fabricante** (`valueInterface:RotaDoMar_CompraDenim`):
- **Porta de Entrada 1**: Recebe `valueObject:TecidoDenim` (10.000 metros/mês)
- **Porta de Saída 1**: Paga `valueObject:DinheiroBRL` (R$ 180.000,00/mês)

**Reciprocidade**: Atômica - ou ambos os fluxos ocorrem, ou nenhum ocorre

### 3.2 Troca 2: Compra de Linhas de Costura

**Troca**: `exchange:CompraLinhasRotaDoMar`
- **Tipo**: e3:ValueExchange, rea:Exchange
- **Atores Envolvidos**:
  - **Provedor**: `actor:LinhasElasticosSC`
  - **Receptor**: `actor:RotaDoMar`

**Interface de Valor**:
- **Outflow (Fornecedor)**: `valueObject:LinhasCostura` (200 cones/mês = R$ 5.000,00)
- **Inflow (Fabricante)**: `valueObject:DinheiroBRL` (R$ 5.000,00)

### 3.3 Troca 3: Venda de Jeans Acabado ao Distribuidor

**Troca**: `exchange:VendaJeansDistribuidor`
- **Tipo**: e3:ValueExchange, rea:Exchange
- **Atores Envolvidos**:
  - **Provedor**: `actor:PoloToritamaJeans`
  - **Receptor**: `actor:DistribuidoraNacional`

**Interface de Valor do Polo** (`valueInterface:Toritama_VendaJeans`):
- **Porta de Saída**: Oferece `valueObject:CalcaJeans` (100.000 peças/mês)
- **Porta de Entrada**: Solicita `valueObject:DinheiroBRL` (R$ 5.500.000,00/mês)

**Interface de Valor do Distribuidor**:
- **Porta de Entrada**: Recebe `valueObject:CalcaJeans` (100.000 peças/mês)
- **Porta de Saída**: Paga `valueObject:DinheiroBRL` (R$ 5.500.000,00/mês)

### 3.4 Troca 4: Venda de Moda Casual à Feira da Sulanca

**Troca**: `exchange:VendaCasualFeiraSulanca`
- **Tipo**: e3:ValueExchange
- **Atores Envolvidos**:
  - **Provedor**: `actor:RotaDoMar`
  - **Receptor**: `actor:FeiraSulancaCaruaru`

**Interface de Valor**:
- **Outflow**: `valueObject:RoupaCasual` (50.000 peças/mês)
- **Inflow**: `valueObject:DinheiroBRL` (R$ 1.250.000,00/mês)

---

## 4. EVENTOS ECONÔMICOS (REA Events)

### 4.1 Evento de Decremento: Fornecimento de Tecido

**Evento**: `event:FornecimentoDenimTecelagemSP_Jan2026`
- **Tipo**: rea:DecrementEvent
- **Agente Provedor**: `actor:TecelagemSP`
- **Recurso Afetado**: `valueObject:TecidoDenim`
- **Quantidade**: -10.000 metros
- **Valor Monetário**: R$ 180.000,00
- **Data**: 2026-01-15
- **Direção StockFlow**: OUT

### 4.2 Evento de Incremento: Recebimento de Tecido

**Evento**: `event:RecebimentoDenimRotaDoMar_Jan2026`
- **Tipo**: rea:IncrementEvent
- **Agente Receptor**: `actor:RotaDoMar`
- **Recurso Afetado**: `valueObject:TecidoDenim`
- **Quantidade**: +10.000 metros
- **Data**: 2026-01-15
- **Direção StockFlow**: IN

**Dualidade**: `event:FornecimentoDenimTecelagemSP_Jan2026` ↔ `event:RecebimentoDenimRotaDoMar_Jan2026`

### 4.3 Evento de Decremento: Consumo de Tecido na Produção

**Evento**: `event:ConsumoTecidoProducaoRotaDoMar_Jan2026`
- **Tipo**: rea:DecrementEvent (transformação manufatureira)
- **Agente**: `actor:RotaDoMar`
- **Recurso Consumido**: `valueObject:TecidoDenim`
- **Quantidade**: -8.000 metros (convertidos em 2.500 calças jeans)
- **Data**: 2026-01-20
- **Processo Relacionado**: scor:Make (Manufacturing Process)

### 4.4 Evento de Incremento: Produção de Jeans Acabado

**Evento**: `event:ProducaoJeansRotaDoMar_Jan2026`
- **Tipo**: rea:IncrementEvent (resultado de transformação)
- **Agente**: `actor:RotaDoMar`
- **Recurso Criado**: `valueObject:CalcaJeans`
- **Quantidade**: +2.500 peças
- **Data**: 2026-01-25
- **Valor Agregado**: R$ 87.500,00 (R$ 35,00/peça x 2.500)

**Script de Processo**: rea:ManufacturingProcess (Conversão de matéria-prima + trabalho → produto acabado)

### 4.5 Evento de Decremento: Venda de Jeans

**Evento**: `event:VendaJeansDistribuidor_Fev2026`
- **Tipo**: rea:DecrementEvent
- **Agente Provedor**: `actor:PoloToritamaJeans`
- **Recurso Afetado**: `valueObject:CalcaJeans`
- **Quantidade**: -100.000 peças
- **Valor Monetário**: R$ 5.500.000,00
- **Data**: 2026-02-01

### 4.6 Evento de Incremento: Recebimento de Pagamento

**Evento**: `event:RecebimentoPagamentoToritama_Fev2026`
- **Tipo**: rea:IncrementEvent
- **Agente Receptor**: `actor:PoloToritamaJeans`
- **Recurso Afetado**: `valueObject:DinheiroBRL`
- **Quantidade**: +R$ 5.500.000,00
- **Data**: 2026-02-05 (pagamento a prazo, 4 dias após entrega)

**Dualidade**: `event:VendaJeansDistribuidor_Fev2026` ↔ `event:RecebimentoPagamentoToritama_Fev2026`

---

## 5. MÉTRICAS ECONÔMICAS (KPIs)

### 5.1 Viabilidade Econômica (e3value Profitability Sheet)

**Lucratividade - Rota do Mar (Mensal)**:
- **Receita de Vendas**: R$ 1.375.000,00 (25.000 peças x R$ 55,00)
- **Custo de Matéria-Prima**:
  - Tecido: R$ 180.000,00
  - Linhas: R$ 5.000,00
  - Elástico: R$ 8.000,00
  - Embalagens: R$ 5.000,00
  - **Total**: R$ 198.000,00
- **Custo de Transformação**: R$ 485.000,00 (mão de obra + overhead)
- **Lucro Líquido**: R$ 692.000,00
- **Margem de Lucro**: 50,3%

**Lucratividade - Polo Toritama Jeans (Mensal - Agregado)**:
- **Receita de Vendas**: R$ 275.000.000,00 (5M peças x R$ 55,00)
- **Custo Total**: R$ 175.000.000,00
- **Lucro Líquido Agregado**: R$ 100.000.000,00
- **Margem de Lucro**: 36,4%

### 5.2 Saldos de Recursos (REA Current Balance)

**Estoque de Tecido Denim - Rota do Mar**:
- **Saldo Inicial (01/01/2026)**: 5.000 metros
- **Incremento (Compra)**: +10.000 metros
- **Decremento (Produção)**: -8.000 metros
- **Saldo Atual (31/01/2026)**: 7.000 metros

**Estoque de Jeans Acabado - Polo Toritama**:
- **Saldo Inicial**: 500.000 peças
- **Incremento (Produção Mensal)**: +5.000.000 peças
- **Decremento (Vendas)**: -4.800.000 peças
- **Saldo Atual**: 700.000 peças

### 5.3 Fluxo de Caixa (Cash-to-Cash Cycle)

**Ciclo Caixa-a-Caixa - Rota do Mar**:
- **Dias de Pagamento a Fornecedores (DPO)**: 30 dias
- **Dias de Produção**: 15 dias
- **Dias de Recebimento de Clientes (DSO)**: 45 dias
- **Ciclo Total**: 30 dias (DSO + Produção - DPO = 45 + 15 - 30)

**Implicação**: Rota do Mar precisa financiar 30 dias de capital de giro

---

## 6. DEPENDÊNCIAS E CAMINHOS DE VALOR

### 6.1 Caminho de Dependência: "Produção de Jeans"

**Start Stimulus**: `stimulus:DemandaJeansConsumidorFinal`
- **Tipo**: e3:StartStimulus
- **Descrição**: Necessidade de 100.000 consumidores por calças jeans de qualidade a preço acessível

**Dependency Path**: `dependencyPath:CadeiaProducaoJeans`
1. `exchange:CompraTecidomDenimRotaDoMar` → Fabricante adquire matéria-prima
2. `event:ConsumoTecidoProducaoRotaDoMar_Jan2026` → Transformação em produto
3. `event:ProducaoJeansRotaDoMar_Jan2026` → Geração de valor
4. `exchange:VendaJeansDistribuidor` → Entrega ao mercado

**End Stimulus**: `stimulus:SatisfacaoCliente`
- **Tipo**: e3:EndStimulus
- **Descrição**: Consumidor final vestido com jeans de qualidade, fabricante lucrativo

### 6.2 Riscos de Dependência

**Risco 1: Concentração Geográfica de Fornecedores**
- **Descrição**: 86,5% dos fornecedores de tecido estão no Sudeste/Sul
- **Impacto**: Se ocorrer greve de transportadoras ou aumento de frete, toda cadeia para
- **Criticidade**: ALTA

**Risco 2: Pagamento a Prazo**
- **Descrição**: Ciclo caixa-a-caixa de 30 dias expõe fabricantes a risco de liquidez
- **Impacto**: Pequenas empresas sem capital de giro podem quebrar com inadimplência
- **Criticidade**: MÉDIA

---

## FONTES DE DADOS

Este dataset foi elaborado com base em pesquisas sobre o APL Têxtil de Pernambuco:

- [NTCPE - Núcleo Gestor de Cadeia Têxtil e de Confecções](https://ntcpe.org.br/)
- [Polo de Confecções do Agreste](http://especiais.leiaja.com/descosturandoacrise/materia1.html)
- [Rodada de Negócios da Moda em Caruaru](https://algomais.com/rodada-caruaru/)
- [Indústria Têxtil Brasileira - Apex Brasil](https://apexbrasil.com.br/content/apexbrasil/br/pt/conteudo/noticias/industria-textil-brasileira-leva-portfolio-diversificado-de-41-empresas-a-colombiatex-2026.html)
- Repositório UFPE sobre ferramentas de gestão no APL

---

**Próximas Etapas**:
- **Parte 2**: Modelar capacidades estratégicas (VDML) - habilidades de design, produção rápida, controle de qualidade
- **Parte 3**: Modelar dinâmica sistêmica (RVCS) - análise de resiliência, pontos de alavancagem, oportunidades de economia circular
