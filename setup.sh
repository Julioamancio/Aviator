#!/bin/bash

echo "========================================"
echo "    AVIATOR BOT - SETUP AUTOMATICO"
echo "========================================"
echo

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para imprimir mensagens coloridas
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCESSO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[AVISO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERRO]${NC} $1"
}

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    print_error "Python3 não encontrado! Instale Python 3.8+ primeiro."
    echo "Ubuntu/Debian: sudo apt install python3 python3-pip python3-venv"
    echo "macOS: brew install python3"
    exit 1
fi

# Verificar se Node.js está instalado
if ! command -v node &> /dev/null; then
    print_error "Node.js não encontrado! Instale Node.js 16+ primeiro."
    echo "Ubuntu/Debian: curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash - && sudo apt-get install -y nodejs"
    echo "macOS: brew install node"
    exit 1
fi

print_success "Python e Node.js encontrados!"
echo

# Criar arquivo de credenciais se não existir
if [ ! -f "credentials.json" ]; then
    print_info "Criando arquivo de credenciais..."
    cp "credentials.example.json" "credentials.json"
    print_warning "Configure suas credenciais em credentials.json"
    echo
fi

# Setup do Backend
print_info "Configurando Backend..."
cd backend

# Criar ambiente virtual se não existir
if [ ! -d "venv" ]; then
    print_info "Criando ambiente virtual Python..."
    python3 -m venv venv
fi

# Ativar ambiente virtual e instalar dependências
print_info "Instalando dependências do backend..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

cd ..

# Setup do Frontend
print_info "Configurando Frontend..."
cd frontend

# Instalar dependências do Node.js
print_info "Instalando dependências do frontend..."
npm install

cd ..

echo
echo "========================================"
echo "        SETUP CONCLUÍDO COM SUCESSO!"
echo "========================================"
echo
echo "Para iniciar o sistema:"
echo
echo "1. Backend (Terminal 1):"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python main.py"
echo
echo "2. Frontend (Terminal 2):"
echo "   cd frontend"
echo "   npm start"
echo
echo "3. Acesse: http://localhost:3000"
echo
print_warning "IMPORTANTE: Configure suas credenciais em credentials.json"
echo

# Tornar o script executável
chmod +x setup.sh