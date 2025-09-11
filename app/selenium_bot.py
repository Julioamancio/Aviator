from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional

from .config_manager import ConfigManager


ResultCallback = Callable[[Dict[str, Any]], None]
EmitCallback = Callable[[str], None]


def _parse_results(text: str) -> list[float]:
    try:
        arr = [s for s in text.replace("x", "").strip().splitlines() if s.strip()]
        return [float(x) for x in arr][:10]
    except Exception:
        return []


def _verificar_estrategia(lista: list[float]) -> bool:
    # True only if first 4 numbers are < 2
    for numero in lista[:4]:
        if numero >= 2:
            return False
    return True


def run_selenium_bot(
    cfg: ConfigManager,
    user_id: int,
    stop_event,
    emit: EmitCallback,
    set_result: ResultCallback,
) -> None:
    """Run the Selenium-based bot based on provided config and user settings.

    This function blocks until stop_event is set; it manages its own waits.
    """
    # Import selenium lazily to avoid hard dependency at import time
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
    except Exception as e:  # pragma: no cover
        emit(f"Selenium not available: {e}")
        return

    # Load config
    data = cfg.load()
    platform = data.get("platform", {})
    login_url: str = platform.get("login_url", "")
    game_url: str = platform.get("game_url", "")
    cookie_xpath: str = platform.get("cookie_button_xpath", "")
    iframe_id: str = platform.get("iframe_id", "gm-frm")
    results_sel: str = platform.get("results_selector", ".result-history")

    # Load user settings
    from .models import UserSetting
    from .extensions import db
    s: Optional[UserSetting] = UserSetting.query.filter_by(user_id=user_id).first()
    username = s.platform_username if s and s.platform_username else ""
    password = s.platform_password if s and s.platform_password else ""
    headless = bool(s.headless) if s else True

    if not username or not password:
        emit("Missing platform credentials in settings.")
        set_result({"error": "missing_credentials"})
        return

    # Configure Chrome
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument('--disable-logging')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--start-maximized")
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-popup-blocking')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option('w3c', True)

    driver = None
    try:
        # Use Selenium Manager (Selenium 4+) to handle driver
        driver = webdriver.Chrome(options=options)
        emit("Chrome driver started.")

        # Open and login
        driver.get(login_url)
        emit("Open login page.")
        time.sleep(3)
        try:
            driver.refresh()
        except Exception:
            pass

        if cookie_xpath:
            try:
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, cookie_xpath)))
                time.sleep(1)
                driver.find_element(By.XPATH, cookie_xpath).click()
                emit("Accepted cookies.")
                time.sleep(1)
            except Exception:
                emit("Cookie button not found; continuing.")

        # Default login xpaths; allow override in config in future if needed
        username_xpath = "//*[@id='username']"
        password_xpath = "//*[@id='password-login']"
        login_button_xpath = "//*[@id='header']/div/div[1]/div/div[2]/app-login/form/div/div/div[2]/button"

        try:
            driver.find_element(By.XPATH, username_xpath).send_keys(username)
            time.sleep(0.5)
            driver.find_element(By.XPATH, password_xpath).send_keys(password)
            time.sleep(0.5)
            driver.find_element(By.XPATH, login_button_xpath).click()
            emit("Submitted login form.")
        except Exception as e:
            emit(f"Login form interaction failed: {e}")
            set_result({"error": "login_failed"})
            return

        time.sleep(5)
        driver.get(game_url)
        emit("Navigated to game page.")

        try:
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, iframe_id)))
            time.sleep(1)
            iframe = driver.find_element(By.ID, iframe_id)
            driver.switch_to.frame(iframe)
            emit("Switched to game iframe.")
        except Exception as e:
            emit(f"Game iframe not available: {e}")
            set_result({"error": "iframe_missing"})
            return

        last_values: list[float] = []
        while not stop_event.is_set():
            try:
                elem = driver.find_element(By.CSS_SELECTOR, results_sel)
                values = _parse_results(elem.text)
                if values:
                    if values != last_values:
                        ok = _verificar_estrategia(values)
                        msg = f"estrategia {'ok' if ok else 'nok'} -> {values[:4]}"
                        emit(msg)
                        set_result({"estrategia_ok": ok, "ultimos": values[:10]})
                        last_values = values
                time.sleep(1.0)
            except Exception:
                time.sleep(1.0)
    finally:
        try:
            if driver:
                driver.quit()
                emit("Driver closed.")
        except Exception:
            pass

