from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.add_argument('--disable-logging')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-extensions')
options.add_argument('--disable-popup-blocking')
options.add_argument('--disable-gpu')
options.add_argument('--disable-infobars')
options.add_argument('--disable-blink-features=AutomationControlled')
service = Service()
driver = webdriver.Chrome(service=service, options=options)
try:
    driver.get('https://estrelabet.com/ptb/bet/main')
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Aceitar')]"))).click()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Entrar')]"))).click()
    WebDriverWait(driver, 20).until(lambda d: 'login' in d.current_url.lower() or d.find_elements(By.CSS_SELECTOR, 'input'))
    Path('login_page.html').write_text(driver.page_source, encoding='utf-8')
finally:
    driver.quit()
