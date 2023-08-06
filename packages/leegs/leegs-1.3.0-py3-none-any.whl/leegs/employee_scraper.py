import re, logging, sys, time, random
import concurrent.futures
import numpy as np
# default values
from .settings import emails, passwords, num_threads
# undetected chromedriver so my account stops getting locked
import undetected_chromedriver as uc
# selenium imports
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
# data storage
from .data_storage import Employees
# funcs imports
from .helper_funcs import check_for_captcha, check_for_compliance, login_through_form, create_driver
# cli imports
from tqdm import tqdm

# # concurrent function that runs extract_employee information on multiple threads
# def get_all_employee_data(employees: list[str]) -> Employees:
#     x = len(employees)
#     # split up employees into `num_threads` lists to evenly distribute workload across threads
#     employees = [employees[i::num_threads] for i in range(num_threads)]
#     # create global employees object for all threads to access
#     employee_storage = Employees()
#     drivers = list()
#     # add a loader for creating the drivers
#     for i in tqdm(range(num_threads), desc='Creating Threaded Browsers'):
#         driver = create_driver(headless=i) # all healdless except the first (gross that this code works tbh)
#         logging.info(f'Logging in as {emails[i]}...')
#         login_through_form(driver, email=emails[i], password=passwords[i], from_homepage=True)
#         drivers.append(driver)
#     # loader
#     loader = tqdm(total=x, desc='Crawling Profiles')
#     # create a thread pool
#     with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
#         # lambda takes in a driver, employees, & storage -- calls extract_employee_info for each employee in list
#             # (d,l,s) == (driver, profile_link, employee_storage)
#         results = executor.map(lambda d,e,s,l: [extract_employee_info(d,p,s,l) for p in e], drivers, employees, [employee_storage]*num_threads, [loader]*num_threads)
#     # close drivers
#     for driver in drivers:
#         driver.quit()
#     # run any remaining profile_links with a new driver that uses the best email
#     res = [x for x in results]
#     errors = [len(r) for r in res]
#     best_login = np.argmin(errors)
#     d = create_driver(headless=False)
#     login_through_form(d, email=emails[best_login], password=passwords[best_login], from_homepage=True)
#     # flatten results & only take the profile_links that were not successfully extracted
#     res = [item for sublist in res for item in sublist if item]
#     # run the remaining profile_links through extract_employee_info
#     for profile_link in res:
#         extract_employee_info(d, profile_link, employee_storage, loader)
#     # close driver
#     d.quit()
#     logging.info(employee_storage[0])
#     return employee_storage

# get all employee data from a list of LinkedIn profiles
# using a single driver to login and extract data
def get_all_employee_data(employees: list[str]) -> Employees:
    # driver = create_driver(headless=False)
    employee_storage = Employees()
    # login
    logging.info('Logging in...')
    # add drivers for threads
    drivers = list()
    for i in tqdm(range(num_threads), desc="Creating Threaded Browsers"):
        driver = create_driver(headless=i)
        login_through_form(driver, email=emails[i], password=passwords[i], from_homepage=True)
        drivers.append(driver)
    # loading bar
    loader = tqdm(total=len(employees), desc='Crawling Profiles')
    # split employees into `num_threads` lists to evenly distribute workload across threads
    employees = [employees[i::num_threads] for i in range(num_threads)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        executor.map(lambda d, e: [extract_employee_info(d, i, employee_storage, loader) for i in e], drivers, employees)
    # for employee in tqdm(employees):
    #     extract_employee_info(driver, employee, employee_storage)
    logging.info(f'Extracted {len(employee_storage)} profiles.')
    return employee_storage

# get the info for a single profile
def extract_employee_info(driver: uc.Chrome, profile_link:str, employees: Employees, loader: tqdm) -> str:
    # shut down thread by killing driver
    if not driver:
        return profile_link
    driver.get(profile_link)
    time.sleep(3)
    # if theres a sign in form prompt, press the sign in button and run the login function
    if driver.find_elements(By.CLASS_NAME, 'join-form'):
        driver.find_element(By.CLASS_NAME, 'authwall-join-form__form-toggle--bottom').click()
        passed = login_through_form(driver, email=emails[0], password=passwords[0])
        if passed:
            driver.get(profile_link)
        else:
            logging.error(f'Account got banned. Shutting down thread.')
            driver.quit()
            return profile_link
    # wait for the profile to load
    try:
        box = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'ph5')))
    except TimeoutException:
        if driver.find_elements(By.CLASS_NAME, 'join-form'):
            logging.info('Got logged out, logging back in...')
            return profile_link
        logging.error(f"Could not load profile info for {re.findall(r'https://www.linkedin.com/in/(.+)/', profile_link)[0]}")
        return profile_link
    # wait a little bit
    time.sleep(random.randint(1,3))
    # extract profile info
    # get name
    first_name, last_name = box.find_element(By.TAG_NAME, 'h1').text.split(maxsplit=1)
    # replace commas in last name
    last_name = last_name.replace(',', ';')
    # get label
    label = box.find_element(By.CLASS_NAME, 'text-body-medium').text
    # replace commas in label
    label = label.replace(',', ';')
    # scroll down a random amount between 100 and 450
    if random.randint(1,2) == 1:
        driver.execute_script(f"window.scrollTo(0, {random.randint(100,650)})")
    time.sleep(random.randint(0,3))
    if random.choice([True, False]):
        # scroll back up
        driver.execute_script(f"window.scrollTo(0, {random.randint(0,300)})")
    # get location
    location = box.find_element(By.CLASS_NAME, 'pb2').text
    # location sometimes has 'Contact Info' at the end of it and we wanna remove that
    location = location.split('Contact info')[0]
    # replace commas from location
    location = location.replace(',', ';')
    # get profile picture
    # check that they don't have a ghost profile pic
    if box.find_elements(By.CLASS_NAME, 'ghost-person'):
        profile_pic = ''
    else:
        profile_pic = box.find_element(By.CLASS_NAME, 'pv-top-card-profile-picture__image').get_attribute('src')
    # if profile_pic:
    #     download_profile_pic(profile_pic, f'{hash(first_name)}.jpg')
    # store all this info in the employees object
    employees.add_employee(first_name, last_name, label=label, location=location, profile_pic=profile_pic)
    logging.info(f'{first_name} {last_name} added to employees: {employees[0].label}')
    # update the loading bar
    loader.update(1)
    return ''

def get_employees_from_file(file:str, /, *, output:str, max_lines:float=float('inf')) -> None:
    '''
    Scrape LinkedIn profiles from a file.
    '''
    # get the list of public profiles
    logging.info('getting employee info...')
    if not file.endswith('.txt'):
        logging.error('Please specify a .txt file.')
        sys.exit(1)
    with open (file, 'r') as f:
        employees = [x.strip() for x in f.readlines()]
    company_employees = get_all_employee_data(employees)
    # write all the info to a csv file
    company_employees.save_as_csv(output, max_lines=max_lines)