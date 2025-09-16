from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

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
    print('url initial', driver.current_url)
    try:
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Aceitar')]"))).click()
        print('clicked cookies')
    except Exception as exc:
        print('no cookie button', exc)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Entrar')]"))).click()
    print('clicked entrar')
    sleep(3)
    print('after click url', driver.current_url)
    inputs = driver.find_elements(By.TAG_NAME, 'input')
    print('inputs count', len(inputs))
    for inp in inputs:
        print('input info', inp.get_attribute('id'), inp.get_attribute('name'), inp.get_attribute('type'), inp.get_attribute('aria-label'), inp.get_attribute('placeholder'))
finally:
    driver.quit()
