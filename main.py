import os
import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

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

# leiab üles div-id "Tänased sünnipäevad", "Hiljutised sõnnipäevad" ning "Tulevased sünnipäevad"
# siit peab eraldi üles otsima tänaste sünnipäevade div-i
containers = WebDriverWait(driver, 10).until(
    EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div[class='xyamay9 x1l90r2v']")))

if len(containers) == 0 or containers[0].find_element(By.TAG_NAME, "h2").find_element(By.TAG_NAME, "span").text != "Tänased sünnipäevad":  # TODO: teised keeled
    # täna pole kellelgi sünnipäev, sulgeb programmi
    exit()

# kõik inimesed, kellel on täna sünnipäev
inimesed = containers[0].find_elements(By.CSS_SELECTOR, "div[class='x78zum5 xz9dl7a x4uap5 xwib8y2 xkhd6sd']")

whitelist = [] # siia tuleb lugeda sealt UI-st need nimed kellele saata

for inimene in inimesed:
    if inimene.find_element(By.TAG_NAME, "h2").find_element(By.TAG_NAME, "span").text in whitelist:
        # inimesel on täna sünnipäev ning ta on meie õnnesoovimise whitelistis
        try:
            # soovib õnne, kui inimesele pole veel õnne soovitud ehk kui textbox on nähtav
            textbox = inimene.find_element(By.CSS_SELECTOR, "div[role='textbox']")
            textbox.clear()
            textbox.send_keys("palju õnne")  # siia peab panema custom õnnesoovi
        except NoSuchElementException:
            print("ei saanud õnne soovida")
