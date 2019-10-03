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

# Storing our Chrome cooking in a folder called __chromedata__
cookies_full_path = os.path.join('__chromedata__')
if not os.path.exists(cookies_full_path):
    os.mkdir(cookies_full_path)
chromeOptions.add_argument("--user-data-dir=" + cookies_full_path)  # Windows way (full path)

driver = webdriver.Chrome(chrome_options=chromeOptions)


def sel_element_exists(driver, lookup_str, lookup_by=By.CLASS_NAME):
    try:
        return driver.find_element(lookup_by, lookup_str)
    except:
        return None


def main():
    url = 'https://giveawaylisting.com/index2.html'
    urllib3.disable_warnings()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/77.0.3865.90 Safari/537.36'}
    response = get(url, headers=headers, verify=False, timeout=60)

    tree = html.fromstring(response.content)

    # Build our list of links
    table = tree.xpath("//table[@id='giveaways']/tbody/tr[@class='lucky']/td[1]/a/@href")

    for giveaway_link in table[2:]:  # Sometimes the top 3 class names are not correctly named so we skip them
        driver.get(giveaway_link)

        time.sleep(1)

        # Checking to see if we need to log in
        login_needed = sel_element_exists(driver, 'participation-need-login')

        if login_needed:
            driver.find_element_by_xpath('//span[@class="a-button-inner"]').click()

        while True:
            try:
                ready = driver.find_element_by_xpath(
                    "//div[@class='a-section a-spacing-medium a-text-left']")
            except NoSuchElementException:
                print("Page loaded but not ready. Sleeping for 2 seconds.")
                time.sleep(2)
            else:
                break

        # Check to see if we have already participated in the giveaway
        # If yes, then move on to the next one
        if ready.text == 'Enter for a chance to win!':
            time.sleep(.5)

            driver.find_element_by_xpath("//*[@class='a-text-center box-click-area']").click()
        else:
            continue

        try:
            # Waiting for the opening box to disappear
            element = WebDriverWait(driver, 20).until(
                EC.invisibility_of_element_located((By.CLASS_NAME, "a-text-center box-click-area"))
            )

            time.sleep(5)

            while True:
                # This ensures we know what the result is because even though the box disappears
                # sometimes the result lags behind
                title = sel_element_exists(driver, "//div[@class='a-section a-spacing-medium a-text-left']", lookup_by=By.XPATH)
                if title and title.text != 'Enter for a chance to win!':
                    time.sleep(.5)
                    break
                else:
                    print("Page loaded but not ready. Sleeping for 2 seconds.")
                    time.sleep(2)

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
            print("An unknown error has occurred.")


while True:
    if __name__ == "__main__":
        main()
