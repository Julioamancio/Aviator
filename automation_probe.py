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
    driver.get('https://link.1-wins.br.com/')
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="signInDesktop-button"]'))).click()
    print('clicked desktop login')
    sleep(2)
    inputs = driver.find_elements(By.TAG_NAME, 'input')
    print('inputs available:', len(inputs))
    for inp in inputs:
        print('input -> name:', inp.get_attribute('name'), 'id:', inp.get_attribute('id'), 'type:', inp.get_attribute('type'), 'placeholder:', inp.get_attribute('placeholder'))
finally:
    driver.quit()
