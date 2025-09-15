# 📦 Instalação do Node.js para Frontend

## 🚀 **Por que Precisa do Node.js?**

O frontend React profissional precisa do Node.js para:
- ✅ **Interface visual completa** para configurar paths e IDs
- ✅ **Editor dinâmico** de elementos da página
- ✅ **Configuração visual** de estratégias de aposta
- ✅ **Monitoramento em tempo real** com gráficos
- ✅ **Controle total** do bot via interface

## 📥 **Como Instalar Node.js**

### **Opção 1: Download Oficial (Recomendado)**
1. **Acesse**: https://nodejs.org/
2. **Baixe**: Versão LTS (Long Term Support)
3. **Execute**: O instalador baixado
4. **Siga**: As instruções padrão
5. **Reinicie**: O terminal após a instalação

### **Opção 2: Via Winget**
```powershell
winget install OpenJS.NodeJS
```

### **Opção 3: Via Chocolatey**
```powershell
choco install nodejs
```

## ✅ **Verificar Instalação**

Após instalar, abra um **novo terminal** e teste:

```bash
# Verificar Node.js
node --version
# Deve mostrar algo como: v18.17.0

# Verificar npm
npm --version
# Deve mostrar algo como: 9.6.7
```

## 🚀 **Iniciar Frontend Após Instalação**

```bash
# 1. Navegar para frontend
cd frontend

# 2. Instalar dependências
npm install

# 3. Iniciar servidor de desenvolvimento
npm start

# 4. Acessar interface
# http://localhost:3000
```

## 🎯 **O que Você Terá com o Frontend**

### **📊 Dashboard Profissional**
- 📈 **Gráficos em tempo real** dos multiplicadores
- 📊 **Estatísticas detalhadas** da sessão
- 🎮 **Controles do bot** (Start/Stop/Pause)
- 💰 **Saldo e lucros** atualizados em tempo real

### **⚙️ Configuração Completa**
- 🌐 **URLs do site** (editáveis)
- 🔍 **Paths dos elementos** (XPath/CSS)
- 🎯 **IDs dos botões** (configuráveis)
- 🔧 **Seletores personalizados**

### **🎰 Estratégias de Aposta**
- 💵 **Valor da aposta** (slider visual)
- 📈 **Multiplicador de cashout** (configurável)
- 🛡️ **Limites de perda/ganho** (controles visuais)
- 📊 **Estratégias predefinidas** (Conservadora, Moderada, Agressiva)

### **🔍 Editor de Elementos**
- 🖱️ **Interface visual** para configurar seletores
- 🎯 **Teste em tempo real** dos elementos
- 📝 **Validação automática** dos paths
- 💾 **Salvamento automático** das configurações

### **📡 Monitoramento Avançado**
- 📊 **Gráficos interativos** (Chart.js)
- 🔄 **Atualizações em tempo real** (WebSocket)
- 📈 **Histórico de multiplicadores**
- 📋 **Logs detalhados** com filtros

### **🎨 Interface Moderna**
- 🌙 **Modo escuro/claro**
- 📱 **Responsivo** (funciona no celular)
- ⚡ **Animações suaves** (Framer Motion)
- 🎯 **Material-UI** (design profissional)

## 🔧 **Funcionalidades Principais**

### **1. Configuração de Elementos**
```javascript
// Interface visual para configurar:
{
  "cookies_button": "//button[contains(text(), 'Aceitar')]",
  "username_field": "//input[@type='email']",
  "password_field": "//input[@type='password']",
  "login_button": "//button[contains(text(), 'Entrar')]",
  "bet_input": "//input[@placeholder*='aposta']",
  "bet_button": "//button[contains(@class, 'bet-button')]",
  "cashout_button": "//button[contains(text(), 'Retirar')]"
}
```

### **2. Configuração de URLs**
```javascript
// Interface para editar:
{
  "site_url": "https://1-wins.br.com/",
  "game_url": "https://1whfxh.life/casino/play/spribe_aviator"
}
```

### **3. Estratégias Visuais**
```javascript
// Controles visuais para:
{
  "amount": 1.0,           // Slider para valor
  "auto_cashout": 1.5,     // Input para multiplicador
  "max_loss": 50.0,        // Limite de perda
  "max_win": 100.0,        // Meta de ganho
  "strategy_type": "conservative" // Dropdown
}
```

## 🎉 **Resultado Final**

Com o Node.js instalado, você terá:

- 🖥️ **Interface profissional** em http://localhost:3000
- ⚙️ **Configuração visual** de todos os elementos
- 📊 **Dashboard completo** com gráficos
- 🎮 **Controle total** do bot
- 📱 **Responsivo** para qualquer dispositivo
- 🔄 **Tempo real** com WebSocket

## 🚨 **Importante**

**Sem o frontend, você só tem a API!**

Com o frontend você tem:
- ✅ **Interface visual completa**
- ✅ **Configuração fácil** de paths/IDs
- ✅ **Monitoramento profissional**
- ✅ **Controle total** do sistema

---

**🎯 Instale o Node.js agora para ter a experiência completa!**

**📥 Download**: https://nodejs.org/