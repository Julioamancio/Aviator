# 🚀 Guia Manual para Upload do Projeto no GitHub

**IMPORTANTE**: O Git não está instalado no seu sistema. Siga este guia para instalar e fazer o upload.

## 📥 1. Instalar Git

### Opção A: Download Direto
1. Acesse: https://git-scm.com/download/win
2. Baixe a versão mais recente
3. Execute o instalador com as configurações padrão
4. Reinicie o terminal após a instalação

### Opção B: Via Winget (Windows 11)
```powershell
winget install --id Git.Git -e --source winget
```

### Opção C: Via Chocolatey
```powershell
# Instalar Chocolatey primeiro (se não tiver)
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Instalar Git
choco install git
```

## 🔧 2. Configurar Git (Após Instalação)

Abra um novo PowerShell/Terminal e execute:

```bash
# Configurar nome
git config --global user.name "Julio Amancio"

# Configurar email (use seu email do GitHub)
git config --global user.email "seu-email@exemplo.com"

# Verificar configuração
git config --list
```

## 🔑 3. Configurar SSH (Recomendado)

```bash
# Gerar chave SSH
ssh-keygen -t ed25519 -C "seu-email@exemplo.com"

# Pressione Enter para aceitar o local padrão
# Digite uma senha (opcional)

# Iniciar ssh-agent
Get-Service -Name ssh-agent | Set-Service -StartupType Manual
Start-Service ssh-agent

# Adicionar chave
ssh-add C:\Users\%USERNAME%\.ssh\id_ed25519

# Copiar chave pública
type C:\Users\%USERNAME%\.ssh\id_ed25519.pub
```

### Adicionar SSH ao GitHub:
1. Copie a chave pública exibida
2. Vá em GitHub.com → Settings → SSH and GPG keys
3. Clique "New SSH key"
4. Cole a chave e salve

## 📁 4. Preparar o Repositório Local

No terminal, navegue até a pasta do projeto:

```bash
cd "C:\Users\julio.amancio\Desktop\Avaiator"

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

## 🌐 5. Configurar Repositório no GitHub

### Opção A: Repositório Novo
1. Vá em https://github.com/new
2. Nome: `Aviator`
3. Descrição: `🎯 Sistema completo de automação para jogo Aviator`
4. **NÃO** marque "Initialize with README"
5. Clique "Create repository"

### Opção B: Limpar Repositório Existente
Se já existe um repositório em https://github.com/Julioamancio/Aviator:

1. Vá no repositório
2. Settings → Danger Zone → Delete this repository
3. Digite o nome para confirmar
4. Crie um novo repositório (Opção A)

## 🚀 6. Upload para GitHub

```bash
# Conectar ao repositório remoto
git remote add origin git@github.com:Julioamancio/Aviator.git

# Ou se preferir HTTPS:
# git remote add origin https://github.com/Julioamancio/Aviator.git

# Verificar remote
git remote -v

# Renomear branch para main
git branch -M main

# Fazer push (primeira vez)
git push -u origin main
```

## 🔄 7. Comandos para Futuras Atualizações

```bash
# Verificar status
git status

# Adicionar mudanças
git add .

# Commit
git commit -m "Descrição das mudanças"

# Push
git push
```

## 🛠️ 8. Solução de Problemas

### Erro de Autenticação SSH:
```bash
# Testar conexão SSH
ssh -T git@github.com

# Se falhar, verificar se a chave está carregada
ssh-add -l

# Recarregar chave se necessário
ssh-add C:\Users\%USERNAME%\.ssh\id_ed25519
```

### Erro de Push (repositório não vazio):
```bash
# Forçar push (CUIDADO: sobrescreve tudo no GitHub)
git push --force-with-lease origin main

# Ou fazer pull primeiro
git pull origin main --allow-unrelated-histories
git push
```

### Erro de Credenciais HTTPS:
```bash
# Configurar credential helper
git config --global credential.helper manager-core

# Na primeira vez, será solicitado login do GitHub
```

## 📋 9. Checklist Final

- [ ] Git instalado e configurado
- [ ] SSH configurado (recomendado)
- [ ] Repositório local inicializado
- [ ] Primeiro commit realizado
- [ ] Repositório GitHub criado/limpo
- [ ] Remote origin configurado
- [ ] Push inicial realizado
- [ ] Verificar se todos os arquivos estão no GitHub

## 🎯 10. Verificação Final

Após o upload, verifique se estes arquivos estão no GitHub:

```
✅ README.md
✅ INSTALLATION.md
✅ GITHUB_SETUP.md
✅ LICENSE
✅ .gitignore
✅ credentials.example.json
✅ setup.bat / setup.sh
✅ backend/ (pasta completa)
✅ frontend/ (pasta completa)
✅ aviator_bot.py
✅ aviator_bot_optimized.py
✅ requirements.txt
```

**❌ NÃO devem aparecer:**
- credentials.json (dados reais)
- node_modules/
- venv/
- __pycache__/
- *.log

## 🆘 Suporte

Se encontrar problemas:

1. **Erro de instalação do Git**: Tente como administrador
2. **Erro de SSH**: Use HTTPS temporariamente
3. **Erro de push**: Verifique se o repositório está vazio
4. **Arquivos não aparecem**: Verifique o .gitignore

---

**✅ Após seguir este guia, seu projeto estará no GitHub!**

Lembre-se de sempre fazer commits regulares e usar mensagens descritivas.