# 🎯 Aviator Bot - Sistema Avançado de Automação

![Aviator Bot](https://img.shields.io/badge/Aviator-Bot-blue?style=for-the-badge&logo=robot)
![Version](https://img.shields.io/badge/version-1.0.0-green?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-yellow?style=for-the-badge)

Um sistema completo de automação para o jogo Aviator com interface web moderna, controles de segurança avançados e monitoramento em tempo real.

## 🚀 Características Principais

### 🎮 Interface Moderna
- **Dashboard Interativo**: Controle completo com estatísticas em tempo real
- **Sidebar Responsiva**: Navegação intuitiva e moderna
- **Tema Escuro/Claro**: Interface personalizável
- **Gráficos Dinâmicos**: Visualização de dados em tempo real

### 🔧 Configuração Flexível
- **Paths Dinâmicos**: Configure XPath, IDs e classes facilmente
- **URLs Personalizáveis**: Adapte para diferentes sites
- **Estratégias Configuráveis**: Múltiplas opções de automação
- **Credenciais Seguras**: Armazenamento criptografado

### 🎰 Apostas Inteligentes
- **Estratégias Pré-definidas**: Conservadora, Moderada e Agressiva
- **Aposta Progressiva**: Sistema de progressão configurável
- **Limites de Segurança**: Controle de perdas e ganhos
- **Cashout Automático**: Saída automática em multiplicadores específicos

### 📊 Monitoramento Avançado
- **Tempo Real**: Acompanhamento instantâneo de resultados
- **Histórico Detalhado**: Análise de padrões e tendências
- **Logs Completos**: Sistema de logging com filtros
- **WebSocket**: Comunicação bidirecional em tempo real

## 🏗️ Arquitetura do Sistema

```
Aviator Bot/
├── backend/                 # API FastAPI
│   ├── main.py             # Servidor principal
│   ├── models.py           # Modelos de dados
│   ├── bot_controller.py   # Controlador do bot
│   ├── websocket_manager.py # Gerenciador WebSocket
│   └── requirements.txt    # Dependências Python
├── frontend/               # Interface React
│   ├── src/
│   │   ├── components/     # Componentes reutilizáveis
│   │   ├── pages/         # Páginas da aplicação
│   │   ├── contexts/      # Contextos React
│   │   └── App.tsx        # Aplicação principal
│   └── package.json       # Dependências Node.js
├── aviator_bot.py         # Bot original
├── aviator_bot_optimized.py # Bot otimizado
└── requirements.txt       # Dependências gerais
```

## 🛠️ Tecnologias Utilizadas

### Backend
- **FastAPI**: Framework web moderno e rápido
- **Selenium**: Automação de navegador
- **WebSocket**: Comunicação em tempo real
- **Pydantic**: Validação de dados
- **Uvicorn**: Servidor ASGI

### Frontend
- **React 18**: Biblioteca de interface moderna
- **TypeScript**: Tipagem estática
- **Material-UI**: Componentes de interface
- **Framer Motion**: Animações fluidas
- **Recharts**: Gráficos interativos
- **React Hook Form**: Gerenciamento de formulários

### Automação
- **Chrome WebDriver**: Controle do navegador
- **XPath/CSS Selectors**: Localização de elementos
- **Estratégias Adaptáveis**: Algoritmos de decisão

## 📦 Instalação

### Pré-requisitos
- Python 3.8+
- Node.js 16+
- Google Chrome
- Git

### 1. Clone o Repositório
```bash
git clone https://github.com/seu-usuario/aviator-bot.git
cd aviator-bot
```

### 2. Configuração do Backend
```bash
cd backend
pip install -r requirements.txt
```

### 3. Configuração do Frontend
```bash
cd frontend
npm install
```

### 4. Configuração de Credenciais
Crie um arquivo `credentials.json` no diretório raiz:
```json
{
  "username": "seu_usuario",
  "password": "sua_senha"
}
```

## 🚀 Execução

### Iniciar Backend
```bash
cd backend
python main.py
```
O servidor estará disponível em: `http://localhost:8000`

### Iniciar Frontend
```bash
cd frontend
npm start
```
A interface estará disponível em: `http://localhost:3000`

## 📖 Guia de Uso

### 1. Configuração Inicial
1. Acesse a página **Configuração**
2. Configure as URLs do site e jogo
3. Defina os timeouts e parâmetros
4. Salve as configurações

### 2. Configuração de Elementos
1. Vá para a página **Elementos**
2. Configure os XPaths dos elementos da página
3. Use as ferramentas de desenvolvedor (F12) para encontrar seletores
4. Teste e valide os elementos

### 3. Definir Credenciais

#### **Opção A: Configuração Automática (Recomendado)**
```bash
# Configurar credenciais interativamente
python configure_credentials.py
```

#### **Opção B: Pen Drive Seguro (E:\AVIATOR)**
```bash
# 1. Configurar credenciais localmente
python configure_credentials.py

# 2. Copiar para pen drive
python copy_to_pendrive.py

# 3. Verificar pen drive
python copy_to_pendrive.py --verify
```

#### **Opção C: Interface Web**
1. Na página **Configuração**, clique em "Credenciais"
2. Insira seu usuário e senha
3. As credenciais são armazenadas de forma segura

### 4. Configurar Estratégia de Apostas
1. Acesse a página **Apostas**
2. Escolha uma estratégia pré-definida ou personalize
3. Configure limites de segurança
4. Defina valores e multiplicadores

### 5. Iniciar o Bot
1. No **Dashboard**, clique em "Iniciar Bot"
2. Acompanhe o status e estatísticas
3. Monitor os logs em tempo real
4. Use "Parar Bot" quando necessário

## 🔒 Recursos de Segurança

### Controles de Risco
- **Limites de Perda**: Parada automática ao atingir limite
- **Limites de Ganho**: Proteção contra ganância
- **Timeout de Segurança**: Prevenção de travamentos
- **Validação de Elementos**: Verificação antes de ações

### Proteção de Dados
- **Credenciais Criptografadas**: Armazenamento seguro
- **Logs Detalhados**: Rastreabilidade completa
- **Backup de Configurações**: Recuperação de dados
- **Validação de Entrada**: Prevenção de ataques

## 📊 Monitoramento

### Dashboard
- Saldo atual e lucro total
- Taxa de vitórias e estatísticas
- Gráficos de multiplicadores
- Status do bot em tempo real

### Logs
- Filtros por nível e componente
- Busca em tempo real
- Exportação de logs
- Histórico detalhado

### Monitoramento
- Resultados recentes
- Análise de padrões
- Distribuição de multiplicadores
- Métricas de performance

## ⚙️ Configurações Avançadas

### Estratégias Personalizadas
```python
# Exemplo de estratégia personalizada
strategy = {
    "amount": 10.0,
    "strategy_type": "custom",
    "auto_cashout": 2.5,
    "max_loss": 100.0,
    "max_win": 500.0,
    "progressive_betting": True,
    "progression_factor": 1.5
}
```

### Elementos Customizados
```json
{
  "cookies_button": "//*[@id='accept-cookies']",
  "username_field": "//input[@name='username']",
  "password_field": "//input[@type='password']",
  "login_button": "//button[contains(text(), 'Login')]"
}
```

## 🐛 Solução de Problemas

### Problemas Comuns

**Bot não inicia**
- Verifique se o Chrome está instalado
- Confirme as credenciais
- Verifique a conexão com a internet

**Elementos não encontrados**
- Atualize os XPaths na página Elementos
- Use as ferramentas de desenvolvedor
- Verifique se o site mudou a estrutura

**Conexão WebSocket falha**
- Verifique se o backend está rodando
- Confirme a porta 8000 está livre
- Reinicie o servidor se necessário

### Logs de Debug
Ative o modo debug nas configurações para logs detalhados:
```python
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## ⚠️ Aviso Legal

**IMPORTANTE**: Este software é fornecido apenas para fins educacionais e de pesquisa. O uso deste bot para apostas reais pode:

- Violar os termos de serviço de sites de apostas
- Resultar em perdas financeiras
- Ser considerado ilegal em algumas jurisdições

**Use por sua própria conta e risco.** Os desenvolvedores não se responsabilizam por:
- Perdas financeiras
- Violações de termos de serviço
- Consequências legais
- Problemas técnicos

## 📞 Suporte

- **Issues**: [GitHub Issues](https://github.com/seu-usuario/aviator-bot/issues)
- **Documentação**: [Wiki](https://github.com/seu-usuario/aviator-bot/wiki)
- **Email**: suporte@aviatorbot.com

## 🙏 Agradecimentos

- Comunidade React e FastAPI
- Desenvolvedores do Selenium
- Contribuidores do projeto
- Beta testers

---

**Desenvolvido com ❤️ para a comunidade**

*Última atualização: Janeiro 2025*