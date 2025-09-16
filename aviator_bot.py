"""
Monitoramento do jogo Aviator na 1win usando Selenium.
Fluxo baseado em login manual: o usuário realiza o login e o script
apenas monitora o histórico de resultados.
"""

import json
from pathlib import Path
from time import sleep
from typing import Iterable, List, Optional

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException, WebDriverException

FORCE_MANUAL_LOGIN = True
CREDENTIALS_FILE = Path("credentials.json")
USB_CREDENTIALS_FILE = Path(r"F:/AVIATOR/credentials.json")
CREDENTIAL_PATHS = (CREDENTIALS_FILE, USB_CREDENTIALS_FILE)
SITE_URL = "https://1-wins.br.com/"
SITE_URL_FALLBACK = "https://1whfxh.life/"
GAME_URLS = [
    "https://1whfxh.life/casino/play/spribe_aviator",
    "https://1-wins.br.com/casino/game/aviator",
]
TARGET_URL_KEYWORDS = ["spribe_aviator", "casino/play"]
LOGIN_BUTTON_XPATH = "//a[contains(@class,'log') and contains(@class,'open-popup')]"
IFRAME_XPATH = "//*[@id='root']/div[2]/div/div/div[2]/div/div[2]/div/div/section/div/iframe"
PAYOUT_CONTAINER_XPATH = "/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[1]/app-stats-widget/div/div[1]/div"
BET_CONTROLS_XPATH = "/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls"
WAIT_TIMEOUT = 30
STRATEGY_THRESHOLD = 2.0
MIN_STRATEGY_CHECKS = 4
HISTORY_SIZE = 10


def load_credentials(paths: Iterable[Path] = CREDENTIAL_PATHS) -> dict:
    for candidate in paths:
        if candidate.exists():
            try:
                data = json.loads(candidate.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                raise RuntimeError(f"Arquivo {candidate} invalido: {exc}") from exc

            if not data.get("username") or not data.get("password"):
                raise RuntimeError(
                    f"Credenciais ausentes no arquivo {candidate}. Atualize username e password."
                )
            return data

    template = {"username": "seu_usuario_aqui", "password": "sua_senha_aqui"}
    CREDENTIALS_FILE.write_text(json.dumps(template, indent=4), encoding="utf-8")
    raise RuntimeError(
        "Nenhum credentials.json encontrado. Um modelo foi criado na pasta atual."
    )


def create_driver(headless: bool = False) -> webdriver.Chrome:
    options = Options()
    options.add_argument("--disable-logging")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("w3c", True)

    if headless:
        options.add_argument("--headless=new")
    else:
        options.add_argument("--start-maximized")

    service = Service()
    return webdriver.Chrome(service=service, options=options)


def verificar_estrategia(resultados: List[float]) -> bool:
    if len(resultados) < MIN_STRATEGY_CHECKS:
        return False
    recentes = resultados[:MIN_STRATEGY_CHECKS]
    return all(valor < STRATEGY_THRESHOLD for valor in recentes)


def aceitar_cookies(driver: webdriver.Chrome) -> None:
    seletores = [
        (By.XPATH, "//button[contains(., 'Aceitar')]")
    ]
    for by, value in seletores:
        try:
            botao = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((by, value)))
            botao.click()
            print("Cookies aceitos")
            return
        except Exception:
            continue
    print("Nenhum banner de cookies para fechar")


def abrir_modal_login(driver: webdriver.Chrome) -> None:
    try:
        botao_login = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, LOGIN_BUTTON_XPATH))
        )
        botao_login.click()
    except Exception:
        print("Nao foi possivel clicar no botao de login automaticamente. Abra manualmente se necessario.")


def fazer_login(driver: webdriver.Chrome, credenciais: Optional[dict]) -> None:
    for url in (SITE_URL, SITE_URL_FALLBACK):
        print(f"Abrindo site inicial: {url}")
        driver.get(url)
        sleep(5)
        try:
            driver.refresh()
            sleep(5)
            break
        except WebDriverException:
            continue

    aceitar_cookies(driver)
    abrir_modal_login(driver)

    if FORCE_MANUAL_LOGIN or not credenciais:
        print("Modo de login manual ativo. Realize o login na janela aberta.")
        try:
            input("Apos concluir o login manualmente, pressione Enter aqui para continuar...")
        except EOFError:
            print("Entrada de teclado indisponivel. Aguardando 5 segundos antes de continuar...")
            sleep(5)
        print("Login manual confirmado. Prosseguindo...")
        sleep(3)
        return

    raise RuntimeError("Login automatico nao implementado para 1win. Use o modo manual.")


def garantir_aba_jogo(driver: webdriver.Chrome) -> None:
    handles = driver.window_handles
    if not handles:
        raise RuntimeError("Nenhuma aba ativa encontrada")

    for handle in reversed(handles):
        driver.switch_to.window(handle)
        sleep(1)
        try:
            url = driver.current_url.lower()
        except WebDriverException:
            continue
        if any(keyword in url for keyword in TARGET_URL_KEYWORDS):
            return
    driver.switch_to.window(handles[-1])


def corpo_jogo_ativo(driver: webdriver.Chrome) -> bool:
    try:
        driver.find_element(By.XPATH, IFRAME_XPATH)
        return True
    except Exception:
        return False


def acessar_jogo(driver: webdriver.Chrome) -> None:
    garantir_aba_jogo(driver)

    if corpo_jogo_ativo(driver):
        print("Jogo ja esta aberto. Usando iframe atual.")
    else:
        last_exception: Optional[Exception] = None
        for url in GAME_URLS:
            print(f"Carregando jogo em {url}...")
            try:
                driver.get(url)
                sleep(5)
                garantir_aba_jogo(driver)
                if corpo_jogo_ativo(driver):
                    break
            except Exception as exc:
                print(f"Falha ao carregar {url}: {exc}")
                last_exception = exc
                continue
        else:
            raise RuntimeError("Nao foi possivel carregar o jogo em nenhum dos URLs conhecidos") from last_exception

    for attempt in range(3):
        try:
            iframe = WebDriverWait(driver, WAIT_TIMEOUT).until(
                EC.presence_of_element_located((By.XPATH, IFRAME_XPATH))
            )
            driver.switch_to.frame(iframe)
            break
        except StaleElementReferenceException:
            if attempt == 2:
                raise
            sleep(1)
            garantir_aba_jogo(driver)
    WebDriverWait(driver, WAIT_TIMEOUT).until(
        EC.presence_of_element_located((By.XPATH, PAYOUT_CONTAINER_XPATH))
    )
    print("Iframe do jogo ativo")
    sleep(2)


def obter_resultados(driver: webdriver.Chrome) -> List[float]:
    try:
        elemento = driver.find_element(By.XPATH, PAYOUT_CONTAINER_XPATH)
    except Exception:
        return []

    texto = elemento.text.strip()
    if not texto:
        return []

    valores: List[float] = []
    for entrada in texto.replace("x", " ").split():
        entrada = entrada.strip().replace(",", ".")
        if not entrada:
            continue
        try:
            valores.append(float(entrada))
        except ValueError:
            continue
    return valores[:HISTORY_SIZE]


def monitorar(driver: webdriver.Chrome) -> None:
    historico_atual: List[float] = []
    while True:
        resultados = obter_resultados(driver)
        if not resultados:
            sleep(5)
            continue
        if resultados != historico_atual:
            historico_atual = resultados
            print(f"Resultados: {historico_atual}")
            if verificar_estrategia(historico_atual):
                print(f"Estrategia identificada: {historico_atual[:MIN_STRATEGY_CHECKS]}")
        sleep(2)


def main() -> None:
    credenciais: Optional[dict] = None
    try:
        credenciais = load_credentials()
    except RuntimeError as erro:
        print(f"Aviso: {erro}")
        print("Prosseguindo em modo de login manual.")

    if FORCE_MANUAL_LOGIN:
        credenciais = None

    driver = create_driver()
    try:
        fazer_login(driver, credenciais)
        garantir_aba_jogo(driver)
        acessar_jogo(driver)
        monitorar(driver)
    finally:
        driver.quit()


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as erro:
        print(f"Erro: {erro}")
