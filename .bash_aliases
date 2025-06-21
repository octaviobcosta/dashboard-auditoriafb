# 🚀 SUPERPODERES DO DASHBOARD - Aliases Avançados

# === COMANDOS PRINCIPAIS ===
alias dashboard-start="python src/app.py"
alias dashboard-dev="python src/app.py --debug"
alias dashboard-test="python -m pytest -v"
alias dashboard-deploy="./scripts/auto-deploy.sh"

# === SUPERPODERES ATIVADOS ===
alias superpowers="./scripts/super-powers.sh"
alias dev-report="python dev-assistant.py report"
alias ux-analysis="python ux-analyzer.py"
alias metrics-dashboard="python src/analytics/metrics_dashboard.py"

# === ANÁLISES AUTOMÁTICAS ===
alias analyze-code="python dev-assistant.py analyze"
alias monitor-performance="python dev-assistant.py monitor"
alias optimize-code="python dev-assistant.py optimize"
alias check-ux="python ux-analyzer.py"

# === GIT SUPERPOWERS ===
alias gst="git status"
alias gad="git add ."
alias gcm="git commit -m"
alias gps="git push"
alias gpl="git pull"
alias gsync="gpl && gad && gcm 'sync: automated sync' && gps"
alias gquick="gad && gcm 'quick fix' && gps"

# === AUTOMAÇÃO ===
alias quick-backup="./scripts/automation/auto-backup.sh"
alias start-monitor="./scripts/super-powers.sh monitor"
alias install-superpowers="./scripts/super-powers.sh install"

# === DESENVOLVIMENTO ===
alias clean-cache="find . -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true"
alias watch-logs="tail -f logs/*.log 2>/dev/null || echo 'No log files found'"
alias server-status="ps aux | grep python | grep app.py"

# === UTILITÁRIOS ===
alias project-info="echo '🚀 Dashboard Auditoria FB' && echo 'Desenvolvido com superpoderes!' && pwd && git status --porcelain | wc -l | xargs echo 'Arquivos modificados:'"
alias help-superpowers="echo '🚀 SUPERPODERES DISPONÍVEIS:' && echo 'superpowers        - Ativa todos os poderes' && echo 'dev-report         - Relatório completo' && echo 'ux-analysis        - Análise UX/UI' && echo 'quick-backup       - Backup automático' && echo 'gsync              - Git sync automático'"

# === MODO DEUS ===
alias god-mode="echo '⚡ MODO DEUS ATIVADO!' && superpowers && dev-report && ux-analysis && quick-backup && echo '🎉 Análise completa realizada!'"

echo "🚀 SUPERPODERES carregados! Digite 'help-superpowers' para ver comandos disponíveis."