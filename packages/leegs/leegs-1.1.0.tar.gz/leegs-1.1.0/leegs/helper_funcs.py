import time, logging
# default genders
from .settings import emails, passwords
# undetected chromedriver so my account stops getting locked
import undetected_chromedriver as uc
# selenium imports
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
# other imports
import pandas as pd
import numpy as np

# creates a driver for each thread to use
def create_driver(headless:bool=False) -> uc.Chrome:
    # PROXY = "11.456.448.110:8080"
    options = uc.ChromeOptions()
    # options.add_argument(f'--proxy-server={PROXY}')
    if headless:
        options.add_argument('--headless')
    # view the headless session through local host
    # options.add_argument('--remote-debugging-port=9222')
    driver = uc.Chrome(options=options)
    driver.maximize_window()
    return driver

# checks if a captcha popped up on the screen
def check_for_captcha(driver: uc.Chrome) -> bool:
    try:
        title = driver.find_element(By.TAG_NAME, 'h2')
    except NoSuchElementException:
        return False
    if title.text.strip().lower() == 'verification':
        logging.info('Captcha detected. Handle manually.')
        time.sleep(10)
        return True
    return False

# checks if one of those compliance messages with the check box pops up
def check_for_compliance(driver: uc.Chrome) -> bool:
    try:
        x = driver.find_element(By.CLASS_NAME, 'form__label')
    except NoSuchElementException:
        return False
    if x.text.strip().startswith("I won't use tools that"):
        logging.info('Compliance detected. Handle manually.')
        time.sleep(10)
        return True
    return

# checks if the account got restricted
def check_for_restriction(driver: uc.Chrome) -> None:
    try:
        title = driver.find_element(By.TAG_NAME, 'h1')
    except NoSuchElementException:
        return
    if title.text.strip() == 'Access to your account has been temporarily restricted':
        logging.error("Account got restricted. Closing driver.")
        driver.quit()

# Logs in from the home page (fastest method)
def login_through_form(driver: uc.Chrome, *, email:str=emails[0], password:str=passwords[0], from_homepage:bool=False) -> bool:
    logging.info('Logging in...')
    # make sure you're at the right link
    if from_homepage: 
        driver.get('https://www.linkedin.com/')
    # type in email and passsword
    driver.find_element(By.ID, 'session_key').send_keys(email)
    driver.find_element(By.ID, 'session_password').send_keys(password)
    # click the sign-in button
    driver.find_element(By.CLASS_NAME, "sign-in-form__submit-button").click()
    time.sleep(2)
    check_for_captcha(driver)
    check_for_compliance(driver)
    check_for_restriction(driver)
    return True

# write detected genders to a csv
def write_genders_to_csv(csv_file: str, genders: dict[str]) -> None:
    logging.info('Writing genders to csv...')
    df = pd.read_csv(csv_file)
    # get rid of profile pic links
    del df['profile_pic']
    # genders is a dict where the keys are integer genders that correspong the index of the row in the csv (key+1 = index_row)
    # assign the genders to the rows that match up with the data rows
    # add a gender column
    df['gender'] = np.nan
    # add the genders to the dataframe
    for key, gender in genders.items():
        df.loc[key-1, 'gender'] = gender
    # write the dataframe to the csv
    df.to_csv(csv_file, index=False)
    return

# if __name__ == '__main__':
#     genders = {1: 'Male'}
#     csv_file = 'mini_data.csv'
#     write_genders_to_csv(csv_file, genders)