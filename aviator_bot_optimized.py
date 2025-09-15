#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bot Aviator Otimizado - 2025
Script para automação e análise de padrões no jogo Aviator
Versão melhorada com tratamento de erros, logging e configurações seguras
"""

import os
import json
import logging
from datetime import datetime
from typing import List, Optional, Dict
from dataclasses import dataclass
from time import sleep

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

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('aviator_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class BotConfig:
    """Configurações do bot"""
    site_url: str = "https://estrelabet.com/ptb/bet/main"
    game_url: str = "https://estrelabet.com/ptb/games/detail/casino/normal/7787"
    username: str = ""
    password: str = ""
    headless: bool = False
    wait_timeout: int = 30
    strategy_threshold: float = 2.0
    history_size: int = 10
    min_strategy_checks: int = 4

class AviatorBot:
    """Bot principal para automação do jogo Aviator"""
    
    def __init__(self, config: BotConfig):
        self.config = config
        self.driver: Optional[webdriver.Chrome] = None
        self.results_history: List[float] = []
        self.session_stats = {
            'start_time': datetime.now(),
            'strategies_found': 0,
            'total_rounds': 0,
            'errors': 0
        }
    
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
            raise
    
    def load_credentials(self, file_path: str = 'credentials.json') -> None:
        """Carrega credenciais de arquivo JSON"""
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    creds = json.load(f)
                    self.config.username = creds.get('username', '')
                    self.config.password = creds.get('password', '')
                logger.info("Credenciais carregadas do arquivo")
            else:
                logger.warning(f"Arquivo de credenciais {file_path} não encontrado")
        except Exception as e:
            logger.error(f"Erro ao carregar credenciais: {e}")
    
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
    
    def login(self) -> bool:
        """Realiza login no site"""
        try:
            logger.info("Iniciando processo de login")
            
            # Navegar para o site
            self.driver.get(self.config.site_url)
            sleep(5)
            
            # Atualizar página
            logger.info("Atualizando página...")
            self.driver.refresh()
            sleep(5)
            
            # Aceitar cookies
            logger.info("Aguardando botão de cookies...")
            if self.wait_and_click(By.XPATH, '//*[@id="cookies-bottom-modal"]/div/div[1]/a'):
                logger.info("Cookies aceitos")
                sleep(3)
            
            # Inserir credenciais
            if not self.config.username or not self.config.password:
                logger.error("Credenciais não configuradas")
                return False
            
            logger.info("Inserindo usuário...")
            if not self.wait_and_send_keys(By.XPATH, '//*[@id="username"]', self.config.username):
                return False
            
            sleep(2)
            
            logger.info("Inserindo senha...")
            if not self.wait_and_send_keys(By.XPATH, '//*[@id="password-login"]', self.config.password):
                return False
            
            sleep(2)
            
            # Clicar no botão de login
            logger.info("Clicando no botão de login...")
            if not self.wait_and_click(By.XPATH, '//*[@id="header"]/div/div[1]/div/div[2]/app-login/form/div/div/div[2]/button'):
                return False
            
            sleep(5)
            logger.info("Login realizado com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"Erro durante login: {e}")
            self.session_stats['errors'] += 1
            return False
    
    def access_game(self) -> bool:
        """Acessa o jogo Aviator"""
        try:
            logger.info("Acessando jogo Aviator...")
            self.driver.get(self.config.game_url)
            
            # Aguardar iframe do jogo
            logger.info("Aguardando frame do jogo...")
            iframe = WebDriverWait(self.driver, self.config.wait_timeout).until(
                EC.presence_of_element_located((By.ID, 'gm-frm'))
            )
            
            # Mudar para o iframe
            self.driver.switch_to.frame(iframe)
            sleep(5)
            
            logger.info("Jogo acessado com sucesso")
            return True
            
        except TimeoutException:
            logger.error("Timeout ao aguardar frame do jogo")
            return False
        except Exception as e:
            logger.error(f"Erro ao acessar jogo: {e}")
            self.session_stats['errors'] += 1
            return False
    
    def verify_strategy(self, results: List[float]) -> bool:
        """Verifica se a estratégia é válida baseada nos últimos resultados"""
        if len(results) < self.config.min_strategy_checks:
            return False
        
        # Estratégia: verificar se os últimos 4 resultados são menores que o threshold
        recent_results = results[:self.config.min_strategy_checks]
        return all(result < self.config.strategy_threshold for result in recent_results)
    
    def get_game_results(self) -> Optional[List[float]]:
        """Obtém os resultados do histórico do jogo"""
        try:
            history_element = self.driver.find_element(By.CLASS_NAME, 'result-history')
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
    
    def monitor_game(self) -> None:
        """Monitora o jogo e aplica estratégias"""
        logger.info("Iniciando monitoramento do jogo")
        
        while True:
            try:
                # Obter resultados atuais
                current_results = self.get_game_results()
                
                if current_results is None:
                    logger.warning("Não foi possível obter resultados")
                    sleep(5)
                    continue
                
                # Verificar se houve mudança nos resultados
                if current_results != self.results_history:
                    self.results_history = current_results
                    self.session_stats['total_rounds'] += 1
                    
                    # Verificar estratégia
                    if self.verify_strategy(current_results):
                        self.session_stats['strategies_found'] += 1
                        logger.info(f"🎯 ESTRATÉGIA ENCONTRADA! Últimos resultados: {current_results[:4]}")
                        logger.info(f"📊 Histórico completo: {current_results}")
                        
                        # Aqui você pode adicionar lógica para apostar automaticamente
                        # CUIDADO: Apostas automáticas podem ser arriscadas!
                        
                    else:
                        logger.info(f"📈 Resultados atuais: {current_results[:4]} (estratégia não ativada)")
                    
                    # Log de estatísticas da sessão
                    if self.session_stats['total_rounds'] % 10 == 0:
                        self.log_session_stats()
                
                sleep(2)  # Intervalo entre verificações
                
            except KeyboardInterrupt:
                logger.info("Monitoramento interrompido pelo usuário")
                break
            except Exception as e:
                logger.error(f"Erro durante monitoramento: {e}")
                self.session_stats['errors'] += 1
                sleep(5)
    
    def log_session_stats(self) -> None:
        """Registra estatísticas da sessão"""
        duration = datetime.now() - self.session_stats['start_time']
        logger.info(f"📊 ESTATÍSTICAS DA SESSÃO:")
        logger.info(f"   ⏱️  Duração: {duration}")
        logger.info(f"   🎮 Rodadas monitoradas: {self.session_stats['total_rounds']}")
        logger.info(f"   🎯 Estratégias encontradas: {self.session_stats['strategies_found']}")
        logger.info(f"   ❌ Erros: {self.session_stats['errors']}")
        if self.session_stats['total_rounds'] > 0:
            success_rate = (self.session_stats['strategies_found'] / self.session_stats['total_rounds']) * 100
            logger.info(f"   📈 Taxa de sucesso: {success_rate:.2f}%")
    
    def cleanup(self) -> None:
        """Limpa recursos e fecha o driver"""
        try:
            if self.driver:
                self.driver.quit()
                logger.info("Driver fechado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao fechar driver: {e}")
    
    def run(self) -> None:
        """Executa o bot completo"""
        try:
            logger.info("🚀 Iniciando Bot Aviator Otimizado")
            
            # Carregar credenciais
            self.load_credentials()
            
            # Configurar driver
            self.setup_driver()
            
            # Fazer login
            if not self.login():
                logger.error("Falha no login. Encerrando bot.")
                return
            
            # Acessar jogo
            if not self.access_game():
                logger.error("Falha ao acessar jogo. Encerrando bot.")
                return
            
            # Monitorar jogo
            self.monitor_game()
            
        except Exception as e:
            logger.error(f"Erro crítico: {e}")
        finally:
            self.log_session_stats()
            self.cleanup()

def create_credentials_template():
    """Cria arquivo template para credenciais"""
    template = {
        "username": "seu_usuario_aqui",
        "password": "sua_senha_aqui"
    }
    
    with open('credentials.json', 'w') as f:
        json.dump(template, f, indent=4)
    
    logger.info("Arquivo credentials.json criado. Configure suas credenciais.")

if __name__ == "__main__":
    # Criar arquivo de credenciais se não existir
    if not os.path.exists('credentials.json'):
        create_credentials_template()
        print("⚠️  Configure suas credenciais no arquivo 'credentials.json' antes de executar o bot.")
        exit(1)
    
    # Configuração do bot
    config = BotConfig(
        headless=False,  # Mude para True para executar sem interface gráfica
        strategy_threshold=2.0,  # Ajuste conforme sua estratégia
        history_size=10,
        min_strategy_checks=4
    )
    
    # Executar bot
    bot = AviatorBot(config)
    bot.run()