@echo off
echo ========================================
echo    AVIATOR BOT - SETUP AUTOMATICO
echo ========================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Python nao encontrado! Instale Python 3.8+ primeiro.
    echo Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Verificar se Node.js está instalado
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Node.js nao encontrado! Instale Node.js 16+ primeiro.
    echo Download: https://nodejs.org/
    pause
    exit /b 1
)

echo [INFO] Python e Node.js encontrados!
echo.

REM Criar arquivo de credenciais se não existir
if not exist "credentials.json" (
    echo [INFO] Criando arquivo de credenciais...
    copy "credentials.example.json" "credentials.json" >nul
    echo [AVISO] Configure suas credenciais em credentials.json
    echo.
)

REM Setup do Backend
echo [INFO] Configurando Backend...
cd backend

REM Criar ambiente virtual se não existir
if not exist "venv" (
    echo [INFO] Criando ambiente virtual Python...
    python -m venv venv
)

REM Ativar ambiente virtual e instalar dependências
echo [INFO] Instalando dependencias do backend...
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt

cd ..

REM Setup do Frontend
echo [INFO] Configurando Frontend...
cd frontend

REM Instalar dependências do Node.js
echo [INFO] Instalando dependencias do frontend...
npm install

cd ..

echo.
echo ========================================
echo        SETUP CONCLUIDO COM SUCESSO!
echo ========================================
echo.
echo Para iniciar o sistema:
echo.
echo 1. Backend (Terminal 1):
echo    cd backend
echo    venv\Scripts\activate
echo    python main.py
echo.
echo 2. Frontend (Terminal 2):
echo    cd frontend
echo    npm start
echo.
echo 3. Acesse: http://localhost:3000
echo.
echo IMPORTANTE: Configure suas credenciais em credentials.json
echo.
pause