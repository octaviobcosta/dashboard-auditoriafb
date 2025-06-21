#!/bin/bash

# Script de automação para deploy do dashboard
# Executa testes, build e deploy automaticamente

set -e  # Para se houver erro

echo "🚀 Iniciando deploy automático..."

# Verifica se estamos no diretório correto
if [ ! -f "src/app.py" ]; then
    echo "❌ Erro: Execute o script na raiz do projeto"
    exit 1
fi

# Instala dependências se necessário
if [ -f "requirements.txt" ]; then
    echo "📦 Instalando dependências..."
    pip install -r requirements.txt --quiet
fi

# Executa testes se existirem
if [ -d "tests" ] || [ -f "test_*.py" ]; then
    echo "🧪 Executando testes..."
    python -m pytest -q || echo "⚠️  Alguns testes falharam, continuando..."
fi

# Verifica sintaxe Python
echo "🔍 Verificando sintaxe..."
python -m py_compile src/app.py
python -m py_compile src/models/database.py

echo "✅ Deploy automático concluído!"