#!/bin/bash

echo "=== Instalação do Dashboard Auditoria FB ==="
echo ""

# Verificar Python
echo "Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Por favor, instale Python 3.8 ou superior."
    exit 1
fi

echo "✅ Python encontrado: $(python3 --version)"
echo ""

# Criar ambiente virtual
echo "Criando ambiente virtual..."
if [ -d "venv" ]; then
    echo "Ambiente virtual já existe. Removendo..."
    rm -rf venv
fi

python3 -m venv venv || {
    echo "❌ Erro ao criar ambiente virtual."
    echo "No Ubuntu/Debian, instale: sudo apt install python3-venv"
    exit 1
}

echo "✅ Ambiente virtual criado"
echo ""

# Ativar ambiente virtual
echo "Ativando ambiente virtual..."
source venv/bin/activate || {
    echo "❌ Erro ao ativar ambiente virtual"
    exit 1
}

echo "✅ Ambiente virtual ativado"
echo ""

# Atualizar pip
echo "Atualizando pip..."
pip install --upgrade pip

# Instalar dependências
echo "Instalando dependências..."
pip install -r requirements.txt || {
    echo "❌ Erro ao instalar dependências"
    exit 1
}

echo ""
echo "✅ Instalação concluída com sucesso!"
echo ""
echo "Para executar a aplicação:"
echo "1. Ative o ambiente virtual: source venv/bin/activate"
echo "2. Execute: python app.py"
echo ""
echo "A aplicação estará disponível em http://localhost:5000"