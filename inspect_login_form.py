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
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Aceitar todos os cookies') or contains(., 'Aceitar')]"))).click()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Entrar')]"))).click()
    sleep(1)
    inputs = driver.find_elements(By.TAG_NAME, 'input')
    for inp in inputs:
        label = inp.get_attribute('aria-label')
        inp_id = inp.get_attribute('id')
        name = inp.get_attribute('name')
        placeholder = inp.get_attribute('placeholder')
        print('input', inp_id, name, placeholder, label)
finally:
    driver.quit()
