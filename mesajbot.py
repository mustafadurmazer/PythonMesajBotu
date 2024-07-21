import re
import requests
import schedule
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

Token = "6504896300:AAEdB7UNPIgU4JArWkLTHNa89OpAzQv4zmg"
ID = "1109232438"
api = "https://api.telegram.org/bot7276688490:AAFSIybrLG_w5QjJEqajwnPrnl-WAABNKBo/SendMessage"

def havadurumugetir():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    url = 'https://www.accuweather.com/tr/tr/konya/318795/daily-weather-forecast/318795'
    driver.get(url)

    try:
        enyuksek = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.high'))
        ).text

        endusuk = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.low'))
        ).text
        endusuk = re.sub(r'\s*/\s*', '', endusuk)

        tanım = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'phrase'))
        ).text
        return enyuksek, endusuk, tanım
    finally:
        driver.quit()

def kurbilgisi():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    url = 'https://bigpara.hurriyet.com.tr/altin/'
    driver.get(url)

    try:
        euro = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="piyasaBandiHisseler"]/div/ul/li[2]/a'))
        )
        dolar = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="piyasaBandiHisseler"]/div/ul/li[3]/a'))
        )
        altın = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="piyasaBandiHisseler"]/div/ul/li[4]/a'))
        )
        return euro.find_element(By.CLASS_NAME, 'value1').text, dolar.find_element(By.CLASS_NAME, 'value1').text, altın.find_element(By.CLASS_NAME, 'value1').text
    finally:
        driver.quit()

def gönder():
    enyuksek, endusuk, tanım = havadurumugetir()
    euro, dolar, altın = kurbilgisi()

    mesaj = f"Hava Durumu:\nMax/Min: {enyuksek} / {endusuk}\n{tanım}\nKur Bilgisi:\nDolar: {dolar}\nEuro: {euro}\nAltın: {altın}"
    
    requests.post(url=api, data={"chat_id": ID, "text": mesaj}).json()
schedule.every().day.at("20:29").do(gönder)

while True:
    time.sleep(60) 
    schedule.run_pending()
