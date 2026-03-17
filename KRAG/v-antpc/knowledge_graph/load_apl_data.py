#!/usr/bin/env python
"""
Load APL Data - Carrega dados do APL Têxtil de PE no Knowledge Graph

Converte dados estruturados dos arquivos Markdown em triplas RDF
e insere no Fuseki usando as ontologias e3value, REA, VDML, SCOR.

Autor: César Cunha
Data: 2026-03-17
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from knowledge_graph.value_chain_federator import ValueChainFederator


def criar_triplas_atores() -> str:
    """
    Cria triplas RDF para os atores da rede de valor do APL Têxtil PE.

    Baseado em: data/apl_textil_pe_parte1_economico.md
    """
    return """
# Fabricantes (Manufacturers)

actor:RotaDoMar a e3:Actor, rea:Manufacturer ;
    rdfs:label "Rota do Mar - Confecções" ;
    rdfs:comment "Empresa de referência no setor de confecções do Agreste, fundada em 1996" ;
    e3:location "Santa Cruz do Capibaribe, PE" ;
    rea:annual_production 1000000 ;
    e3:specialization "Moda casual, jeans, moda praia" .

actor:PoloToritamaJeans a e3:MarketSegment, rea:Manufacturer ;
    rdfs:label "Polo Toritama Jeans" ;
    rdfs:comment "Agregação de 3.000+ empresas especializadas em jeans" ;
    e3:location "Toritama, PE" ;
    rea:annual_production 60000000 ;
    e3:specialization "Jeans, denim, lavanderia industrial" ;
    e3:number_of_companies 3000 .

actor:ConfecoesCaruaru a e3:Actor, rea:Manufacturer ;
    rdfs:label "Confecções Caruaru Ltda" ;
    rdfs:comment "Fabricante de moda infantil e lingerie" ;
    e3:location "Caruaru, PE" ;
    rea:annual_production 500000 ;
    e3:specialization "Moda infantil, lingerie, moda íntima" .

# Fornecedores (Suppliers)

actor:TecelagemSP a e3:Actor, rea:Supplier, scor:Supplier ;
    rdfs:label "Tecelagem São Paulo SA" ;
    rdfs:comment "Fornecedor de tecidos planos de algodão e poliéster" ;
    e3:location "São Paulo, SP" ;
    scor:on_time_delivery_rate 92.5 ;
    e3:products "Tecidos planos, popeline, brim, sarja" .

actor:LinhasElasticosSC a e3:Actor, rea:Supplier, scor:Supplier ;
    rdfs:label "Linhas & Elásticos Catarinense" ;
    rdfs:comment "Fornecedor de linhas de costura e elásticos" ;
    e3:location "Santa Catarina, SC" ;
    scor:on_time_delivery_rate 88.0 ;
    e3:products "Linhas de poliéster, elásticos de cós" .

actor:EmbalagemNordeste a e3:Actor, rea:Supplier ;
    rdfs:label "Embalagens Nordeste" ;
    rdfs:comment "Fornecedor regional de embalagens plásticas e etiquetas" ;
    e3:location "Recife, PE" ;
    scor:on_time_delivery_rate 95.0 ;
    e3:products "Sacos plásticos, etiquetas, tags" .

# Distribuidores

actor:FeiraSulancaCaruaru a e3:Actor, scor:Distributor ;
    rdfs:label "Feira da Sulanca Caruaru" ;
    rdfs:comment "Centro de compras atacadista que comercializa 800 milhões de peças/ano" ;
    e3:location "Caruaru, PE" ;
    rea:annual_volume 800000000 ;
    e3:business_model "Atacado para lojistas de todo Brasil" .

actor:DistribuidoraNacional a e3:Actor, scor:Distributor ;
    rdfs:label "Distribuidora Nacional de Moda" ;
    rdfs:comment "Distribuidor atacadista com alcance nacional" ;
    scor:markets_served "Norte, Nordeste, Centro-Oeste" ;
    rea:monthly_volume 100000 .

# Clientes

actor:LojistasRegionais a e3:MarketSegment, scor:Customer ;
    rdfs:label "Lojistas Regionais" ;
    rdfs:comment "Pequenos e médios lojistas que compram na Feira da Sulanca" ;
    e3:location "Brasil (diversos estados)" ;
    e3:purchase_frequency "Semanal ou quinzenal" .

actor:GrandesRedes a e3:Actor, scor:Customer ;
    rdfs:label "Grandes Redes de Varejo" ;
    rdfs:comment "Redes nacionais de moda que compram grandes volumes" ;
    rea:monthly_volume 50000 ;
    e3:payment_terms "30-60 dias" .
"""


def criar_triplas_trocas_valor() -> str:
    """
    Cria triplas RDF para trocas de valor entre atores.

    Modelagem e3value: ValueExchange conecta ValuePorts de diferentes atores.
    """
    return """
# Trocas de Valor (Value Exchanges)

# Troca 1: Tecelagem SP → Rota do Mar (tecidos por dinheiro)
exchange:tecidos_rotamar a e3:ValueExchange ;
    rdfs:label "Compra de tecidos pela Rota do Mar" ;
    e3:connects port:tecelagem_out_tecidos, port:rotamar_in_tecidos .

port:tecelagem_out_tecidos a e3:ValuePort ;
    e3:direction "out" ;
    e3:belongs_to actor:TecelagemSP ;
    e3:offers object:tecidos_planos .

port:rotamar_in_tecidos a e3:ValuePort ;
    e3:direction "in" ;
    e3:belongs_to actor:RotaDoMar ;
    e3:requests object:tecidos_planos .

object:tecidos_planos a e3:ValueObject ;
    rdfs:label "Tecidos Planos (popeline, brim)" ;
    e3:economic_value 15000.00 ;
    e3:unit "R$ por tonelada" .

# Troca 2: Rota do Mar → Feira Sulanca (roupas por dinheiro)
exchange:roupas_feira a e3:ValueExchange ;
    rdfs:label "Venda de confecções para a Feira da Sulanca" ;
    e3:connects port:rotamar_out_roupas, port:feira_in_roupas .

port:rotamar_out_roupas a e3:ValuePort ;
    e3:direction "out" ;
    e3:belongs_to actor:RotaDoMar ;
    e3:offers object:roupas_casual .

port:feira_in_roupas a e3:ValuePort ;
    e3:direction "in" ;
    e3:belongs_to actor:FeiraSulancaCaruaru ;
    e3:requests object:roupas_casual .

object:roupas_casual a e3:ValueObject ;
    rdfs:label "Roupas Casuais e Jeans" ;
    e3:economic_value 45.00 ;
    e3:unit "R$ por peça (preço médio atacado)" .

# Troca 3: Feira Sulanca → Lojistas Regionais
exchange:feira_lojistas a e3:ValueExchange ;
    rdfs:label "Venda atacadista para lojistas regionais" ;
    e3:connects port:feira_out_atacado, port:lojistas_in_atacado .

port:feira_out_atacado a e3:ValuePort ;
    e3:direction "out" ;
    e3:belongs_to actor:FeiraSulancaCaruaru ;
    e3:offers object:roupas_atacado .

port:lojistas_in_atacado a e3:ValuePort ;
    e3:direction "in" ;
    e3:belongs_to actor:LojistasRegionais ;
    e3:requests object:roupas_atacado .

object:roupas_atacado a e3:ValueObject ;
    rdfs:label "Roupas para Revenda" ;
    e3:economic_value 50.00 ;
    e3:unit "R$ por peça" .
"""


def criar_triplas_capacidades() -> str:
    """
    Cria triplas RDF para capacidades organizacionais (VDML).

    Baseado em: data/apl_textil_pe_parte2_capacidades.md
    """
    return """
# Capacidades Organizacionais (VDML)

# Capacidades Core (Diferenciadoras)

capability:design_moda a vdml:Capability ;
    rdfs:label "Design de Moda Regional" ;
    rdfs:comment "Capacidade de criar coleções alinhadas ao mercado nordestino" ;
    vdml:capability_level "Alto" ;
    vdml:is_core true ;
    vdml:belongs_to actor:RotaDoMar .

capability:producao_rapida a vdml:Capability ;
    rdfs:label "Produção Rápida (Fast Fashion)" ;
    rdfs:comment "Capacidade de responder rapidamente às tendências de mercado" ;
    vdml:capability_level "Alto" ;
    vdml:is_core true ;
    vdml:belongs_to actor:PoloToritamaJeans .

# Capacidades de Suporte

capability:gestao_estoque a vdml:Capability ;
    rdfs:label "Gestão de Estoque" ;
    rdfs:comment "Controle de inventário de matéria-prima e produtos acabados" ;
    vdml:capability_level "Médio" ;
    vdml:is_core false ;
    vdml:belongs_to actor:ConfecoesCaruaru .

capability:logistica_distribuicao a vdml:Capability ;
    rdfs:label "Logística e Distribuição Nacional" ;
    rdfs:comment "Capacidade de distribuir para todo o Brasil" ;
    vdml:capability_level "Alto" ;
    vdml:is_core true ;
    vdml:belongs_to actor:DistribuidoraNacional .

capability:relacionamento_fornecedores a vdml:Capability ;
    rdfs:label "Relacionamento com Fornecedores" ;
    rdfs:comment "Parcerias estratégicas com fornecedores do Sul/Sudeste" ;
    vdml:capability_level "Médio" ;
    vdml:is_core false ;
    vdml:belongs_to actor:RotaDoMar .
"""


def criar_triplas_metricas_scor() -> str:
    """
    Cria triplas RDF para métricas SCOR de supply chain.

    Baseado em: data/apl_textil_pe_parte3_sistemica.md
    """
    return """
# Métricas SCOR (Supply Chain Operations Reference)

# Perfect Order Fulfillment (Pedido Perfeito)
metric:perfect_order a scor:PerfectOrderFulfillment, scor:Metric ;
    rdfs:label "Taxa de Pedido Perfeito" ;
    rdfs:comment "Pedidos entregues completos, no prazo e sem danos" ;
    scor:actual_value 87.5 ;
    scor:target_value 95.0 ;
    scor:metric_unit "%" ;
    scor:performance_attribute scor:Reliability .

# Order Fulfillment Cycle Time
metric:cycle_time a scor:OrderFulfillmentCycleTime, scor:Metric ;
    rdfs:label "Tempo de Ciclo de Atendimento" ;
    rdfs:comment "Tempo médio entre pedido e entrega" ;
    scor:actual_value 12.5 ;
    scor:target_value 8.0 ;
    scor:metric_unit "dias" ;
    scor:performance_attribute scor:Responsiveness .

# Supply Chain Cost
metric:supply_chain_cost a scor:SupplyChainCost, scor:Metric ;
    rdfs:label "Custo Total da Cadeia" ;
    rdfs:comment "Custo end-to-end como % da receita" ;
    scor:actual_value 18.3 ;
    scor:target_value 15.0 ;
    scor:metric_unit "% da receita" ;
    scor:performance_attribute scor:Cost .

# Upward Supply Chain Flexibility
metric:upward_flexibility a scor:UpwardSupplyChainFlexibility, scor:Metric ;
    rdfs:label "Flexibilidade Upward" ;
    rdfs:comment "Capacidade de aumentar produção em 30 dias" ;
    scor:actual_value 25.0 ;
    scor:target_value 35.0 ;
    scor:metric_unit "% de aumento" ;
    scor:performance_attribute scor:Agility .

# Cash-to-Cash Cycle Time
metric:cash_to_cash a scor:Metric ;
    rdfs:label "Ciclo Cash-to-Cash" ;
    rdfs:comment "Tempo entre pagamento a fornecedores e recebimento de clientes" ;
    scor:actual_value 45.0 ;
    scor:target_value 30.0 ;
    scor:metric_unit "dias" ;
    scor:performance_attribute scor:AssetManagement .
"""


def main():
    """
    Função principal para carregar dados do APL Têxtil PE.
    """
    print("=" * 70)
    print("LOAD APL DATA - Carregamento de Dados do APL Têxtil de Pernambuco")
    print("=" * 70)
    print()

    # Inicializar federador
    print("1. Conectando ao Fuseki...")
    fed = ValueChainFederator()

    if not fed.verificar_conexao():
        print("\n❌ ERRO: Não foi possível conectar ao Fuseki")
        print("   Certifique-se de que o Fuseki está rodando:")
        print("   docker ps | grep fuseki")
        print("   OU execute: bash setup.sh")
        return 1

    print("\n2. Preparando triplas RDF...")

    # NOTA: Não incluir @prefix aqui, o método inserir_triplas já adiciona os prefixes SPARQL
    # Combinar todas as triplas (sem prefixes)
    all_triples = "# ========== ATORES ==========\n"
    all_triples += criar_triplas_atores()
    all_triples += "\n# ========== TROCAS DE VALOR ==========\n"
    all_triples += criar_triplas_trocas_valor()
    all_triples += "\n# ========== CAPACIDADES ==========\n"
    all_triples += criar_triplas_capacidades()
    all_triples += "\n# ========== MÉTRICAS SCOR ==========\n"
    all_triples += criar_triplas_metricas_scor()

    print(f"   ✓ {len(all_triples.split(chr(10)))} linhas de triplas preparadas")

    # Inserir no Fuseki
    print("\n3. Inserindo dados no Knowledge Graph...")
    success = fed.inserir_triplas(
        all_triples,
        graph_uri="http://valuechain.org/data/apl-textil-pe"
    )

    if success:
        print("   ✓ Dados inseridos com sucesso!")
    else:
        print("   ✗ Erro ao inserir dados")
        return 1

    # Verificar estatísticas
    print("\n4. Verificando estatísticas...")
    stats = fed.estatisticas_grafo()

    print("\n" + "=" * 70)
    print("ESTATÍSTICAS DO KNOWLEDGE GRAPH")
    print("=" * 70)
    print(f"Total de triplas: {stats.get('total_triplas', 0):,}")
    print(f"Total de classes: {stats.get('total_classes', 0)}")
    print(f"Total de atores: {stats.get('total_atores', 0)}")
    print(f"Total de capacidades: {stats.get('total_capacidades', 0)}")

    # Listar atores
    print("\n5. Listando atores carregados...")
    atores = fed.listar_atores()

    if atores:
        print(f"\n   Encontrados {len(atores)} atores:")
        for ator in atores[:10]:  # Limitar a 10 para não poluir
            label = ator['uri'].split('/')[-1]
            tipo = ator['tipo'].split('#')[-1] if '#' in ator['tipo'] else ator['tipo']
            print(f"   - {label} ({tipo})")

        if len(atores) > 10:
            print(f"   ... e mais {len(atores) - 10} atores")
    else:
        print("   ⚠️  Nenhum ator encontrado")

    print("\n" + "=" * 70)
    print("✅ CARREGAMENTO CONCLUÍDO COM SUCESSO!")
    print("=" * 70)
    print("\nPróximos passos:")
    print("- Execute queries SPARQL de análise:")
    print("  cat knowledge_graph/sparql_queries/analise_economica.sparql")
    print("\n- Ou use via Python:")
    print("  python -c 'from knowledge_graph.value_chain_federator import ValueChainFederator; f=ValueChainFederator(); print(f.listar_atores())'")
    print("\n- Explore no Jupyter Notebook:")
    print("  jupyter notebook notebooks/Tutorial_ValueChain_Analysis.ipynb")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
