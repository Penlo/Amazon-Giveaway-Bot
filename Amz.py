import chromedriver_binary  # Adds chromedriver binary to path
import os
import pickle
import urllib3
import time

from lxml import etree
from lxml import html
from requests import get
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import InvalidArgumentException
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


def amazon_video(driver):
    # Checking if its an Amazon Video. If it is then execute
    try:
        driver.find_element(By.XPATH, '//div[@class="amazon-video"]').click()
        pause_small()
        print('Waiting for button to be clickable')
        submit = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//button[@class="a-button a-button-primary amazon-video-continue-button"]'))
        )
        submit.click()
    except:
        return False


def youtube_video(driver):
    # Test if its an Youtube Video. If it is then execute
    try:
        js = 'document.evaluate("//div[@class=\'youtube-video\']/a", document.body, null, 9, null). singleNodeValue.click();'
        driver.execute_script(js)
        pause_small()
        submit = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//button[@class="a-button a-button-primary youtube-continue-button"]'))
        )
        submit.click()
    except:
        return False


def instant_box(driver):
    # Test if its an Instant win box. If it is then execute
    try:
        driver.find_element(By.XPATH, '//*[@class="a-text-center box-click-area"]').click()
        pause_small()
    except:
        return False


def give_away_type(driver):
    ga_type = 0
    # Checking if its an Amazon Video
    try:
        driver.find_element(By.XPATH, '//div[@class="amazon-video"]')
        ga_type = 1
        return ga_type
    except:
        # Checking if its a Youtube Video
        try:
            driver.find_element(By.XPATH, '//div[@class="youtube-video"]')
            ga_type = 2
            return ga_type
        except:
            # Checking if its an Instant Win box
            try:
                driver.find_element(By.XPATH, '//*[@class="a-text-center box-click-area"]')
                ga_type = 3
                return ga_type
            except:
                return ga_type


def main():
    you_won = False

    # Grab all the links
    url = 'https://giveawaylisting.com/index2.html'
    urllib3.disable_warnings()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/77.0.3865.90 Safari/537.36'}
    response = get(url, headers=headers, verify=False, timeout=60)
    tree = html.fromstring(response.content)

    print('Aquiring list of giveway links...')
    table = tree.xpath('//table[@id="giveaways"]/tbody/tr[@class="lucky video" or @class="lucky"]/td[1]/a/@href')

    print("Finished! Let's get started!\n")

    # Sometimes the top 3 class names are not correctly named so we skip them
    fresh_links = table[2:]

    # Reverse list because giveaways ending soonest are in the end of the list
    fresh_links.reverse()

    # Load past links list from pickle
    dir_path, _ = os.path.split(os.path.abspath(__file__)) # path of executing file
    PICKLE_FILE_PATH = os.path.join(dir_path, 'pastlinks.pickle')
    try:
        past_links = pickle.load(open(PICKLE_FILE_PATH, 'rb'))
    except (OSError, IOError) as e:
        past_links = []

    # Setup links so we only use unattemped and store attempted that are still fresh
    if past_links:
        # Remove old links: remove from past_links what IS NOT in fresh_links
        past_links = list(set(past_links) & set(fresh_links))
        # Remove attempted links: remove from fresh_links what IS in past_links
        fresh_links = [item for item in fresh_links if item not in past_links]  # This method preserves order
    
	# If zero links available then sleep for one hour.
    if len(fresh_links) == 0:
        print('No giveaways, sleeping for one hour')
        time.sleep(3600)  # Sleep for one hour
        return False
	
    for i, giveaway_link in enumerate(fresh_links):
        try:
            print(f'Opening Giveaway link: {giveaway_link}  ({i+1} of {len(fresh_links)})')
            driver.get(giveaway_link)
            pause_small()

            # Checking to see if we need to log in
            login_needed = element_exists(driver, 'participation-need-login')
            if login_needed:
                driver.find_element(By.XPATH, '//span[@class="a-button-inner"]').click()
                print('Please log in...')

            # Checking to see if the giveaway has ended
            ended_check = element_exists(driver, 'a-section a-spacing-medium a-padding-base not-active')
            if ended_check:
                continue

            print('Waiting for page load to complete')
            pause_small()
            ready = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//div[@class="a-section a-spacing-medium a-text-left"]'))
            )

            # Store link as already attempted
            past_links.append(giveaway_link)
            if (i % 50) == 0:
                # Store all attempted links for later - write this every 50 iterations
                print(f'--- Dumping attempted links to pickle:  {PICKLE_FILE_PATH}')
                pickle.dump(past_links, open(PICKLE_FILE_PATH, 'wb'))

            # Check to see if we have already participated in the giveaway
            if ready.text == 'Enter for a chance to win!':
                # Check type of Giveaway and run
                ga_run = give_away_type(driver)
                if ga_run == 1:
                    print('Playing Amazon Video')
                    amazon_video(driver)
                elif ga_run == 2:
                    print('Playing Youtube Video')
                    youtube_video(driver)
                elif ga_run == 3:
                    print('Opening Box')
                    instant_box(driver)
                else:
                    print("Could not determine type of Giveaway. Moving on..")
                    continue

                print('Waiting for the box to disappear')
                WebDriverWait(driver, 30).until(
                    EC.invisibility_of_element_located((By.CLASS_NAME, 'a-text-center box-click-area'))
                )

            else:
                print('You already participated in this giveaway. Moving on.')
                continue

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
                you_won = True
                break
        except InvalidArgumentException as e:
            raise e

        except Exception as e:
            print(e)
            # Move onto next link, regardless of error this link produced
            pass

    # Finished with fresh_links. Store all attempted links for later
    pickle.dump(past_links, open(PICKLE_FILE_PATH, 'wb'))
    return you_won


if __name__ == '__main__':

    while True:
        if main():
            print('Yay! I won!')
            break
