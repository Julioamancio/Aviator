# 📋 Guia de Instalação e Configuração - Aviator Bot

Este guia fornece instruções detalhadas para instalar, configurar e usar o Aviator Bot.

## 🔧 Pré-requisitos

### Software Necessário
- **Python 3.8 ou superior** - [Download](https://www.python.org/downloads/)
- **Node.js 16 ou superior** - [Download](https://nodejs.org/)
- **Google Chrome** - [Download](https://www.google.com/chrome/)
- **Git** - [Download](https://git-scm.com/downloads)

### Verificação dos Pré-requisitos
```bash
# Verificar Python
python --version
# ou
python3 --version

# Verificar Node.js
node --version

# Verificar npm
npm --version

# Verificar Git
git --version
```

## 📦 Instalação Passo a Passo

### 1. Preparação do Ambiente

#### Windows
```cmd
# Criar pasta para o projeto
mkdir C:\AviatorBot
cd C:\AviatorBot

# Clonar ou extrair os arquivos do projeto
# (Os arquivos já estão na pasta Avaiator)
```

#### Linux/Mac
```bash
# Criar pasta para o projeto
mkdir ~/AviatorBot
cd ~/AviatorBot
```

### 2. Configuração do Backend

```bash
# Navegar para a pasta backend
cd backend

# Criar ambiente virtual (recomendado)
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Verificar instalação
pip list
```

### 3. Configuração do Frontend

```bash
# Navegar para a pasta frontend
cd ../frontend

# Instalar dependências
npm install

# Verificar instalação
npm list --depth=0
```

### 4. Configuração de Credenciais

Crie um arquivo `credentials.json` na pasta raiz do projeto:

```json
{
  "username": "seu_usuario_aqui",
  "password": "sua_senha_aqui"
}
```

**⚠️ IMPORTANTE**: Nunca compartilhe este arquivo ou faça commit dele no Git!

## 🚀 Primeira Execução

### 1. Iniciar o Backend

```bash
# Na pasta backend
cd backend

# Ativar ambiente virtual (se não estiver ativo)
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Iniciar servidor
python main.py
```

Você deve ver:
```
INFO:     Started server process [PID]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 2. Iniciar o Frontend

Em um novo terminal:

```bash
# Na pasta frontend
cd frontend

# Iniciar aplicação React
npm start
```

O navegador deve abrir automaticamente em `http://localhost:3000`

## ⚙️ Configuração Inicial

### 1. Configurações Básicas

1. **Acesse a interface**: `http://localhost:3000`
2. **Vá para Configuração**: Use o menu lateral
3. **Configure URLs**:
   - Site URL: `https://estrelabet.com/ptb/bet/main`
   - Game URL: `https://estrelabet.com/ptb/games/detail/casino/normal/7787`
4. **Ajuste Timeouts**:
   - Wait Timeout: 30 segundos
   - Update Interval: 2 segundos
5. **Salve as configurações**

### 2. Configuração de Elementos

1. **Acesse Elementos**: Menu lateral → Elementos
2. **Configure os seletores necessários**:

```
Cookies Button: //*[@id="cookies-bottom-modal"]/div/div[1]/a
Username Field: //*[@id="username"]
Password Field: //*[@id="password-login"]
Login Button: //*[@id="header"]/div/div[1]/div/div[2]/app-login/form/div/div/div[2]/button
Game Iframe: gm-frm
Result History: result-history
```

3. **Salve os elementos**

### 3. Definir Credenciais

1. **Na página Configuração**, clique em "Credenciais"
2. **Insira seu usuário e senha**
3. **Salve as credenciais**

## 🎯 Primeiro Uso

### 1. Teste de Conexão

1. **Dashboard**: Verifique se mostra "Conectado"
2. **Status do Bot**: Deve mostrar "Parado"
3. **Clique em "Iniciar Bot"**
4. **Acompanhe os logs** na página Logs

### 2. Configurar Estratégia de Apostas

1. **Acesse Apostas**: Menu lateral → Apostas
2. **Escolha uma estratégia**:
   - **Conservadora**: Baixo risco, cashout em 2x
   - **Moderada**: Risco médio, cashout em 3x
   - **Agressiva**: Alto risco, cashout em 5x
3. **Configure limites de segurança**:
   - Perda máxima: R$ 50,00
   - Ganho máximo: R$ 100,00
4. **Inicie as apostas** (apenas quando o bot estiver rodando)

## 🔍 Monitoramento

### Dashboard
- **Saldo atual** e lucro total
- **Taxa de vitórias**
- **Estratégias encontradas**
- **Gráficos em tempo real**

### Logs
- **Filtros por nível**: Info, Aviso, Erro
- **Busca por texto**
- **Exportação de logs**

### Monitoramento
- **Resultados recentes**
- **Análise de multiplicadores**
- **Estatísticas detalhadas**

## 🛠️ Solução de Problemas

### Problemas Comuns

#### Backend não inicia
```bash
# Verificar se a porta 8000 está livre
netstat -an | findstr :8000

# Matar processo se necessário (Windows)
taskkill /f /im python.exe

# Reinstalar dependências
pip install -r requirements.txt --force-reinstall
```

#### Frontend não carrega
```bash
# Limpar cache do npm
npm cache clean --force

# Reinstalar dependências
rm -rf node_modules package-lock.json
npm install

# Verificar porta 3000
netstat -an | findstr :3000
```

#### Bot não encontra elementos
1. **Verifique se o site mudou**
2. **Use F12 para inspecionar elementos**
3. **Atualize os XPaths na página Elementos**
4. **Teste um elemento por vez**

#### Erro de login
1. **Verifique credenciais**
2. **Confirme se o site está acessível**
3. **Verifique se não há captcha**
4. **Tente login manual primeiro**

### Logs de Debug

Para ativar logs detalhados, edite `backend/main.py`:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Verificação de Saúde

Teste os endpoints da API:

```bash
# Verificar saúde da API
curl http://localhost:8000/health

# Verificar configuração
curl http://localhost:8000/config

# Verificar status do bot
curl http://localhost:8000/bot/status
```

## 🔒 Segurança

### Boas Práticas

1. **Nunca compartilhe credenciais**
2. **Use senhas fortes**
3. **Mantenha o software atualizado**
4. **Configure limites de segurança**
5. **Monitore regularmente**

### Backup de Configurações

```bash
# Fazer backup das configurações
cp bot_config.json bot_config_backup.json
cp credentials.json credentials_backup.json
```

## 📊 Otimização de Performance

### Configurações Recomendadas

```json
{
  "headless": true,
  "wait_timeout": 20,
  "update_interval": 3,
  "max_retries": 2
}
```

### Monitoramento de Recursos

- **CPU**: Mantenha abaixo de 50%
- **Memória**: Máximo 1GB
- **Rede**: Conexão estável necessária

## 🆘 Suporte

### Antes de Pedir Ajuda

1. **Verifique os logs** na página Logs
2. **Teste configurações básicas**
3. **Verifique conexão com internet**
4. **Reinicie backend e frontend**

### Informações para Suporte

- Versão do Python
- Versão do Node.js
- Sistema operacional
- Logs de erro
- Configurações utilizadas

### Contato

- **Issues**: GitHub Issues
- **Email**: suporte@aviatorbot.com
- **Documentação**: Wiki do projeto

---

**✅ Instalação Concluída!**

Se você seguiu todos os passos, o Aviator Bot deve estar funcionando corretamente. Lembre-se de sempre usar com responsabilidade e dentro dos limites legais.