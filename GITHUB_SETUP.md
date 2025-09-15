# 🚀 Guia para Upload do Projeto para GitHub

Este guia te ajudará a configurar o Git, SSH e fazer o upload do projeto Aviator Bot para o GitHub.

## 📋 Pré-requisitos

- Git instalado no sistema
- Conta no GitHub
- Terminal/PowerShell

## 🔑 Configuração SSH

### 1. Verificar se já existe uma chave SSH

```bash
# Verificar chaves existentes
ls -la ~/.ssh
# ou no Windows
dir C:\Users\%USERNAME%\.ssh
```

### 2. Gerar nova chave SSH (se necessário)

```bash
# Gerar chave SSH (substitua seu email)
ssh-keygen -t ed25519 -C "seu-email@exemplo.com"

# Pressione Enter para aceitar o local padrão
# Digite uma senha segura (opcional mas recomendado)
```

### 3. Adicionar chave SSH ao ssh-agent

#### Windows (PowerShell como Administrador):
```powershell
# Iniciar ssh-agent
Get-Service -Name ssh-agent | Set-Service -StartupType Manual
Start-Service ssh-agent

# Adicionar chave privada
ssh-add C:\Users\%USERNAME%\.ssh\id_ed25519
```

#### Linux/Mac:
```bash
# Iniciar ssh-agent
eval "$(ssh-agent -s)"

# Adicionar chave privada
ssh-add ~/.ssh/id_ed25519
```

### 4. Copiar chave pública

#### Windows:
```powershell
# Copiar chave pública para clipboard
Get-Content C:\Users\%USERNAME%\.ssh\id_ed25519.pub | Set-Clipboard

# Ou visualizar para copiar manualmente
type C:\Users\%USERNAME%\.ssh\id_ed25519.pub
```

#### Linux/Mac:
```bash
# Copiar para clipboard (Linux)
xclip -sel clip < ~/.ssh/id_ed25519.pub

# Copiar para clipboard (Mac)
pbcopy < ~/.ssh/id_ed25519.pub

# Ou visualizar para copiar manualmente
cat ~/.ssh/id_ed25519.pub
```

### 5. Adicionar chave SSH ao GitHub

1. Acesse [GitHub.com](https://github.com)
2. Vá em **Settings** → **SSH and GPG keys**
3. Clique em **New SSH key**
4. Cole a chave pública copiada
5. Dê um título descritivo (ex: "Meu PC - Aviator Bot")
6. Clique em **Add SSH key**

### 6. Testar conexão SSH

```bash
ssh -T git@github.com
```

Você deve ver uma mensagem como:
```
Hi username! You've successfully authenticated, but GitHub does not provide shell access.
```

## 🔧 Configuração do Git

### 1. Configurar informações globais

```bash
# Configurar nome
git config --global user.name "Seu Nome"

# Configurar email
git config --global user.email "seu-email@exemplo.com"

# Verificar configurações
git config --list
```

## 📁 Preparação do Projeto

### 1. Navegar para a pasta do projeto

```bash
cd "C:\Users\julio.amancio\Desktop\Avaiator"
```

### 2. Criar arquivo .gitignore

Crie um arquivo `.gitignore` na raiz do projeto:

```gitignore
# Dependências
node_modules/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Ambientes virtuais
venv/
env/
ENV/

# Arquivos de configuração sensíveis
credentials.json
bot_config.json
*.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Logs
*.log
logs/

# Cache
.cache/
.npm
.eslintcache

# Build do React
frontend/build/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Sistema
.DS_Store
Thumbs.db

# Selenium
*.png
*.jpg
*.jpeg
screenshots/

# Backup
*.bak
*.backup
```

### 3. Inicializar repositório Git

```bash
# Inicializar repositório
git init

# Adicionar todos os arquivos
git add .

# Fazer primeiro commit
git commit -m "🎯 Initial commit: Aviator Bot complete system

- ✅ FastAPI backend with WebSocket support
- ✅ Modern React frontend with Material-UI
- ✅ Dynamic configuration system
- ✅ Automated betting with security controls
- ✅ Real-time monitoring and logging
- ✅ Complete documentation"
```

## 🌐 Upload para GitHub

### 1. Criar repositório no GitHub

1. Acesse [GitHub.com](https://github.com)
2. Clique em **New repository**
3. Nome: `Aviator` (ou outro nome de sua escolha)
4. Descrição: `🎯 Sistema completo de automação para jogo Aviator com interface moderna`
5. **NÃO** marque "Initialize with README" (já temos um)
6. Clique em **Create repository**

### 2. Conectar repositório local ao GitHub

```bash
# Adicionar remote origin (substitua SEU_USUARIO pelo seu username)
git remote add origin git@github.com:SEU_USUARIO/Aviator.git

# Verificar remote
git remote -v

# Renomear branch principal para main (se necessário)
git branch -M main

# Fazer push inicial
git push -u origin main
```

## 📝 Comandos Úteis para Futuras Atualizações

### Workflow básico:

```bash
# Verificar status
git status

# Adicionar arquivos modificados
git add .
# ou arquivos específicos
git add arquivo.py

# Fazer commit
git commit -m "Descrição das mudanças"

# Enviar para GitHub
git push
```

### Comandos avançados:

```bash
# Ver histórico de commits
git log --oneline

# Ver diferenças
git diff

# Desfazer mudanças não commitadas
git checkout -- arquivo.py

# Voltar ao commit anterior
git reset --hard HEAD~1

# Criar nova branch
git checkout -b nova-feature

# Trocar de branch
git checkout main

# Merge de branch
git merge nova-feature
```

## 🔒 Segurança

### Arquivos que NUNCA devem ser commitados:

- `credentials.json` - Credenciais de login
- `bot_config.json` - Configurações com dados sensíveis
- `.env` - Variáveis de ambiente
- Logs com informações pessoais
- Screenshots ou dados de sessão

### Template de credentials.json:

Crie um arquivo `credentials.example.json`:

```json
{
  "username": "seu_usuario_aqui",
  "password": "sua_senha_aqui"
}
```

## 📋 Checklist Final

- [ ] SSH configurado e testado
- [ ] Git configurado com nome e email
- [ ] Arquivo .gitignore criado
- [ ] Repositório inicializado
- [ ] Primeiro commit realizado
- [ ] Repositório criado no GitHub
- [ ] Remote origin configurado
- [ ] Push inicial realizado
- [ ] Arquivos sensíveis protegidos

## 🆘 Solução de Problemas

### Erro de permissão SSH:
```bash
# Verificar se a chave está carregada
ssh-add -l

# Recarregar chave se necessário
ssh-add ~/.ssh/id_ed25519
```

### Erro de push:
```bash
# Se o repositório remoto tem commits que você não tem
git pull origin main --rebase
git push
```

### Resetar para estado limpo:
```bash
# CUIDADO: Isso remove todas as mudanças não commitadas
git reset --hard HEAD
git clean -fd
```

## 🎯 Próximos Passos

1. **Configure GitHub Actions** para CI/CD
2. **Adicione badges** ao README
3. **Configure branch protection** na branch main
4. **Crie releases** para versões estáveis
5. **Configure issues templates**

---

**✅ Seu projeto estará no GitHub e pronto para colaboração!**

Lembre-se de sempre fazer commits frequentes e usar mensagens descritivas.