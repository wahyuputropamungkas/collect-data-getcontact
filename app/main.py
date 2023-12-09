from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from datetime import datetime
import time
import read_vcard
import os

ua = UserAgent(browsers=['chrome'])
userAgent = ua.random
userAgents = [userAgent]
mainURL = 'https://web.getcontact.com/'

def writeTags(tags, contact):
    if len(tags) > 0:
        directory = './results'
        currentTime = datetime.now()
        resultDirectory = os.path.join(directory, currentTime.strftime('%Y%m%d'))
        resultFilename = f"{contact}-{currentTime.strftime('%Y%m%d%H%M%S')}.txt"

        os.makedirs(resultDirectory, exist_ok=True)

        with open(os.path.join(resultDirectory, resultFilename), 'a+') as f:
            for tag in tags:
                try:
                    f.write(f'{tag}\n')
                except Exception as e:
                    f.write(f'{str(e)}\n')

def openWeb():
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('log-level=3')
    options.add_argument("--window-size=1280,720")
    options.add_argument("user-data-dir=C:\\Users\\Angelcrusher\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 1")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    driver = webdriver.Chrome(options=options)

    # driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    # for agent in userAgents:
    #     driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": agent})

    driver.get(url=mainURL)

    time.sleep(5)

    # waiting for form

    try:
        webPage = WebDriverWait(driver=driver, timeout=60).until(expected_conditions.presence_of_element_located((By.TAG_NAME, 'form')))
    except Exception as e:
        print('Unable to find form element')

        return True

    contacts = read_vcard.getContacts()

    if len(contacts) > 0:
        for contact in contacts:
            if contact['name'] is not None and contact['cell'] is not None:
                driver.find_element(By.ID, 'numberInput').clear()
                driver.find_element(By.ID, 'numberInput').send_keys(contact['cell'])

                # submit form

                actionButtons = driver.find_elements(By.ID, 'submitButton')

                if len(actionButtons) > 0:
                    actionButtons[0].click()

                # waiting for result

                try:
                    backButton = WebDriverWait(driver=driver, timeout=60).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'r-back')))
                except Exception as e:
                    print('Unable to get back button')

                    return True

                time.sleep(2)

                notAvailableElement = driver.find_elements(By.XPATH, '//p[contains(text(), "invalid")]')

                if len(notAvailableElement) > 0:
                    print(f'{contact["cell"]} is not available')

                    continue

                # waiting for tag link

                visibleTagButton = driver.find_elements(By.XPATH, '//div[contains(@class, "r-tag-box")]')

                if len(visibleTagButton) == 0:
                    print(f'{contact["cell"]} tag is not available')

                    continue

                try:
                    tagLink = WebDriverWait(driver=driver, timeout=60).until(expected_conditions.presence_of_element_located((By.XPATH, '//div[contains(@class, "r-tag-box")]')))
                except Exception as e:
                    print('Unable to get profile')

                    return True

                # click for tags

                tagButtons = driver.find_elements(By.XPATH, '//div[contains(@class, "r-tag-box")]')

                if len(tagButtons) > 0:
                    tagButtons[0].click()

                # waiting for tags

                time.sleep(2)

                try:
                    webPage = WebDriverWait(driver=driver, timeout=60).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'rtl-item')))
                except Exception as e:
                    print('Unable to get tags')

                    return True

                tags = driver.find_elements(By.CLASS_NAME, 'rtl-item')

                if len(tags) > 0:
                    readyTags = []

                    for tag in tags:
                        readyTags.append(tag.text)

                    writeTags(tags=readyTags, contact=contact['cell'])

                    print(f'{contact} : {str(len(readyTags))} tags')

openWeb()