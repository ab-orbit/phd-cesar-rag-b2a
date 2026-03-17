# APL Têxtil de Pernambuco - Parte 2: Capacidades Estratégicas
## Dataset Incremental para Knowledge Graph Federado

> **Ontologias Aplicadas**: VDML (Value Delivery Modeling Language)
> **Objetivo**: Modelar capacidades organizacionais, propostas de valor, métodos de entrega e métricas de desempenho

---

## 1. PROPOSTAS DE VALOR (Value Propositions)

### 1.1 Proposta Principal: "Moda Popular de Alta Velocidade"

**Proposta**: `valueProposition:ModaPopularVelocidade`
- **Tipo**: vdml:ValueProposition
- **Provedor**: `actor:PoloToritamaJeans` (agregado de 3.000+ empresas)
- **Destinatário**: `actor:LojistasRegionais`, `actor:DistribuidoraNacional`
- **Descrição**: "Produção em massa de roupas casuais e jeans de qualidade aceitável a preços altamente competitivos, com reposição rápida de estoque (ciclo de 15 dias)"

**Componentes de Valor**:

1. **Custo Competitivo** (`component:CustoCompetitivo`)
   - **Tipo**: vdml:CostDimension
   - **Descrição**: Preço 30-40% menor que marcas nacionais tradicionais
   - **Valoração**: Jeans vendido a R$ 55,00 (atacado) vs. R$ 90,00 de concorrentes
   - **Fonte de Vantagem**: Economia de escala, mão de obra local, informalidade parcial

2. **Velocidade de Reposição** (`component:VelocidadeReposicao`)
   - **Tipo**: vdml:TimeDimension
   - **Descrição**: Ciclo de produção e entrega de 15 dias (vs. 45-60 dias de importados)
   - **Valoração**: Lojistas podem repor estoque 3x mais rápido
   - **Fonte de Vantagem**: Proximidade geográfica, flexibilidade de pequenas unidades

3. **Volume Garantido** (`component:VolumeGarantido`)
   - **Tipo**: vdml:ValuePropositionComponent
   - **Descrição**: Capacidade de atender grandes volumes sem lead time longo
   - **Valoração**: 800 milhões de peças/ano de capacidade instalada
   - **Fonte de Vantagem**: 18.000 empresas atuando em paralelo

4. **Diversidade de Produtos** (`component:DiversidadeProdutos`)
   - **Tipo**: vdml:ValuePropositionComponent
   - **Descrição**: Mix amplo: jeans, casual, infantil, lingerie, moda praia
   - **Valoração**: Lojista pode comprar todo mix em único fornecedor
   - **Fonte de Vantagem**: Clusters especializados (Toritama=jeans, Caruaru=infantil)

### 1.2 Proposta Secundária: "Qualidade Controlada"

**Proposta**: `valueProposition:QualidadeControlada`
- **Tipo**: vdml:ValueProposition
- **Provedor**: `actor:RotaDoMar` (empresa de referência)
- **Destinatário**: Distribuidores exigentes
- **Descrição**: "Produtos com certificação de qualidade e baixa taxa de defeitos (<2%), garantindo marca forte no varejo"

**Componentes**:

1. **Confiabilidade** (`component:Confiabilidade`)
   - **Tipo**: vdml:QualityDimension
   - **Taxa de Defeitos**: <2% (vs. 5-8% da média do APL informal)
   - **Garantia**: 30 dias para devolução

---

## 2. CAPACIDADES ORGANIZACIONAIS (Capabilities)

### 2.1 Capacidade CORE: "Produção em Massa Flexível"

**Capacidade**: `capability:ProducaoMassaFlexivel`
- **Tipo**: vdml:CoreCapability
- **É Central**: TRUE (diferencial competitivo)
- **Nível de Maturidade**: 4/5 (otimizada)
- **Descrição**: Habilidade de produzir grandes volumes mantendo flexibilidade para mudanças rápidas de modelo/cor

**Entrega de Valor**:
- **Delivers**: `valueProposition:ModaPopularVelocidade` (componente VelocidadeReposicao)

**Capacidades de Suporte**:
- **Supports**: `capability:GestaoMateriaPrima`, `capability:LogisticaRapida`

**Métodos de Realização**:

#### Método 1: `capabilityMethod:ProducaoLotesPequenos`
- **Tipo**: vdml:CapabilityMethod
- **Descrição**: Produção em lotes de 500-2.000 peças (vs. 50.000+ de grandes indústrias)
- **Vantagem**: Permite trocar modelo rapidamente sem desperdício
- **Custo**: R$ 15.000/lote (setup + produção)
- **Duração**: 3-5 dias/lote

**Práticas Utilizadas**:
- **Practice**: `practice:SetupRapido` (troca de modelo em <2 horas)
- **Practice**: `practice:CelulasProducao` (equipes de 5-8 costureiras por célula)
- **Practice**: `practice:EstoqueZeroWIP` (produção just-in-time entre etapas)

**Atividades Executadas**:
1. `activity:Corte` (Cortar tecido conforme molde)
2. `activity:Costura` (Costurar partes)
3. `activity:Acabamento` (Aplicar botões, etiquetas)
4. `activity:Lavagem` (apenas jeans - stonewash, destroyed)
5. `activity:Embalagem` (Embalar e etiquetar)

### 2.2 Capacidade CORE: "Design Rápido de Moda"

**Capacidade**: `capability:DesignRapidoModa`
- **Tipo**: vdml:CoreCapability
- **É Central**: TRUE
- **Nível de Maturidade**: 3/5 (definida)
- **Descrição**: Capacidade de copiar tendências globais e lançar coleções em 30 dias

**Entrega de Valor**:
- **Delivers**: `valueProposition:ModaPopularVelocidade` (componente DiversidadeProdutos)

**Métodos de Realização**:

#### Método 1: `capabilityMethod:FastFashionCopy`
- **Tipo**: vdml:CapabilityMethod
- **Descrição**: Replicação acelerada de tendências de desfiles internacionais
- **Duração**: 15-30 dias (inspiração → produção)
- **Custo**: R$ 5.000/coleção (viagem a feiras + desenvolvimento)

**Práticas**:
- **Practice**: `practice:BenchmarkingFeiras` (visitas a feiras de moda em SP)
- **Practice**: `practice:ProtopitagemRapida` (protótipo em 3 dias)
- **Practice**: `practice:TestesMercado` (testar 200 peças antes de escalar)

**Atividades**:
1. `activity:PesquisaTendencias` (Identificar tendências em feiras/redes sociais)
2. `activity:CriacaoMolde` (Desenvolver modelagem)
3. `activity:PrototipoTeste` (Produzir amostras)
4. `activity:AjusteFinal` (Corrigir caimento/acabamento)

### 2.3 Capacidade SUPPORT: "Gestão de Matéria-Prima"

**Capacidade**: `capability:GestaoMateriaPrima`
- **Tipo**: vdml:SupportCapability
- **É Central**: FALSE (habilitadora, não diferenciadora)
- **Nível de Maturidade**: 3/5
- **Descrição**: Gerenciar compra, estocagem e distribuição de tecidos/aviamentos

**Métodos de Realização**:

#### Método 1: `capabilityMethod:CompraConsolidada`
- **Tipo**: vdml:CapabilityMethod
- **Descrição**: NTCPE negocia compra conjunta para 50+ empresas
- **Vantagem**: Desconto de 12-15% por volume
- **Custo de Coordenação**: R$ 2.000/mês (taxa NTCPE)

**Práticas**:
- **Practice**: `practice:ForecastColetivo` (empresas compartilham previsão de demanda)
- **Practice**: `practice:ContratoFramework` (acordo anual com fornecedores SP/SC)

**Atividades**:
1. `activity:ConsolidarDemanda` (Agregar pedidos de 50 empresas)
2. `activity:NegociarFornecedores` (Licitação com tecelagens)
3. `activity:ReceberLotes` (Recebimento centralizado em Caruaru)
4. `activity:DistribuirEmpresas` (Entrega local a cada fabricante)

### 2.4 Capacidade SUPPORT: "Lavanderia Industrial (Jeans)"

**Capacidade**: `capability:LavanderiaIndustrialJeans`
- **Tipo**: vdml:SupportCapability
- **É Central**: FALSE (mas crítica para jeans)
- **Nível de Maturidade**: 5/5 (Toritama tem 50+ lavanderias - referência nacional)
- **Descrição**: Aplicar processos químicos e mecânicos para efeitos visuais em jeans (stonewash, destroyed, tie-dye)

**Métodos de Realização**:

#### Método 1: `capabilityMethod:StonewashAutomatizado`
- **Duração**: 4 horas/lote (1.000 peças)
- **Custo**: R$ 3,50/peça
- **Recursos**: Máquinas lavadoras industriais de 300kg, pedras vulcânicas, produtos químicos

**Atividades**:
1. `activity:PreLavagem` (Remover goma do tecido)
2. `activity:EstonamentoQuimico` (Aplicar permanganato/enzimas)
3. `activity:EnxagueCentrifugacao` (Remover químicos)
4. `activity:SecagemTumbler` (Secar e amaciamento)

### 2.5 Capacidade SUPPORT: "Logística Rápida Regional"

**Capacidade**: `capability:LogisticaRapida`
- **Tipo**: vdml:SupportCapability
- **É Central**: FALSE
- **Nível de Maturidade**: 3/5
- **Descrição**: Entregar pedidos em 3-5 dias para Nordeste, 7-10 dias para resto do Brasil

**Métodos**:

#### Método 1: `capabilityMethod:RotasConsolidadas`
- **Descrição**: Caminhões saem diariamente de Caruaru para capitais brasileiras
- **Custo de Frete**: R$ 0,50-1,00/peça (dependendo distância)
- **Frequência**: Diária (Nordeste), 3x/semana (Sul/Sudeste)

**Atividades**:
1. `activity:ConsolidarPedidos` (Agrupar pedidos de múltiplas empresas)
2. `activity:RoteirizarEntregas` (Planejar rota otimizada)
3. `activity:CarregarCaminhao` (Loading e conferência)
4. `activity:Transportar` (Viagem)
5. `activity:DescarregarClientes` (Entrega porta-a-porta)

---

## 3. ATIVIDADES DETALHADAS (Activities)

### 3.1 Atividade: Corte de Tecido

**Atividade**: `activity:Corte`
- **Tipo**: vdml:Activity
- **Pertence ao Método**: `capabilityMethod:ProducaoLotesPequenos`
- **Descrição**: Cortar peças de tecido conforme moldes de papel usando máquina de corte industrial

**Decomposição**:
- **Sub-atividade 1**: `activity:EncaixeMoldes` (Arranjar moldes para minimizar desperdício)
- **Sub-atividade 2**: `activity:CorteAutomatizado` (Cortar múltiplas camadas simultaneamente)
- **Sub-atividade 3**: `activity:SeparacaoLotes` (Organizar peças por tamanho/cor)

**Papel Responsável**: `role:Cortador`
- **Tipo**: vdml:Role
- **Competências**: Leitura de moldes, operação de máquina industrial, otimização de encaixe
- **Quantidade**: 2 cortadores/célula de produção

**Recursos Usados**:
- **Recurso 1**: `resource:MaquinaCorteIndustrial`
  - **Tipo**: vdml:Resource
  - **Quantidade**: 1 máquina/célula
  - **Custo**: R$ 25.000 (investimento inicial)
  - **Vida Útil**: 10 anos
- **Recurso 2**: `resource:MesaCorte`
  - **Quantidade**: 1 mesa (10m x 2m)
  - **Custo**: R$ 3.000

**Duração**: 2 horas (para lote de 500 peças)
**Custo**: R$ 500 (mão de obra + energia + manutenção)

### 3.2 Atividade: Costura

**Atividade**: `activity:Costura`
- **Tipo**: vdml:Activity
- **Descrição**: Unir peças cortadas usando máquinas de costura industrial (reta, overloque, galoneira)

**Decomposição**:
- **Sub 1**: `activity:CosturaPrincipal` (Unir laterais, virilha, cintura)
- **Sub 2**: `activity:CosturaAcabamento` (Barras, pespontos decorativos)
- **Sub 3**: `activity:Revisao` (Inspeção visual de costuras)

**Papéis**:
- **Role**: `role:Costureira`
  - **Quantidade**: 5-8 costureiras/célula
  - **Competências**: Operação de máquina reta/overloque, controle de qualidade
  - **Produtividade**: 40 peças/dia/costureira

**Recursos**:
- **Máquina Reta Industrial**: R$ 2.500/unidade (5 por célula)
- **Máquina Overloque**: R$ 3.500/unidade (2 por célula)
- **Galoneira**: R$ 4.000/unidade (1 por célula)

**Duração**: 8 horas (lote de 500 peças com 5 costureiras)
**Custo**: R$ 2.000 (mão de obra + consumo de linha/energia)

### 3.3 Atividade: Lavagem Stonewash (apenas Jeans)

**Atividade**: `activity:Lavagem`
- **Tipo**: vdml:Activity
- **Pertence a**: `capability:LavanderiaIndustrialJeans`

**Sub-atividades**:
- `activity:EstonamentoQuimico`: Aplicar enzimas celulase para desgaste do índigo
- `activity:EnxagueCentrifugacao`: Remover químicos residuais
- `activity:Secagem`: Tumbler industrial a 80°C

**Papel**: `role:OperadorLavanderia`
- **Competências**: Química têxtil, operação de lavadoras de 300kg, controle de pH

**Recursos**:
- `resource:LavadoraIndustrial300kg`: R$ 120.000/unidade
- `resource:TumblerSecador`: R$ 80.000/unidade
- `resource:EnzimasCelulase`: R$ 15/kg (consumo de 0,5kg/1000 peças)

**Duração**: 4 horas/lote (1.000 peças)
**Custo**: R$ 3.500/lote (química + energia + água + mão de obra)

### 3.4 Atividade: Pesquisa de Tendências

**Atividade**: `activity:PesquisaTendencias`
- **Tipo**: vdml:Activity
- **Pertence a**: `capability:DesignRapidoModa`

**Sub-atividades**:
- `activity:VisitaFeiraSP`: Visita trimestral à Texbrasil (São Paulo)
- `activity:MonitoramentoRedesSociais`: Análise de Instagram/TikTok de influencers
- `activity:AnaliseVendas`: Identificar modelos mais vendidos no APL

**Papel**: `role:Estilista`
- **Competências**: Moda, análise de tendências, fotografia, redes sociais
- **Quantidade**: 1 estilista para cada 10 empresas (terceirizado/compartilhado)

**Duração**: Contínuo (4 horas/dia)
**Custo**: R$ 8.000/mês (salário + viagens)

---

## 4. COLABORAÇÕES E REDE DE NEGÓCIOS

### 4.1 Rede de Negócios: APL Têxtil do Agreste

**Rede**: `businessNetwork:APL_TextilAgreste`
- **Tipo**: vdml:BusinessNetwork
- **Participantes**: 18.000+ empresas de confecção
- **Coordenação**: `actor:NTCPE`
- **Objetivo Coletivo**: Aumentar competitividade global do polo têxtil

**Colaborações Principais**:

#### Colaboração 1: Compra Consolidada de Matéria-Prima

**Colaboração**: `collaboration:CompraConsolidadaTecidos`
- **Tipo**: vdml:Collaboration
- **Participantes**:
  - **Role**: `role:EmpresaCompradora` (50+ empresas participantes)
  - **Role**: `role:CoordenadorCompras` (NTCPE)
  - **Role**: `role:FornecedorTecido` (Tecelagens SP/SC)
- **Parte da Rede**: `businessNetwork:APL_TextilAgreste`
- **Frequência**: Trimestral
- **Volume**: R$ 15 milhões/trimestre (tecidos para 50 empresas)
- **Benefício**: Desconto de 12-15% + melhoria em prazo de pagamento (30→45 dias)

**Processo**:
1. Empresas enviam previsão de demanda para NTCPE
2. NTCPE consolida e negocia com fornecedores
3. Fornecedores entregam lote consolidado em Caruaru
4. NTCPE distribui proporcionalmente às empresas

#### Colaboração 2: Logística Compartilhada

**Colaboração**: `collaboration:FreteCompartilhado`
- **Participantes**:
  - **Role**: `role:Embarcador` (10+ empresas que enviam para mesma região)
  - **Role**: `role:Transportadora` (empresa local)
- **Benefício**: Redução de 30% no custo de frete unitário

---

## 5. MÉTRICAS DE DESEMPENHO (Performance Objectives)

### 5.1 Objetivo: Lead Time de Produção

**Métrica**: `metric:LeadTimeProducao`
- **Tipo**: vdml:Measurement
- **Elemento Medido**: `capability:ProducaoMassaFlexivel`
- **Atributo**: scor:Responsiveness (Responsividade)
- **Unidade**: Dias
- **Valor Atual**: 15 dias (ordem → produto acabado)
- **Valor Alvo**: 12 dias
- **Gap**: -3 dias
- **Objetivo**: `performanceObjective:ReduzirLeadTime`

**Ações para Atingir Meta**:
- Implementar RFID em estoques intermediários (WIP tracking)
- Reduzir setup de máquinas de 2h para 1h
- Automatizar corte com máquina CNC

### 5.2 Objetivo: Taxa de Defeitos

**Métrica**: `metric:TaxaDefeitos`
- **Elemento Medido**: `activity:Costura`
- **Atributo**: scor:Reliability (Confiabilidade)
- **Unidade**: Percentual (%)
- **Valor Atual**: 5,2% (média do APL)
- **Valor Alvo**: 2,0% (benchmark Rota do Mar)
- **Gap**: -3,2 pontos percentuais
- **Objetivo**: `performanceObjective:MelhorarQualidade`

**Ações**:
- Treinamento de costureiras (40h/ano)
- Implementar inspeção em 3 pontos (corte, costura, acabamento)
- Bonus por qualidade (redução de retrabalho)

### 5.3 Objetivo: Custo de Produção por Peça

**Métrica**: `metric:CustoProducaoPeca`
- **Elemento Medido**: `capabilityMethod:ProducaoLotesPequenos`
- **Atributo**: scor:Cost
- **Unidade**: R$/peça
- **Valor Atual**: R$ 35,00/peça (jeans)
- **Valor Alvo**: R$ 32,00/peça
- **Gap**: -R$ 3,00
- **Objetivo**: `performanceObjective:OtimizarCustos`

**Ações**:
- Renegociar tecido via compra consolidada NTCPE
- Automatizar corte (reduzir desperdício de 8% para 5%)
- Aumentar escala de lotes (500→1.000 peças) para diluir setup

### 5.4 Objetivo: Tempo de Ciclo de Design

**Métrica**: `metric:TempoDesign`
- **Elemento Medido**: `capability:DesignRapidoModa`
- **Atributo**: scor:Responsiveness
- **Unidade**: Dias
- **Valor Atual**: 30 dias (tendência → coleção lançada)
- **Valor Alvo**: 20 dias
- **Objetivo**: `performanceObjective:AcelerarInovacao`

**Ações**:
- Contratar estilista full-time (vs. terceirizado)
- Implementar CAD/CAM para modelagem digital
- Criar banco de moldes reutilizáveis

### 5.5 Objetivo: Utilização de Capacidade Produtiva

**Métrica**: `metric:UtilizacaoCapacidade`
- **Elemento Medido**: `resource:MaquinaCosturaIndustrial` (agregado do APL)
- **Atributo**: scor:AssetManagement
- **Unidade**: Percentual (%)
- **Valor Atual**: 68% (sazonalidade alta: 85%, baixa: 50%)
- **Valor Alvo**: 80% (média anual)
- **Objetivo**: `performanceObjective:NivelarProducao`

**Ações**:
- Diversificar mix de produtos (adicionar moda praia no inverno)
- Buscar contratos de longo prazo com distribuidores
- Produzir para estoque estratégico em baixa temporada

### 5.6 Objetivo: Taxa de Entrega no Prazo (On-Time Delivery)

**Métrica**: `metric:EntregaNoPrazo`
- **Elemento Medido**: `capability:LogisticaRapida`
- **Atributo**: scor:Reliability
- **Unidade**: Percentual (%)
- **Valor Atual**: 78%
- **Valor Alvo**: 95%
- **Objetivo**: `performanceObjective:MelhorarConfiabilidade`

**Ações**:
- Implementar TMS (Transportation Management System)
- Contratar transportadoras com SLA
- Buffer de segurança de 1 dia no planejamento

---

## 6. RECURSOS CRÍTICOS (Resources)

### 6.1 Maquinário

**Máquina de Costura Reta Industrial** (`resource:MaquinaCosturaReta`)
- **Tipo**: vdml:Resource
- **Usado por**: `activity:Costura`
- **Quantidade Total no APL**: ~50.000 máquinas (estimativa)
- **Custo Unitário**: R$ 2.500
- **Vida Útil**: 15 anos
- **Taxa de Depreciação**: R$ 167/ano

**Lavadora Industrial 300kg** (`resource:LavadoraIndustrial`)
- **Usado por**: `activity:Lavagem` (Toritama)
- **Quantidade**: 200+ máquinas (50 lavanderias x 4 máquinas/média)
- **Custo**: R$ 120.000
- **Capacidade**: 1.000 peças/ciclo (4 horas)

### 6.2 Mão de Obra

**Costureiras** (`resource:MaoObraCostureiras`)
- **Tipo**: vdml:Resource (Human Resource)
- **Quantidade**: 130.000 pessoas (formal + informal)
- **Custo Médio**: R$ 2.000/mês (salário + encargos para formais)
- **Produtividade**: 40 peças/dia/costureira
- **Armazenado em**: `store:MercadoTrabalhoAgreste`

**Estilistas/Designers** (`resource:Estilistas`)
- **Quantidade**: ~500 profissionais (1 para cada 36 empresas)
- **Custo**: R$ 5.000-8.000/mês
- **Produtividade**: 4-6 coleções/ano

### 6.3 Instalações

**Galpões Industriais** (`resource:GalpaoProducao`)
- **Quantidade**: 2.000+ galpões (empresas médias/grandes)
- **Área Média**: 500 m²
- **Custo de Aluguel**: R$ 5.000-10.000/mês
- **Localização**: Armazenados em `store:DistritoIndustrialCaruaru`, `store:PoloToritama`

---

## FONTES

Este dataset usa informações sobre estrutura organizacional, capacidades e práticas do APL Têxtil de Pernambuco.

---

**Próxima Etapa**:
- **Parte 3**: Modelar dinâmica sistêmica (RVCS) - análise de risco exponencial, oportunidades de Indústria 6.0, resiliência da rede
