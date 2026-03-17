#!/bin/bash
# Script de setup automático do V-ANTPC
# Value Chain Analysis with Networked Triple-Pattern Cognition
# Inicializa Apache Jena Fuseki e carrega ontologias de cadeia de valor

set -e

echo "============================================================"
echo "V-ANTPC - Value Chain Knowledge Graph Setup"
echo "============================================================"

# 1. Verificar Docker
echo -e "\n1. Verificando Docker..."
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não encontrado. Instale Docker primeiro."
    exit 1
fi
echo "✓ Docker encontrado"

# 2. Parar containers antigos
echo -e "\n2. Limpando containers antigos..."
docker rm -f fuseki 2>/dev/null || true
echo "✓ Cleanup completo"

# 3. Iniciar Fuseki
echo -e "\n3. Iniciando Apache Jena Fuseki..."
docker run -d --name fuseki -p 3030:3030 -e ADMIN_PASSWORD=admin stain/jena-fuseki
echo "✓ Fuseki iniciado (porta 3030)"

# 4. Aguardar Fuseki ficar pronto
echo -e "\n4. Aguardando Fuseki inicializar..."
for i in {1..30}; do
    if curl -s http://localhost:3030/$/ping > /dev/null 2>&1; then
        echo "✓ Fuseki pronto!"
        break
    fi
    echo -n "."
    sleep 1
done

# 5. Criar dataset
echo -e "\n5. Criando dataset 'kg'..."
curl -X POST -u admin:admin http://localhost:3030/$/datasets \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "dbName=kg&dbType=tdb2" \
  2>/dev/null || echo "Dataset já existe ou erro ao criar"

# 6. Carregar ontologias usando Python
echo -e "\n6. Carregando ontologias de Value Chain..."

if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
else
    echo "⚠️  Python não encontrado. Pule esta etapa ou instale Python."
    PYTHON_CMD=""
fi

if [ -n "$PYTHON_CMD" ]; then
    cat > /tmp/load_ontologies.py << 'PYEOF'
import sys
sys.path.insert(0, 'knowledge_graph')

try:
    from value_chain_federator import ValueChainFederator

    print("   Inicializando Value Chain Federator...")
    fed = ValueChainFederator()

    if fed.verificar_conexao():
        print("\n   Carregando ontologias...")
        results = fed.carregar_todas_ontologias()

        success = sum(1 for v in results.values() if v)
        print(f"\n   ✓ {success}/4 ontologias carregadas com sucesso")
    else:
        print("   ✗ Não foi possível conectar ao Fuseki")
        sys.exit(1)

except Exception as e:
    print(f"   ✗ Erro ao carregar ontologias: {e}")
    print("\n   Execute manualmente:")
    print("   cd v-antpc && python knowledge_graph/value_chain_federator.py")
PYEOF

    $PYTHON_CMD /tmp/load_ontologies.py
    rm /tmp/load_ontologies.py
else
    echo "   ⚠️  Carregue ontologias manualmente:"
    echo "      cd v-antpc && python knowledge_graph/value_chain_federator.py"
fi

# 7. Verificar status
echo -e "\n7. Verificando status final..."
if curl -s http://localhost:3030/$/ping > /dev/null 2>&1; then
    echo "✅ SUCESSO! Fuseki rodando em http://localhost:3030"
    echo ""
    echo "Interface web: http://localhost:3030"
    echo "SPARQL endpoint: http://localhost:3030/kg/sparql"
    echo "Dataset: kg"
    echo "Usuário: admin"
    echo "Senha: admin"
else
    echo "❌ Erro: Fuseki não está respondendo"
    echo "Verifique os logs: docker logs fuseki"
    exit 1
fi

echo ""
echo "============================================================"
echo "Setup concluído! Próximos passos:"
echo "============================================================"
echo "1. Carregar dados do APL Têxtil de PE:"
echo "   python knowledge_graph/load_apl_data.py"
echo ""
echo "2. Execute queries SPARQL de análise:"
echo "   cat knowledge_graph/sparql_queries/analise_economica.sparql"
echo ""
echo "3. Ou use via Python:"
echo "   python -c 'from knowledge_graph.value_chain_federator import ValueChainFederator; f=ValueChainFederator(); print(f.listar_atores())'"
echo ""
echo "4. Explore a interface web:"
echo "   http://localhost:3030 (usuário: admin, senha: admin)"
echo ""
echo "Para parar o Fuseki:"
echo "   docker stop fuseki"
echo ""
echo "Para ver logs:"
echo "   docker logs -f fuseki"
echo "============================================================"
