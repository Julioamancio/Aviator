#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bot Aviator Otimizado para 1win (2025)
Fluxo: login manual, acesso ao Aviator e monitoramento das velas.
"""

import os
import json
import logging
from datetime import datetime
from typing import List, Optional, Dict
from dataclasses import dataclass
from time import sleep
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    WebDriverException,
    StaleElementReferenceException
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('aviator_bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

FORCE_MANUAL_LOGIN = True
CREDENTIAL_PATHS = (
    Path("credentials.json"),
    Path(r"F:/AVIATOR/credentials.json"),
)
SITE_URL = "https://1-wins.br.com/"
SITE_URL_FALLBACK = "https://1whfxh.life/"
GAME_URL_PRIMARY = "https://1whfxh.life/casino/play/spribe_aviator"
GAME_URL_FALLBACKS = [
    "https://1-wins.br.com/casino/game/aviator",
]
TARGET_URL_KEYWORDS = ["spribe_aviator", "casino/play"]
LOGIN_BUTTON_XPATH = "//a[contains(@class,'log') and contains(@class,'open-popup')]"
IFRAME_XPATH = "//*[@id='root']/div[2]/div/div/div[2]/div/div[2]/div/div/section/div/iframe"
PAYOUT_CONTAINER_XPATH = "/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[1]/app-stats-widget/div/div[1]/div"
BET_CONTROLS_XPATH = "/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls"

@dataclass
class BotConfig:
    site_url: str = SITE_URL
    game_url: str = GAME_URL_PRIMARY
    username: str = ""
    password: str = ""
    headless: bool = False
    wait_timeout: int = 30
    strategy_threshold: float = 2.0
    history_size: int = 10
    min_strategy_checks: int = 4
    manual_login: bool = FORCE_MANUAL_LOGIN

class AviatorBot:
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
        try:
            options = Options()
            chrome_options = [
                '--disable-logging',
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-extensions',
                '--disable-popup-blocking',
                '--disable-gpu',
                '--disable-infobars',
                '--disable-blink-features=AutomationControlled',
                '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            ]

            if self.config.headless:
                chrome_options.append('--headless')
            else:
                chrome_options.append('--start-maximized')

            for option in chrome_options:
                options.add_argument(option)

            options.add_experimental_option('excludeSwitches', ['enable-automation'])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_experimental_option('w3c', True)

            service = Service()
            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

            if not self.config.headless:
                self.driver.maximize_window()

            logger.info("Driver configurado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao configurar driver: {e}")
            raise

    def load_credentials(self, file_path: str = 'credentials.json') -> None:
        try:
            candidate_paths = []
            default_path = Path(file_path)
            candidate_paths.append(default_path)
            for extra in CREDENTIAL_PATHS:
                if extra not in candidate_paths:
                    candidate_paths.append(extra)

            for candidate in candidate_paths:
                if candidate.exists():
                    with open(candidate, 'r', encoding='utf-8') as f:
                        creds = json.load(f)
                        self.config.username = creds.get('username', '')
                        self.config.password = creds.get('password', '')
                    self.config.manual_login = FORCE_MANUAL_LOGIN
                    logger.info(f"Credenciais carregadas do arquivo {candidate}")
                    return

            self.config.manual_login = True
            logger.warning(f"Arquivo de credenciais nao encontrado nas localizacoes: {[str(p) for p in candidate_paths]}")
        except Exception as e:
            logger.error(f"Erro ao carregar credenciais: {e}")
            self.config.manual_login = True

    def wait_and_click(self, by: By, value: str, timeout: int = None) -> bool:
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

    def wait_for_manual_login(self) -> None:
        logger.info("Aguardando login manual no navegador.")
        try:
            input("Pressione Enter aqui apos concluir o login manual...")
        except EOFError:
            logger.warning("Entrada de teclado indisponivel. Aguardando 5 segundos antes de continuar...")
            sleep(5)
        except KeyboardInterrupt:
            raise
        logger.info("Login manual confirmado pelo usuario. Prosseguindo...")
        sleep(3)

    def handle_cookies(self) -> None:
        if self.wait_and_click(By.XPATH, "//button[contains(., 'Aceitar')]", timeout=5):
            logger.info("Cookies aceitos")
        else:
            logger.info("Nenhum banner de cookies para fechar")

    def open_login_modal(self) -> None:
        if not self.wait_and_click(By.XPATH, LOGIN_BUTTON_XPATH, timeout=10):
            logger.info("Nao foi possivel abrir o modal de login automaticamente.")

    def ensure_latest_window(self) -> None:
        handles = self.driver.window_handles
        if not handles:
            raise RuntimeError("Nenhuma aba ativa encontrada")
        for handle in reversed(handles):
            self.driver.switch_to.window(handle)
            sleep(1)
            try:
                current_url = self.driver.current_url.lower()
            except WebDriverException:
                continue
            if any(keyword in current_url for keyword in TARGET_URL_KEYWORDS):
                return
        self.driver.switch_to.window(handles[-1])

    def login(self) -> bool:
        try:
            logger.info("Iniciando processo de login")

            for url in (self.config.site_url, SITE_URL_FALLBACK):
                logger.info(f"Abrindo site inicial: {url}")
                try:
                    self.driver.get(url)
                    sleep(5)
                    self.driver.refresh()
                    sleep(5)
                    break
                except WebDriverException as exc:
                    logger.warning(f"Falha ao abrir {url}: {exc}")
                    continue

            self.handle_cookies()
            self.open_login_modal()

            if self.config.manual_login or not self.config.username or not self.config.password:
                logger.warning("Credenciais nao configuradas ou login manual ativado.")
                self.wait_for_manual_login()
                return True

            logger.error("Login automatico nao implementado para 1win. Ative manual_login.")
            return False

        except Exception as e:
            logger.error(f"Erro durante login: {e}")
            self.session_stats['errors'] += 1
            return False

    def access_game(self) -> bool:
        urls_to_try = [self.config.game_url] + [u for u in GAME_URL_FALLBACKS if u != self.config.game_url]
        last_exception: Optional[Exception] = None

        self.ensure_latest_window()
        if self._game_iframe_present():
            logger.info("Jogo ja esta aberto na aba atual.")
        else:
            for url in urls_to_try:
                try:
                    logger.info(f"Carregando jogo em {url}...")
                    self.driver.get(url)
                    sleep(5)
                    self.ensure_latest_window()
                    if self._game_iframe_present():
                        break
                except Exception as exc:
                    logger.error(f"Falha ao carregar {url}: {exc}")
                    last_exception = exc
                    continue
            else:
                logger.error("Nao foi possivel carregar o jogo em nenhum dos URLs conhecidos")
                if last_exception:
                    raise last_exception
                return False

        for attempt in range(3):
            try:
                iframe = WebDriverWait(self.driver, self.config.wait_timeout).until(
                    EC.presence_of_element_located((By.XPATH, IFRAME_XPATH))
                )
                self.driver.switch_to.frame(iframe)
                break
            except StaleElementReferenceException:
                if attempt == 2:
                    raise
                sleep(1)
                self.ensure_latest_window()

        WebDriverWait(self.driver, self.config.wait_timeout).until(
            EC.presence_of_element_located((By.XPATH, PAYOUT_CONTAINER_XPATH))
        )
        logger.info("Jogo acessado com sucesso")
        sleep(2)
        return True

    def _game_iframe_present(self) -> bool:
        try:
            self.ensure_latest_window()
            self.driver.find_element(By.XPATH, IFRAME_XPATH)
            return True
        except Exception:
            return False

    def verify_strategy(self, results: List[float]) -> bool:
        if len(results) < self.config.min_strategy_checks:
            return False
        recent_results = results[:self.config.min_strategy_checks]
        return all(result < self.config.strategy_threshold for result in recent_results)

    def get_game_results(self) -> Optional[List[float]]:
        try:
            history_element = self.driver.find_element(By.XPATH, PAYOUT_CONTAINER_XPATH)
            history_text = history_element.text.strip()
            if not history_text:
                return None

            results: List[float] = []
            for chunk in history_text.replace("x", " ").split():
                chunk = chunk.strip().replace(",", ".")
                if not chunk:
                    continue
                try:
                    results.append(float(chunk))
                except ValueError:
                    continue
            return results[:self.config.history_size]

        except (NoSuchElementException, ValueError) as e:
            logger.warning(f"Erro ao obter resultados: {e}")
            return None
        except Exception as e:
            logger.error(f"Erro inesperado ao obter resultados: {e}")
            return None

    def monitor_game(self) -> None:
        logger.info("Iniciando monitoramento do jogo")

        while True:
            try:
                current_results = self.get_game_results()

                if current_results is None:
                    logger.warning("Nao foi possivel obter resultados")
                    sleep(5)
                    continue

                if current_results != self.results_history:
                    self.results_history = current_results
                    self.session_stats['total_rounds'] += 1

                    if self.verify_strategy(current_results):
                        self.session_stats['strategies_found'] += 1
                        logger.info(f"[ESTRATEGIA] Ultimos resultados: {current_results[:4]}")
                        logger.info(f"[HISTORICO] {current_results}")
                    else:
                        logger.info(f"[INFO] Resultados atuais: {current_results[:4]} (estrategia nao ativada)")

                    if self.session_stats['total_rounds'] % 10 == 0:
                        self.log_session_stats()

                sleep(2)

            except KeyboardInterrupt:
                logger.info("Monitoramento interrompido pelo usuario")
                break
            except Exception as e:
                logger.error(f"Erro durante monitoramento: {e}")
                self.session_stats['errors'] += 1
                sleep(5)

    def log_session_stats(self) -> None:
        duration = datetime.now() - self.session_stats['start_time']
        logger.info("[STATS] ESTATISTICAS DA SESSAO:")
        logger.info(f"   Duracao: {duration}")
        logger.info(f"   Rodadas monitoradas: {self.session_stats['total_rounds']}")
        logger.info(f"   Estrategias encontradas: {self.session_stats['strategies_found']}")
        logger.info(f"   Erros: {self.session_stats['errors']}")
        if self.session_stats['total_rounds'] > 0:
            success_rate = (self.session_stats['strategies_found'] / self.session_stats['total_rounds']) * 100
            logger.info(f"   Taxa de sucesso: {success_rate:.2f}%")

    def cleanup(self) -> None:
        try:
            if self.driver:
                self.driver.quit()
                logger.info("Driver fechado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao fechar driver: {e}")

    def run(self) -> None:
        try:
            logger.info("Iniciando Bot Aviator Otimizado")

            self.load_credentials()
            self.setup_driver()

            if not self.login():
                logger.error("Falha no login. Encerrando bot.")
                return

            if not self.access_game():
                logger.error("Falha ao acessar jogo. Encerrando bot.")
                return

            self.monitor_game()

        except Exception as e:
            logger.error(f"Erro critico: {e}")
        finally:
            self.log_session_stats()
            self.cleanup()

def create_credentials_template():
    template = {
        "username": "seu_usuario_aqui",
        "password": "sua_senha_aqui"
    }

    with open('credentials.json', 'w', encoding='utf-8') as f:
        json.dump(template, f, indent=4)

    logger.info("Arquivo credentials.json criado. Configure suas credenciais.")

if __name__ == "__main__":
    if not any(path.exists() for path in CREDENTIAL_PATHS):
        create_credentials_template()
        print("ATENCAO: Configure suas credenciais no arquivo 'credentials.json' para login automatico.")
        print("Se preferir, realize o login manualmente quando o navegador abrir.")

    config = BotConfig(
        headless=False,
        strategy_threshold=2.0,
        history_size=10,
        min_strategy_checks=4,
        manual_login=FORCE_MANUAL_LOGIN
    )

    bot = AviatorBot(config)
    bot.run()
