#!/usr/bin/env python
"""
Arquivo principal para executar a aplicação.
Mantém compatibilidade com a estrutura organizada.
"""

import sys
import os

# Adiciona o diretório src ao PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Importa e executa a aplicação
from app import app, init_db, Config

if __name__ == '__main__':
    # Criar diretório de uploads se não existir
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    
    # Inicializar banco
    init_db()
    
    # Rodar aplicação
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=5000)