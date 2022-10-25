import os
import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def ava_brauser():
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_experimental_option("detach", True)  # jätab akna lahti

    return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)


def logi_sisse(browser_driver):
    browser_driver.get("https://www.facebook.com/")
    WebDriverWait(browser_driver, 30).until(EC.element_to_be_clickable(
        (By.XPATH, '//button[@class="_42ft _4jy0 _9xo6 _4jy3 _4jy1 selected _51sy"]'))).click()

    username = WebDriverWait(browser_driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']")))
    password = WebDriverWait(browser_driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pass']")))

    # textfieldidesse kasutaja ja parooli sisestamine
    username.clear()
    username.send_keys(os.environ.get("USER"))  # siia tuleb kasutajanimi/mail
    password.clear()
    password.send_keys(os.environ.get("PASS"))  # siia tuleb parool

    # sisenemise nupu vajutamine
    WebDriverWait(browser_driver, 2).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

    WebDriverWait(browser_driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[aria-label='Facebook']")))


def soovi_õnne(browser_driver, whitelist):
    browser_driver.get("https://www.facebook.com/events/birthdays")

    # leiab üles div-id "Tänased sünnipäevad", "Hiljutised sõnnipäevad" ning "Tulevased sünnipäevad"
    # siit peab eraldi üles otsima tänaste sünnipäevade div-i
    containers = WebDriverWait(browser_driver, 10).until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div[class='xyamay9 x1l90r2v']")))

    if len(containers) == 0 or containers[0].find_element(By.TAG_NAME, "h2").find_element(By.TAG_NAME,
                                                                                          "span").text != "Tänased sünnipäevad":  # TODO: teised keeled
        # täna pole kellelgi sünnipäev, sulgeb programmi
        exit()

    # kõik inimesed, kellel on täna sünnipäev
    inimesed = containers[0].find_elements(By.CSS_SELECTOR, "div[class='x78zum5 xz9dl7a x4uap5 xwib8y2 xkhd6sd']")

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


def get_friends_list(browser_driver):
    return browser_driver.find_elements(By.CSS_SELECTOR,
                                        "a[class='x1i10hfl x1qjc9v5 xjbqb8w xjqpnuy xa49m3k xqeqjp1 x2hbi6w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x16tdsg8 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x87ps6o x1lku1pv x1a2a7pz x1lq5wgf xgqcy7u x30kzoy x9jhf4c x1lliihq']")


def sõbrad(browser_driver):
    browser_driver.get("https://www.facebook.com/friends/list")
    WebDriverWait(browser_driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[aria-label='Facebook']")))

    num_of_loaded_friends = len(get_friends_list(browser_driver))

    while True:
        # vajutab sõprade listi scrollbari peale ja siis vajutab end klahvi kuni jõuab listi lõppu
        browser_driver.find_element(By.CSS_SELECTOR,
                                    "div[class='x14nfmen x1s85apg xds687c x5yr21d xg01cxk x10l6tqk x13vifvy x1wsgiic x19991ni xwji4o3 x1kky2od x1sd63oq']").click()
        ActionChains(browser_driver) \
            .key_down(Keys.END) \
            .key_up(Keys.END) \
            .perform()

        try:
            WebDriverWait(browser_driver, 5).until(
                lambda browser_driver: len(get_friends_list(browser_driver)) > num_of_loaded_friends)
            num_of_loaded_friends = len(get_friends_list(browser_driver))
        except TimeoutException:
            # siseneb siia excepti kui on kerinud sõprade listi lõppu ja viie sekundi jooksul ei lae uusi sõpru juurde

            time.sleep(1)

            konteinerid = get_friends_list(browser_driver)

            sõprade_list = []

            for element in konteinerid:
                pilt = element.find_element(By.TAG_NAME, "image").get_property("href").get("animVal")
                nimi = element.find_element(By.CSS_SELECTOR, "span[class='x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x6prxxf xvq8zen x1s688f xzsf02u']").text
                sõprade_list.append((pilt, nimi))

            print(sõprade_list[0])
            return sõprade_list  # no more friends loaded

            # returnib listi, mis koosneb tuple'itest kujul (pilt, nimi)


load_dotenv()
driver = ava_brauser()
logi_sisse(driver)
sõbrad(driver)
