from selenium import webdriver
from time import sleep

from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException

import os
from dotenv import load_dotenv
import time

load_dotenv()

chrome_options = Options()
chrome_options.add_argument("--disable-notifications")
chrome_options.add_experimental_option("detach", True)  # jätab akna lahti

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
driver.get("https://www.facebook.com/")

cookies = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.XPATH, '//button[@class="_42ft _4jy0 _9xo6 _4jy3 _4jy1 selected _51sy"]'))).click()

username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']")))
password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pass']")))

# textfieldidesse kasutaja ja parooli sisestamine
username.clear()
username.send_keys(os.environ.get("USER"))  # siia tuleb kasutajanimi/mail
password.clear()
password.send_keys(os.environ.get("PASS"))  # siia tuleb parool

# sisenemise nupu vajutamine
button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

time.sleep(5)

driver.get("https://www.facebook.com/events/birthdays")

if "Tänased sünnipäevad" not in driver.page_source:
    # täna pole kellelgi sünnipäev, sulgeb programmi
    exit()

# leiab üles div-id "Tänased sünnipäevad", "Hiljutised sõnnipäevad" ning "Tulevased sünnipäevad", siit peab eraldi üles otsima tänaste sünnipäevade div-i
containers = WebDriverWait(driver, 10).until(
    EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div[class='xyamay9 x1l90r2v']")))

if containers[0].find_element(By.TAG_NAME, "h2").find_element(By.TAG_NAME, "span").text != "Tänased sünnipäevad":
    # täna pole kellelgi sünnipäev, sulgeb programmi
    exit()

# TODO: containers[0] on tänaste sünnipäevade div, seal sees tuleb otsida üles kellele saata õnnitlus


# kirjutab kõikidesse input kastidesse "palju õnne"
# elements = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div[role='textbox']")))
# for element in elements:
#    element.clear()
#   element.send_keys("palju õnne")
