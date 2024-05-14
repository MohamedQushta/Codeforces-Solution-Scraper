import os
import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import concurrent.futures

def initialize_driver(chromedriver_path):
    # Ensure chromedriver path is correct
    if not os.path.isfile(chromedriver_path):
        raise FileNotFoundError(f"ChromeDriver not found at path: {chromedriver_path}")

    # Explicitly set the path to the chromedriver executable
    service = Service(executable_path=chromedriver_path)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Optional: run in headless mode
    
    # Initialize the driver
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def navigate_to_problemset(driver):
    problemset_btn = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/problemset"]'))
    )
    problemset_btn.click()

def get_all_problems_from_page(driver, url, home_page):
    driver.get(url)
    time.sleep(3)
    problem_rows = WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, 'tr'))
    )
    for i in range(1, 30):
        cells = WebDriverWait(problem_rows[i], 30).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, 'td'))
        )
        problem_id = ""
        problem_name = ""
        tags = []

        if cells:
            problem_id_link = cells[0].find_element(By.TAG_NAME, "a")
            problem_id = problem_id_link.text

            elements_of_name_cell = WebDriverWait(cells[1], 5).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, 'div'))
            )

            if elements_of_name_cell:
                problem_name_link = elements_of_name_cell[0].find_element(By.TAG_NAME, 'a')
                problem_name = problem_name_link.text

                try:
                    tags_list = WebDriverWait(elements_of_name_cell[-1], 30).until(
                        EC.presence_of_all_elements_located((By.TAG_NAME, 'a'))
                    )
                    for tag in tags_list:
                        tag_name = tag.text
                        tags.append(tag_name)
                except:
                    tags.append("No tags")

        home_page.add_row(problem_id, problem_name, ", ".join(tags))

def main(chromedriver_path, home_page):
    driver = initialize_driver(chromedriver_path)
    driver.get('https://codeforces.com/')
    navigate_to_problemset(driver)

    mainlink = "https://codeforces.com/problemset/page/"
    urls = [mainlink + str(i) for i in range(1, 3)]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(get_all_problems_from_page, driver, url, home_page) for url in urls]
        concurrent.futures.wait(futures)

    driver.quit()
