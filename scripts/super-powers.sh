#!/bin/bash

# 🚀 SUPERPODERES DE DESENVOLVIMENTO
# Script mestre que ativa todos os poderes especiais

echo "🚀 Ativando SUPERPODERES de desenvolvimento..."

# Função para logging colorido
log_info() { echo -e "\033[1;34m[INFO]\033[0m $1"; }
log_success() { echo -e "\033[1;32m[SUCCESS]\033[0m $1"; }
log_warning() { echo -e "\033[1;33m[WARNING]\033[0m $1"; }
log_error() { echo -e "\033[1;31m[ERROR]\033[0m $1"; }

# Cria estrutura de diretórios
create_project_structure() {
    log_info "Criando estrutura de superpoderes..."
    
    mkdir -p {logs,metrics,reports,backups,tmp}
    mkdir -p scripts/{automation,monitoring,deployment}
    mkdir -p src/{analytics,optimization,security}
    
    log_success "Estrutura criada!"
}

# Instala ferramentas de desenvolvimento avançadas
install_dev_tools() {
    log_info "Instalando ferramentas de superpoder..."
    
    # Python tools
    pip install --quiet --upgrade \
        black autopep8 flake8 mypy \
        pytest pytest-cov pytest-benchmark \
        memory-profiler line-profiler \
        bandit safety \
        requests beautifulsoup4 \
        watchdog schedule \
        rich typer click
    
    log_success "Ferramentas instaladas!"
}

# Configura git hooks automáticos
setup_git_hooks() {
    log_info "Configurando Git Hooks..."
    
    # Pre-commit hook
    cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
echo "🔍 Executando verificações pré-commit..."

# Formata código automaticamente
python -m black src/ --quiet
python -m autopep8 --in-place --recursive src/

# Verifica sintaxe
python -m flake8 src/ --max-line-length=100 --ignore=E203,W503

# Executa testes rápidos
python -m pytest tests/ -x --tb=short

echo "✅ Verificações concluídas!"
EOF

    chmod +x .git/hooks/pre-commit
    log_success "Git hooks configurados!"
}

# Cria sistema de monitoramento
setup_monitoring() {
    log_info "Configurando monitoramento automático..."
    
    # Cria script de monitoramento contínuo
    cat > scripts/monitoring/continuous-monitor.py << 'EOF'
import time
import psutil
import json
from datetime import datetime
from pathlib import Path

def monitor_system():
    while True:
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent,
            "python_processes": len([p for p in psutil.process_iter(['name']) if 'python' in p.info['name']])
        }
        
        # Salva métricas
        metrics_file = Path("metrics") / f"system_{datetime.now().strftime('%Y%m%d')}.json"
        with open(metrics_file, 'a') as f:
            f.write(json.dumps(metrics) + '\n')
        
        time.sleep(30)  # Monitora a cada 30 segundos

if __name__ == "__main__":
    monitor_system()
EOF

    log_success "Sistema de monitoramento configurado!"
}

# Configura CI/CD pipeline
setup_cicd() {
    log_info "Configurando pipeline CI/CD..."
    
    # Cria workflow GitHub Actions
    mkdir -p .github/workflows
    
    cat > .github/workflows/dashboard-ci.yml << 'EOF'
name: Dashboard CI/CD

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python -m pytest tests/ --cov=src/
    
    - name: Code quality check
      run: |
        python -m flake8 src/
        python -m black --check src/
    
    - name: Security scan
      run: |
        python -m bandit -r src/
        python -m safety check
    
    - name: Performance analysis
      run: |
        python dev-assistant.py report

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    - name: Deploy to production
      run: |
        echo "🚀 Deploying to production..."
        # Adicione seus comandos de deploy aqui
EOF

    log_success "Pipeline CI/CD configurado!"
}

# Cria dashboard de métricas em tempo real
create_metrics_dashboard() {
    log_info "Criando dashboard de métricas..."
    
    cat > src/analytics/metrics_dashboard.py << 'EOF'
from flask import Flask, render_template, jsonify
import json
import glob
from datetime import datetime, timedelta
from pathlib import Path

app = Flask(__name__)

@app.route('/metrics')
def metrics_dashboard():
    """Dashboard de métricas em tempo real"""
    return render_template('metrics_dashboard.html')

@app.route('/api/metrics')
def api_metrics():
    """API para métricas"""
    metrics_files = glob.glob('metrics/*.json')
    all_metrics = []
    
    for file in sorted(metrics_files)[-10:]:  # Últimos 10 arquivos
        with open(file, 'r') as f:
            for line in f:
                try:
                    metric = json.loads(line)
                    all_metrics.append(metric)
                except:
                    continue
    
    return jsonify(all_metrics)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
EOF

    log_success "Dashboard de métricas criado!"
}

# Configura backup automático
setup_auto_backup() {
    log_info "Configurando backup automático..."
    
    cat > scripts/automation/auto-backup.sh << 'EOF'
#!/bin/bash

# Backup automático inteligente
BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Backup seletivo (apenas arquivos importantes)
rsync -av --exclude='__pycache__' --exclude='venv' --exclude='node_modules' \
    --exclude='*.pyc' --exclude='logs' --exclude='tmp' \
    src/ templates/ static/ requirements.txt "$BACKUP_DIR/"

# Compacta backup
tar -czf "$BACKUP_DIR.tar.gz" "$BACKUP_DIR/"
rm -rf "$BACKUP_DIR"

# Remove backups antigos (mantém apenas os últimos 5)
ls -t backups/*.tar.gz | tail -n +6 | xargs rm -f

echo "✅ Backup criado: $BACKUP_DIR.tar.gz"
EOF

    chmod +x scripts/automation/auto-backup.sh
    log_success "Backup automático configurado!"
}

# Função principal
main() {
    log_info "🚀 INICIANDO CONFIGURAÇÃO DE SUPERPODERES..."
    
    create_project_structure
    install_dev_tools
    setup_git_hooks
    setup_monitoring
    setup_cicd
    create_metrics_dashboard
    setup_auto_backup
    
    log_success "🎉 SUPERPODERES ATIVADOS COM SUCESSO!"
    
    echo ""
    echo "🚀 COMANDOS DISPONÍVEIS:"
    echo "  python dev-assistant.py report    - Relatório completo"
    echo "  ./scripts/automation/auto-backup.sh - Backup automático"
    echo "  python src/analytics/metrics_dashboard.py - Dashboard métricas"
    echo "  ./scripts/super-powers.sh monitor - Inicia monitoramento"
    echo ""
    echo "📊 Dashboards disponíveis:"
    echo "  http://localhost:5000 - Dashboard principal"
    echo "  http://localhost:5001 - Dashboard de métricas"
    echo ""
}

# Executa comando específico se fornecido
if [ "$1" = "monitor" ]; then
    log_info "Iniciando monitoramento contínuo..."
    python scripts/monitoring/continuous-monitor.py &
    echo "Monitor executando em background (PID: $!)"
elif [ "$1" = "backup" ]; then
    ./scripts/automation/auto-backup.sh
elif [ "$1" = "install" ]; then
    main
else
    main
fi