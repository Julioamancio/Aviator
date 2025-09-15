#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modelos de dados para o Aviator Bot
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum

class BotStatusEnum(str, Enum):
    """Estados possíveis do bot"""
    STOPPED = "stopped"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    ERROR = "error"
    LOGGED_IN = "logged_in"
    IN_GAME = "in_game"
    MONITORING = "monitoring"
    BETTING = "betting"

class StrategyTypeEnum(str, Enum):
    """Tipos de estratégia de aposta"""
    CONSERVATIVE = "conservative"
    MODERATE = "moderate"
    AGGRESSIVE = "aggressive"
    CUSTOM = "custom"

class BotConfig(BaseModel):
    """Configuração principal do bot"""
    site_url: str = Field(default="https://estrelabet.com/ptb/bet/main", description="URL do site")
    game_url: str = Field(default="https://estrelabet.com/ptb/games/detail/casino/normal/7787", description="URL do jogo")
    headless: bool = Field(default=False, description="Executar em modo headless")
    wait_timeout: int = Field(default=30, ge=5, le=120, description="Timeout para aguardar elementos (segundos)")
    strategy_threshold: float = Field(default=2.0, ge=1.0, le=10.0, description="Threshold para estratégia")
    history_size: int = Field(default=10, ge=5, le=50, description="Tamanho do histórico")
    min_strategy_checks: int = Field(default=4, ge=2, le=10, description="Mínimo de verificações para estratégia")
    update_interval: int = Field(default=2, ge=1, le=10, description="Intervalo de atualização (segundos)")
    max_retries: int = Field(default=3, ge=1, le=10, description="Máximo de tentativas")
    
class ElementConfig(BaseModel):
    """Configuração de elementos da página"""
    cookies_button: str = Field(default='//*[@id="cookies-bottom-modal"]/div/div[1]/a', description="XPath do botão de cookies")
    username_field: str = Field(default='//*[@id="username"]', description="XPath do campo de usuário")
    password_field: str = Field(default='//*[@id="password-login"]', description="XPath do campo de senha")
    login_button: str = Field(default='//*[@id="header"]/div/div[1]/div/div[2]/app-login/form/div/div/div[2]/button', description="XPath do botão de login")
    game_iframe: str = Field(default='gm-frm', description="ID do iframe do jogo")
    result_history: str = Field(default='result-history', description="Classe do histórico de resultados")
    bet_input: str = Field(default='', description="XPath do campo de aposta")
    bet_button: str = Field(default='', description="XPath do botão de apostar")
    cashout_button: str = Field(default='', description="XPath do botão de cashout")
    multiplier_display: str = Field(default='', description="XPath do display do multiplicador")
    balance_display: str = Field(default='', description="XPath do display do saldo")

class LoginCredentials(BaseModel):
    """Credenciais de login"""
    username: str = Field(..., min_length=1, description="Nome de usuário")
    password: str = Field(..., min_length=1, description="Senha")

class BettingStrategy(BaseModel):
    """Configuração de estratégia de aposta"""
    amount: float = Field(..., gt=0, description="Valor da aposta")
    strategy_type: StrategyTypeEnum = Field(..., description="Tipo de estratégia")
    auto_cashout: Optional[float] = Field(None, gt=1.0, description="Multiplicador para cashout automático")
    max_loss: Optional[float] = Field(None, gt=0, description="Perda máxima permitida")
    max_win: Optional[float] = Field(None, gt=0, description="Ganho máximo desejado")
    stop_on_loss: bool = Field(default=True, description="Parar ao atingir perda máxima")
    stop_on_win: bool = Field(default=True, description="Parar ao atingir ganho máximo")
    progressive_betting: bool = Field(default=False, description="Aposta progressiva")
    progression_factor: float = Field(default=1.5, ge=1.1, le=3.0, description="Fator de progressão")
    reset_on_win: bool = Field(default=True, description="Resetar progressão ao ganhar")

class GameResult(BaseModel):
    """Resultado de uma rodada do jogo"""
    multiplier: float = Field(..., description="Multiplicador da rodada")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp da rodada")
    bet_amount: Optional[float] = Field(None, description="Valor apostado")
    cashout_multiplier: Optional[float] = Field(None, description="Multiplicador do cashout")
    profit: Optional[float] = Field(None, description="Lucro/prejuízo")
    strategy_triggered: bool = Field(default=False, description="Se a estratégia foi ativada")

class SessionStats(BaseModel):
    """Estatísticas da sessão"""
    start_time: datetime = Field(default_factory=datetime.now, description="Início da sessão")
    total_rounds: int = Field(default=0, description="Total de rodadas monitoradas")
    strategies_found: int = Field(default=0, description="Estratégias encontradas")
    bets_placed: int = Field(default=0, description="Apostas realizadas")
    wins: int = Field(default=0, description="Vitórias")
    losses: int = Field(default=0, description="Derrotas")
    total_bet: float = Field(default=0.0, description="Total apostado")
    total_profit: float = Field(default=0.0, description="Lucro total")
    current_balance: Optional[float] = Field(None, description="Saldo atual")
    max_multiplier: float = Field(default=0.0, description="Maior multiplicador visto")
    avg_multiplier: float = Field(default=0.0, description="Multiplicador médio")
    errors: int = Field(default=0, description="Número de erros")
    uptime: Optional[str] = Field(None, description="Tempo de execução")
    
    def calculate_win_rate(self) -> float:
        """Calcula a taxa de vitórias"""
        if self.bets_placed == 0:
            return 0.0
        return (self.wins / self.bets_placed) * 100
    
    def calculate_roi(self) -> float:
        """Calcula o ROI (Return on Investment)"""
        if self.total_bet == 0:
            return 0.0
        return (self.total_profit / self.total_bet) * 100

class BotStatus(BaseModel):
    """Status detalhado do bot"""
    status: BotStatusEnum = Field(..., description="Status atual do bot")
    is_running: bool = Field(default=False, description="Se o bot está em execução")
    is_betting: bool = Field(default=False, description="Se está apostando automaticamente")
    current_balance: Optional[float] = Field(None, description="Saldo atual")
    last_multiplier: Optional[float] = Field(None, description="Último multiplicador")
    last_update: datetime = Field(default_factory=datetime.now, description="Última atualização")
    error_message: Optional[str] = Field(None, description="Mensagem de erro")
    current_strategy: Optional[BettingStrategy] = Field(None, description="Estratégia atual")
    recent_results: List[float] = Field(default_factory=list, description="Resultados recentes")
    
class LogEntry(BaseModel):
    """Entrada de log"""
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp do log")
    level: str = Field(..., description="Nível do log (INFO, WARNING, ERROR)")
    message: str = Field(..., description="Mensagem do log")
    component: Optional[str] = Field(None, description="Componente que gerou o log")

class WebSocketMessage(BaseModel):
    """Mensagem WebSocket"""
    type: str = Field(..., description="Tipo da mensagem")
    data: Dict[str, Any] = Field(..., description="Dados da mensagem")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp da mensagem")

class ApiResponse(BaseModel):
    """Resposta padrão da API"""
    success: bool = Field(..., description="Se a operação foi bem-sucedida")
    message: str = Field(..., description="Mensagem de resposta")
    data: Optional[Dict[str, Any]] = Field(None, description="Dados adicionais")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp da resposta")

class ConfigPreset(BaseModel):
    """Preset de configuração"""
    name: str = Field(..., description="Nome do preset")
    description: str = Field(..., description="Descrição do preset")
    config: BotConfig = Field(..., description="Configuração do bot")
    elements: ElementConfig = Field(..., description="Configuração de elementos")
    strategy: Optional[BettingStrategy] = Field(None, description="Estratégia de aposta")
    created_at: datetime = Field(default_factory=datetime.now, description="Data de criação")

class SystemInfo(BaseModel):
    """Informações do sistema"""
    python_version: str = Field(..., description="Versão do Python")
    selenium_version: str = Field(..., description="Versão do Selenium")
    chrome_version: Optional[str] = Field(None, description="Versão do Chrome")
    os_info: str = Field(..., description="Informações do SO")
    memory_usage: float = Field(..., description="Uso de memória (MB)")
    cpu_usage: float = Field(..., description="Uso de CPU (%)")
    uptime: str = Field(..., description="Tempo de execução")