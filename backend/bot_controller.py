#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Controlador do Bot Aviator
Gerencia toda a lógica de automação e controle do bot
"""

import asyncio
import logging
import json
import os
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from dataclasses import asdict

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    TimeoutException, 
    NoSuchElementException, 
    WebDriverException
)
from webdriver_manager.chrome import ChromeDriverManager

from models import (
    BotConfig, 
    BotStatus, 
    BotStatusEnum,
    SessionStats, 
    BettingStrategy,
    ElementConfig,
    GameResult
)

logger = logging.getLogger(__name__)

class AviatorBotController:
    """Controlador principal do bot Aviator"""
    
    def __init__(self):
        self.config = BotConfig()
        self.elements = ElementConfig()
        self.driver: Optional[webdriver.Chrome] = None
        self.status = BotStatusEnum.STOPPED
        self.session_stats = SessionStats()
        self.betting_strategy: Optional[BettingStrategy] = None
        self.is_betting_active = False
        self.current_balance: Optional[float] = None
        self.recent_results: List[float] = []
        self.game_results: List[GameResult] = []
        self.error_message: Optional[str] = None
        self.credentials: Optional[Dict[str, str]] = None
        self._running = False
        self._stop_requested = False
        
        # Carregar configurações salvas
        self.load_config()
    
    def get_config(self) -> BotConfig:
        """Retorna a configuração atual"""
        return self.config
    
    def update_config(self, updates: Dict[str, Any]) -> BotConfig:
        """Atualiza a configuração"""
        for key, value in updates.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
        
        self.save_config()
        logger.info(f"Configuração atualizada: {updates}")
        return self.config
    
    def get_elements(self) -> ElementConfig:
        """Retorna a configuração de elementos"""
        return self.elements
    
    def update_elements(self, updates: Dict[str, Any]) -> ElementConfig:
        """Atualiza a configuração de elementos"""
        for key, value in updates.items():
            if hasattr(self.elements, key) and value:
                setattr(self.elements, key, value)
        
        self.save_config()
        logger.info(f"Elementos atualizados: {updates}")
        return self.elements
    
    def set_credentials(self, username: str, password: str) -> None:
        """Define as credenciais de login"""
        self.credentials = {"username": username, "password": password}
        logger.info("Credenciais definidas")
    
    def get_status(self) -> str:
        """Retorna o status atual como string"""
        return self.status.value
    
    def get_detailed_status(self) -> BotStatus:
        """Retorna status detalhado"""
        return BotStatus(
            status=self.status,
            is_running=self._running,
            is_betting=self.is_betting_active,
            current_balance=self.current_balance,
            last_multiplier=self.recent_results[0] if self.recent_results else None,
            last_update=datetime.now(),
            error_message=self.error_message,
            current_strategy=self.betting_strategy,
            recent_results=self.recent_results[:10]
        )
    
    def get_session_stats(self) -> SessionStats:
        """Retorna estatísticas da sessão"""
        if self.session_stats.start_time:
            uptime = datetime.now() - self.session_stats.start_time
            self.session_stats.uptime = str(uptime).split('.')[0]  # Remove microsegundos
        
        # Calcular multiplicador médio
        if self.recent_results:
            self.session_stats.avg_multiplier = sum(self.recent_results) / len(self.recent_results)
            self.session_stats.max_multiplier = max(self.recent_results)
        
        return self.session_stats
    
    def is_running(self) -> bool:
        """Verifica se o bot está em execução"""
        return self._running
    
    def start_betting(self, strategy: BettingStrategy) -> None:
        """Inicia apostas automáticas"""
        self.betting_strategy = strategy
        self.is_betting_active = True
        logger.info(f"Apostas automáticas iniciadas com estratégia: {strategy.strategy_type}")
    
    def stop_betting(self) -> None:
        """Para apostas automáticas"""
        self.is_betting_active = False
        self.betting_strategy = None
        logger.info("Apostas automáticas paradas")
    
    def setup_driver(self) -> None:
        """Configura e inicializa o driver do Chrome"""
        try:
            options = Options()
            
            # Configurações de performance e segurança
            chrome_options = [
                '--disable-logging',
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-extensions',
                '--disable-popup-blocking',
                '--disable-gpu',
                '--disable-infobars',
                '--disable-blink-features=AutomationControlled',
                '--disable-web-security',
                '--allow-running-insecure-content',
                '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            ]
            
            if self.config.headless:
                chrome_options.append('--headless')
            else:
                chrome_options.append('--start-maximized')
            
            for option in chrome_options:
                options.add_argument(option)
            
            # Configurações experimentais
            options.add_experimental_option('excludeSwitches', ['enable-automation'])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_experimental_option('w3c', True)
            
            # Inicializar driver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            
            # Executar script para evitar detecção
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            if not self.config.headless:
                self.driver.maximize_window()
            
            logger.info("Driver configurado com sucesso")
            
        except Exception as e:
            logger.error(f"Erro ao configurar driver: {e}")
            self.error_message = f"Erro ao configurar driver: {e}"
            self.status = BotStatusEnum.ERROR
            raise
    
    def wait_and_click(self, by: By, value: str, timeout: int = None) -> bool:
        """Aguarda elemento e clica com tratamento de erro"""
        timeout = timeout or self.config.wait_timeout
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            element.click()
            return True
        except TimeoutException:
            logger.error(f"Timeout ao aguardar elemento: {value}")
            return False
        except Exception as e:
            logger.error(f"Erro ao clicar no elemento {value}: {e}")
            return False
    
    def wait_and_send_keys(self, by: By, value: str, text: str, timeout: int = None) -> bool:
        """Aguarda elemento e envia texto com tratamento de erro"""
        timeout = timeout or self.config.wait_timeout
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            element.clear()
            element.send_keys(text)
            return True
        except TimeoutException:
            logger.error(f"Timeout ao aguardar elemento: {value}")
            return False
        except Exception as e:
            logger.error(f"Erro ao enviar texto para elemento {value}: {e}")
            return False
    
    async def login(self) -> bool:
        """Realiza login no site"""
        try:
            self.status = BotStatusEnum.STARTING
            logger.info("Iniciando processo de login")
            
            if not self.credentials:
                raise Exception("Credenciais não configuradas")
            
            # Navegar para o site
            self.driver.get(self.config.site_url)
            await asyncio.sleep(5)
            
            # Atualizar página
            logger.info("Atualizando página...")
            self.driver.refresh()
            await asyncio.sleep(5)
            
            # Aceitar cookies
            logger.info("Aguardando botão de cookies...")
            if self.wait_and_click(By.XPATH, self.elements.cookies_button):
                logger.info("Cookies aceitos")
                await asyncio.sleep(3)
            
            # Inserir credenciais
            logger.info("Inserindo usuário...")
            if not self.wait_and_send_keys(By.XPATH, self.elements.username_field, self.credentials["username"]):
                return False
            
            await asyncio.sleep(2)
            
            logger.info("Inserindo senha...")
            if not self.wait_and_send_keys(By.XPATH, self.elements.password_field, self.credentials["password"]):
                return False
            
            await asyncio.sleep(2)
            
            # Clicar no botão de login
            logger.info("Clicando no botão de login...")
            if not self.wait_and_click(By.XPATH, self.elements.login_button):
                return False
            
            await asyncio.sleep(5)
            self.status = BotStatusEnum.LOGGED_IN
            logger.info("Login realizado com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"Erro durante login: {e}")
            self.error_message = f"Erro durante login: {e}"
            self.status = BotStatusEnum.ERROR
            self.session_stats.errors += 1
            return False
    
    async def access_game(self) -> bool:
        """Acessa o jogo Aviator"""
        try:
            logger.info("Acessando jogo Aviator...")
            self.driver.get(self.config.game_url)
            
            # Aguardar iframe do jogo
            logger.info("Aguardando frame do jogo...")
            iframe = WebDriverWait(self.driver, self.config.wait_timeout).until(
                EC.presence_of_element_located((By.ID, self.elements.game_iframe))
            )
            
            # Mudar para o iframe
            self.driver.switch_to.frame(iframe)
            await asyncio.sleep(5)
            
            self.status = BotStatusEnum.IN_GAME
            logger.info("Jogo acessado com sucesso")
            return True
            
        except TimeoutException:
            logger.error("Timeout ao aguardar frame do jogo")
            self.error_message = "Timeout ao aguardar frame do jogo"
            self.status = BotStatusEnum.ERROR
            return False
        except Exception as e:
            logger.error(f"Erro ao acessar jogo: {e}")
            self.error_message = f"Erro ao acessar jogo: {e}"
            self.status = BotStatusEnum.ERROR
            self.session_stats.errors += 1
            return False
    
    def verify_strategy(self, results: List[float]) -> bool:
        """Verifica se a estratégia é válida baseada nos últimos resultados"""
        if len(results) < self.config.min_strategy_checks:
            return False
        
        # Estratégia: verificar se os últimos resultados são menores que o threshold
        recent_results = results[:self.config.min_strategy_checks]
        return all(result < self.config.strategy_threshold for result in recent_results)
    
    def get_game_results(self) -> Optional[List[float]]:
        """Obtém os resultados do histórico do jogo"""
        try:
            history_element = self.driver.find_element(By.CLASS_NAME, self.elements.result_history)
            history_text = history_element.text.replace('x', '').strip()
            
            if not history_text:
                return None
            
            results = [float(n) for n in history_text.split('\n') if n.strip()]
            return results[:self.config.history_size]
            
        except (NoSuchElementException, ValueError) as e:
            logger.warning(f"Erro ao obter resultados: {e}")
            return None
        except Exception as e:
            logger.error(f"Erro inesperado ao obter resultados: {e}")
            return None
    
    def get_current_balance(self) -> Optional[float]:
        """Obtém o saldo atual"""
        try:
            if self.elements.balance_display:
                balance_element = self.driver.find_element(By.XPATH, self.elements.balance_display)
                balance_text = balance_element.text.replace('R$', '').replace(',', '.').strip()
                return float(balance_text)
        except Exception as e:
            logger.warning(f"Erro ao obter saldo: {e}")
        return None
    
    async def place_bet(self, amount: float) -> bool:
        """Realiza uma aposta"""
        try:
            if not self.elements.bet_input or not self.elements.bet_button:
                logger.warning("Elementos de aposta não configurados")
                return False
            
            # Inserir valor da aposta
            if not self.wait_and_send_keys(By.XPATH, self.elements.bet_input, str(amount)):
                return False
            
            await asyncio.sleep(1)
            
            # Clicar no botão de apostar
            if not self.wait_and_click(By.XPATH, self.elements.bet_button):
                return False
            
            self.session_stats.bets_placed += 1
            self.session_stats.total_bet += amount
            logger.info(f"Aposta de R$ {amount} realizada")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao realizar aposta: {e}")
            return False
    
    async def cashout(self) -> bool:
        """Realiza cashout"""
        try:
            if not self.elements.cashout_button:
                logger.warning("Elemento de cashout não configurado")
                return False
            
            if self.wait_and_click(By.XPATH, self.elements.cashout_button):
                logger.info("Cashout realizado")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Erro ao realizar cashout: {e}")
            return False
    
    async def monitor_game(self) -> None:
        """Monitora o jogo e aplica estratégias"""
        logger.info("Iniciando monitoramento do jogo")
        self.status = BotStatusEnum.MONITORING
        
        while self._running and not self._stop_requested:
            try:
                # Obter resultados atuais
                current_results = self.get_game_results()
                
                if current_results is None:
                    logger.warning("Não foi possível obter resultados")
                    await asyncio.sleep(5)
                    continue
                
                # Verificar se houve mudança nos resultados
                if current_results != self.recent_results:
                    self.recent_results = current_results
                    self.session_stats.total_rounds += 1
                    
                    # Atualizar saldo
                    self.current_balance = self.get_current_balance()
                    
                    # Verificar estratégia
                    if self.verify_strategy(current_results):
                        self.session_stats.strategies_found += 1
                        logger.info(f"🎯 ESTRATÉGIA ENCONTRADA! Últimos resultados: {current_results[:4]}")
                        
                        # Se apostas automáticas estão ativas, realizar aposta
                        if self.is_betting_active and self.betting_strategy:
                            await self.execute_betting_strategy()
                    
                    else:
                        logger.info(f"📈 Resultados atuais: {current_results[:4]} (estratégia não ativada)")
                    
                    # Registrar resultado
                    game_result = GameResult(
                        multiplier=current_results[0],
                        strategy_triggered=self.verify_strategy(current_results)
                    )
                    self.game_results.append(game_result)
                    
                    # Manter apenas os últimos 100 resultados
                    if len(self.game_results) > 100:
                        self.game_results = self.game_results[-100:]
                
                await asyncio.sleep(self.config.update_interval)
                
            except Exception as e:
                logger.error(f"Erro durante monitoramento: {e}")
                self.session_stats.errors += 1
                await asyncio.sleep(5)
    
    async def execute_betting_strategy(self) -> None:
        """Executa a estratégia de aposta"""
        try:
            if not self.betting_strategy:
                return
            
            # Verificar limites de perda e ganho
            if self.betting_strategy.max_loss and self.session_stats.total_profit <= -self.betting_strategy.max_loss:
                if self.betting_strategy.stop_on_loss:
                    logger.info("Limite de perda atingido. Parando apostas.")
                    self.stop_betting()
                    return
            
            if self.betting_strategy.max_win and self.session_stats.total_profit >= self.betting_strategy.max_win:
                if self.betting_strategy.stop_on_win:
                    logger.info("Limite de ganho atingido. Parando apostas.")
                    self.stop_betting()
                    return
            
            # Calcular valor da aposta
            bet_amount = self.betting_strategy.amount
            
            # Aposta progressiva
            if self.betting_strategy.progressive_betting and self.session_stats.losses > 0:
                bet_amount *= (self.betting_strategy.progression_factor ** self.session_stats.losses)
            
            # Realizar aposta
            if await self.place_bet(bet_amount):
                self.status = BotStatusEnum.BETTING
                
                # Aguardar resultado da aposta
                # Aqui você implementaria a lógica para aguardar o resultado
                # e realizar cashout automático se configurado
                
                logger.info(f"Aposta executada: R$ {bet_amount}")
            
        except Exception as e:
            logger.error(f"Erro ao executar estratégia de aposta: {e}")
    
    async def start(self) -> None:
        """Inicia o bot"""
        try:
            if self._running:
                raise Exception("Bot já está em execução")
            
            self._running = True
            self._stop_requested = False
            self.session_stats = SessionStats()  # Reset stats
            self.error_message = None
            
            logger.info("🚀 Iniciando Bot Aviator")
            
            # Configurar driver
            self.setup_driver()
            
            # Fazer login
            if not await self.login():
                raise Exception("Falha no login")
            
            # Acessar jogo
            if not await self.access_game():
                raise Exception("Falha ao acessar jogo")
            
            # Monitorar jogo
            await self.monitor_game()
            
        except Exception as e:
            logger.error(f"Erro crítico: {e}")
            self.error_message = str(e)
            self.status = BotStatusEnum.ERROR
            self._running = False
            raise
    
    async def stop(self) -> None:
        """Para o bot"""
        try:
            logger.info("Parando bot...")
            self._stop_requested = True
            self.status = BotStatusEnum.STOPPING
            
            # Parar apostas se ativas
            if self.is_betting_active:
                self.stop_betting()
            
            # Aguardar um pouco para finalizar operações
            await asyncio.sleep(2)
            
            self._running = False
            self.status = BotStatusEnum.STOPPED
            logger.info("Bot parado com sucesso")
            
        except Exception as e:
            logger.error(f"Erro ao parar bot: {e}")
            self.error_message = f"Erro ao parar bot: {e}"
    
    async def cleanup(self) -> None:
        """Limpa recursos e fecha o driver"""
        try:
            if self.driver:
                self.driver.quit()
                logger.info("Driver fechado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao fechar driver: {e}")
    
    def save_config(self) -> None:
        """Salva configurações em arquivo"""
        try:
            config_data = {
                "config": self.config.dict(),
                "elements": self.elements.dict()
            }
            
            with open('bot_config.json', 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=4, ensure_ascii=False)
            
            logger.info("Configurações salvas")
        except Exception as e:
            logger.error(f"Erro ao salvar configurações: {e}")
    
    def load_config(self) -> None:
        """Carrega configurações de arquivo"""
        try:
            if os.path.exists('bot_config.json'):
                with open('bot_config.json', 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                
                if 'config' in config_data:
                    self.config = BotConfig(**config_data['config'])
                
                if 'elements' in config_data:
                    self.elements = ElementConfig(**config_data['elements'])
                
                logger.info("Configurações carregadas")
        except Exception as e:
            logger.warning(f"Erro ao carregar configurações: {e}")