import os
import time
from pathlib import Path

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
    #chrome_options.add_argument("--headless")  # avab akna nähtamatult
    #chrome_options.add_experimental_option("detach", True)  # jätab akna lahti

    return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)


def loe_andmed():
    f = open("andmed.txt", "r")
    ls = []
    for i in f:
        ls += [i.strip()]

    return ls


def logi_sisse(browser_driver, ls):
    load_dotenv()
    browser_driver.get("https://www.facebook.com/")
    WebDriverWait(browser_driver, 30).until(EC.element_to_be_clickable(
        (By.XPATH, '//button[@class="_42ft _4jy0 _9xo6 _4jy3 _4jy1 selected _51sy"]'))).click()

    username = WebDriverWait(browser_driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']")))
    password = WebDriverWait(browser_driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pass']")))

    # textfieldidesse kasutaja ja parooli sisestamine
    username.clear()
    username.send_keys(ls[0])  # siia tuleb kasutajanimi/mail
    password.clear()
    password.send_keys(ls[1])  # siia tuleb parool

    # sisenemise nupu vajutamine
    WebDriverWait(browser_driver, 2).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

    WebDriverWait(browser_driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[aria-label='Facebook']")))


def soovi_õnne(browser_driver):

    whitelist = []
    with open("friend_list.txt", "r", encoding="UTF-8") as f:
        lines = f.readlines()
    non_empty_lines = []
    for line in lines:
        if line.strip():
            non_empty_lines.append(line)

    for line in non_empty_lines:
        line_as_list = line.strip().split(';')
        if line_as_list[2] == "True":
            whitelist.append({"name": line_as_list[0], "custom_wish": line_as_list[1]})

    browser_driver.get("https://www.facebook.com/events/birthdays")

    # leiab üles div-id "Tänased sünnipäevad", "Hiljutised sõnnipäevad" ning "Tulevased sünnipäevad"
    # siit peab eraldi üles otsima tänaste sünnipäevade div-i
    containers = WebDriverWait(browser_driver, 10).until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div[class='x1l90r2v xyamay9']")))

    time.sleep(1)

    if len(containers) == 0 or containers[0].find_element(By.TAG_NAME, "h2").find_element(By.TAG_NAME,
                                                                                          "span").text != "Tänased sünnipäevad":  # TODO: teised keeled
        # täna pole kellelgi sünnipäev, sulgeb programmi
        exit()

    # kõik inimesed, kellel on täna sünnipäev
    inimesed = containers[0].find_elements(By.CSS_SELECTOR, "div[class='x78zum5  xz9dl7a x4uap5 xwib8y2 xkhd6sd']")

    for inimene in inimesed:
        for item in whitelist:
            if inimene.find_element(By.TAG_NAME, "h2").find_element(By.TAG_NAME, "span").text == item.get("name"):
                # inimesel on täna sünnipäev ning ta on meie õnnesoovimise whitelistis
                try:
                    # soovib õnne, kui inimesele pole veel õnne soovitud ehk kui textbox on nähtav
                    textbox = inimene.find_element(By.CSS_SELECTOR, "div[role='textbox']")
                    textbox.clear()
                    if item.get("custom_wish").strip():
                        textbox.send_keys(item.get("custom_wish"))
                    else:
                        textbox.send_keys("Palju õnne!")
                    textbox.send_keys(Keys.ENTER)
                except NoSuchElementException:
                    print("ei saanud õnne soovida")


def get_friends_list(browser_driver):
    return browser_driver.find_elements(By.CSS_SELECTOR,
                                        "a[class='x1i10hfl x1qjc9v5 xjbqb8w xjqpnuy xa49m3k xqeqjp1 x2hbi6w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x16tdsg8 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x87ps6o x1lku1pv x1a2a7pz x1lq5wgf xgqcy7u x30kzoy x9jhf4c x1lliihq']")


def sõbrad(browser_driver):
    browser_driver.get("https://www.facebook.com/friends/list")
    WebDriverWait(browser_driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[aria-label='Facebook']")))

    num_of_loaded_friends = len(get_friends_list(browser_driver))

    time.sleep(3)

    browser_driver.find_element(By.CSS_SELECTOR,
                                "label[class='x1a2a7pz x1qjc9v5 xnwf7zb x40j3uw x1s7lred x15gyhx8 x9f619 x78zum5 x1fns5xo x1n2onr6 xh8yej3 xu0aao5 xmjcpbm']").click()

    while True:
        # vajutab sõprade listi scrollbari peale ja siis vajutab end klahvi kuni jõuab listi lõppu
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
                try:
                    pilt = element.find_element(By.TAG_NAME, "image").get_property("href").get("animVal")
                    nimi = element.find_element(By.CSS_SELECTOR,
                                                "span[class='x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x6prxxf xvq8zen x1s688f xzsf02u']").text

                    sõprade_list.append(
                        {
                            "pilt": pilt,
                            "nimi": nimi
                        })
                except NoSuchElementException:
                    print("ei leidnud")

            return sõprade_list  # no more friends loaded

            # returnib listi, mis koosneb dictionarydest kujul {"pilt": pilt, "nimi": nimi}


if __name__ == '__main__':
    browser = ava_brauser()

    logi_sisse(browser, loe_andmed())
    soovi_õnne(browser)
