@echo off
echo === Instalacao do Dashboard Auditoria FB ===
echo.

REM Verificar Python
echo Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo X Python nao encontrado. Por favor, instale Python 3.8 ou superior.
    pause
    exit /b 1
)

echo OK Python encontrado
echo.

REM Criar ambiente virtual
echo Criando ambiente virtual...
if exist venv (
    echo Ambiente virtual ja existe. Removendo...
    rmdir /s /q venv
)

python -m venv venv
if %errorlevel% neq 0 (
    echo X Erro ao criar ambiente virtual
    pause
    exit /b 1
)

echo OK Ambiente virtual criado
echo.

REM Ativar ambiente virtual
echo Ativando ambiente virtual...
call venv\Scripts\activate.bat

REM Atualizar pip
echo Atualizando pip...
python -m pip install --upgrade pip

REM Instalar dependencias
echo Instalando dependencias...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo X Erro ao instalar dependencias
    pause
    exit /b 1
)

echo.
echo OK Instalacao concluida com sucesso!
echo.
echo Para executar a aplicacao:
echo 1. Ative o ambiente virtual: venv\Scripts\activate
echo 2. Execute: python app.py
echo.
echo A aplicacao estara disponivel em http://localhost:5000
pause