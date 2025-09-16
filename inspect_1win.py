from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
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
    driver.get('https://1-wins.br.com/')
    sleep(8)
    title = driver.title.encode('ascii', 'ignore').decode()
    print('title:', title)
    buttons = driver.find_elements(By.TAG_NAME, 'button')
    print('button count', len(buttons))
    for btn in buttons[:20]:
        txt = btn.text.strip()
        if txt:
            print('button:', txt.encode('ascii', 'ignore').decode())
finally:
    driver.quit()
