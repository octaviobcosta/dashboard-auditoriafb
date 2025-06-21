# Script para executar run.py com venv ativado

# Volta para a raiz do projeto
Push-Location "$PSScriptRoot\..\.."

# Ativa o venv
& "$PSScriptRoot\venv.ps1"

# Executa run.py
Write-Host "[RUN] Executando aplicação Flask..." -ForegroundColor Cyan
python run.py

# Retorna ao diretório original
Pop-Location