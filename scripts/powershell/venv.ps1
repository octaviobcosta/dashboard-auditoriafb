# Script direto para ativar venv

$venvPaths = @(
    ".\venv\Scripts\Activate.ps1",
    ".\env\Scripts\Activate.ps1", 
    ".\.venv\Scripts\Activate.ps1",
    ".\virtualenv\Scripts\Activate.ps1"
)

$activated = $false

foreach ($path in $venvPaths) {
    if (Test-Path $path) {
        Write-Host "[OK] Ativando venv..." -ForegroundColor Green
        & $path
        $activated = $true
        Write-Host "[ATIVO] Ambiente virtual ativo!" -ForegroundColor Yellow
        break
    }
}

if (-not $activated) {
    Write-Host "[ERRO] Venv nao encontrado!" -ForegroundColor Red
    $create = Read-Host "Criar ambiente virtual? (s/n)"
    if ($create -eq 's' -or $create -eq 'S') {
        python -m venv venv
        Write-Host "[OK] Venv criado! Execute novamente: .\venv.ps1" -ForegroundColor Green
    }
}