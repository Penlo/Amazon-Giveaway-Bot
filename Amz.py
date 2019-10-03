import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import os
import time
import chromedriver_binary  # Adds chromedriver binary to path
from lxml import etree
import urllib3
from requests import get
from lxml import html


chromeOptions = webdriver.ChromeOptions()

cookies_full_path = os.path.join('__chromedata__')
if not os.path.exists(cookies_full_path):
    os.mkdir(cookies_full_path)
chromeOptions.add_argument("--user-data-dir=" + cookies_full_path)  # Windows way (full path)

driver = webdriver.Chrome(chrome_options=chromeOptions)


def main():
    url = 'https://giveawaylisting.com/index2.html'
    urllib3.disable_warnings()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/77.0.3865.90 Safari/537.36'}
    response = get(url, headers=headers, verify=False, timeout=60)

    tree = html.fromstring(response.content)

    table = tree.xpath("//table[@id='giveaways']/tbody/tr[@class='lucky']/td[1]/a/@href")

    for giveaway_link in table[2:]:
        driver.get(giveaway_link)

        while True:
            try:
                ready = driver.find_element_by_xpath(
                    "//div[@class='a-section a-spacing-medium a-text-left']")
            except NoSuchElementException:
                print("Page loaded but not ready. Sleeping for 2 seconds.")
                time.sleep(2)
            else:
                break

        if ready.text == 'Enter for a chance to win!':
            time.sleep(.5)

            driver.find_element_by_xpath("//*[@class='a-text-center box-click-area']").click()
        else:
            continue

        try:
            element = WebDriverWait(driver, 20).until(
                EC.invisibility_of_element_located((By.CLASS_NAME, "a-text-center box-click-area"))
            )

            time.sleep(5)

            title = driver.find_element_by_xpath(
                "//div[@class='a-section a-spacing-medium a-text-left']")

            while True:
                try:
                    title != 'Enter for a chance to win!'
                except NoSuchElementException:
                    print("Page loaded but not ready. Sleeping for 2 seconds.")
                    time.sleep(2)
                else:
                    time.sleep(.5)
                    break

            if "You didn't win" in title.text:
                print("You didn't win.. movin on!")
                time.sleep(1.5)
                continue
            else:
                time.sleep(5)
                if 'you won!' in title.text:
                    print(title.text)
                    print("You won!")
                    break

        except NoSuchElementException:
            print("title not loaded yet. Sleeping for 1 seconds.")
            time.sleep(1)


while True:
    if __name__ == "__main__":
        main()
