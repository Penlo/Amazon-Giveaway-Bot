import chromedriver_binary  # Adds chromedriver binary to path
import os
import urllib3
import time

from lxml import etree
from lxml import html
from requests import get
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


chromeOptions = webdriver.ChromeOptions()

# Storing our Chrome cookies in a subfolder called __chromedata__
cookies_full_path = os.path.join('__chromedata__')
if not os.path.exists(cookies_full_path):
    os.mkdir(cookies_full_path)
# chromeOptions.add_argument('--user-data-dir=chrome-data')         # Linux way
chromeOptions.add_argument('--user-data-dir=' + cookies_full_path)  # Windows way (full path)
driver = webdriver.Chrome(chrome_options=chromeOptions)


def element_exists(driver, lookup_str, lookup_by=By.CLASS_NAME):
    try:
        return driver.find_element(lookup_by, lookup_str)
    except:
        return None


def pause_mini():
    time.sleep(.5)


def pause_small():
    time.sleep(1)


def main():
    url = 'https://giveawaylisting.com/index2.html'
    urllib3.disable_warnings()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/77.0.3865.90 Safari/537.36'}
    response = get(url, headers=headers, verify=False, timeout=60)
    tree = html.fromstring(response.content)

    print('Aquiring list of giveway links...')
    table = tree.xpath('//table[@id="giveaways"]/tbody/tr[@class="lucky"]/td[1]/a/@href')
    print("Finished! Let's get started!\n")

    # Sometimes the top 3 class names are not correctly named so we skip them
    for giveaway_link in reversed(table[2:]):
        print(f'Opening Giveaway link: {giveaway_link}')
        driver.get(giveaway_link)
        pause_small()

        # Checking to see if we need to log in
        login_needed = element_exists(driver, 'participation-need-login')
        if login_needed:
            driver.find_element(By.XPATH, '//span[@class="a-button-inner"]').click()
            print('Please log in...')

        print('Waiting for page load to complete')
        ready = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//div[@class="a-section a-spacing-medium a-text-left"]'))
        )

        # Check to see if we have already participated in the giveaway
        if ready.text == 'Enter for a chance to win!':
            pause_mini()
            driver.find_element(By.XPATH, '//*[@class="a-text-center box-click-area"]').click()
        else:
            print('You already participated in this giveaway. Moving on.')
            continue

        try:
            print ('Waiting for the opening box to disappear')            
            WebDriverWait(driver, 20).until(
                EC.invisibility_of_element_located((By.CLASS_NAME, 'a-text-center box-click-area'))
            )

            while True:
                # This ensures we know what the result is because even though the box disappears
                # sometimes the result lags behind
                title = element_exists(driver, '//div[@class="a-section a-spacing-medium a-text-left"]', lookup_by=By.XPATH)
                if title and title.text != 'Enter for a chance to win!':
                    pause_mini()
                    break
                else:
                    print('Page loaded but not ready. Sleeping for 1 seconds.')
                    pause_small()

            if "You didn't win" in title.text:
                print("You didn't win.. movin on!")
                pause_mini()
                continue
            elif 'you won!' in title.text:
                print(title.text)
                print('You won!')
                break

        except NoSuchElementException:
            print('An unknown error has occurred.')


while True:
    if __name__ == '__main__':
        main()
