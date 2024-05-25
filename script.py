import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import requests
import threading

def initialize_driver(chromedriver_path):

    if not os.path.isfile(chromedriver_path):
        raise FileNotFoundError(f"ChromeDriver not found at path: {chromedriver_path}")

    service = Service(executable_path=chromedriver_path)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")

    driver = webdriver.Chrome(service=service, options=options)
    return driver


def get_all_problems_from_page(driver, thread_id, url, home_page, stop_flag):
    driver.get(url)
    time.sleep(3)
    problem_rows = WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, 'tr'))
    )
    for i in range(1, 30):
        if stop_flag.is_set():
            print(f"Thread {thread_id} stopping early.")
            break

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
        home_page.add_row(thread_id, problem_id, problem_name, ", ".join(tags))
            
        for i in range(2):
            if i == 0:
                problem_id_link = cells[i].find_element(By.TAG_NAME, "a")
                problem_id_text = problem_id_link.text
                problem_link_url = problem_id_link.get_attribute("href")
                response = requests.get(problem_link_url)
                print(problem_id_text, end=" ")
            else:
                elements_of_name_cell = WebDriverWait(cells[i],30).until(
                    EC.presence_of_all_elements_located((By.TAG_NAME, 'div'))
                )
                for i in range(len(elements_of_name_cell)):
                    if i == 0:
                        problem_name_link = elements_of_name_cell[i].find_element(By.TAG_NAME, 'a')
                        problem_name_text = problem_name_link.text
                        print(problem_name_text, end=" ")
                    else:
                        tags_list = WebDriverWait(elements_of_name_cell[i],30).until(
                            EC.presence_of_all_elements_located((By.TAG_NAME, 'a'))
                        )
                        html_content = """
                        <!DOCTYPE html>
                        <html lang="en">
                        <head>
                            <meta charset="UTF-8">
                            <meta http-equiv="refresh" content="0;url={}">
                            <title>Redirecting...</title>
                        </head>
                        <body>
                            <p>If you are not redirected, <a href="{}">click here</a>.</p>
                        </body>
                        </html>
                        """.format(problem_link_url, problem_link_url)

                        if response.status_code == 200:
                            for tag in tags_list:
                                tag_name = tag.text
                                print(tag_name, end=" ")
                                tag_folder = "./{}".format(tag_name)
                                if not os.path.exists(tag_folder):
                                    os.makedirs(tag_folder)
                                with open("{}/{}.html".format(tag_folder, problem_name_text), "w") as file:
                                    file.write(html_content)

        print()

def main(chromedriver_path, noOfThreads, home_page, stop_flag):
    driver = initialize_driver(chromedriver_path)
    driver.get('https://codeforces.com/')

    threads = []
    for i in range(int(noOfThreads)):
        tname = f"Thread {i+1}"
        driver = initialize_driver(chromedriver_path)
        t = threading.Thread(target=get_all_problems_from_page, daemon=True, args=[driver, tname, f"https://codeforces.com/problemset/page/{i+1}", home_page, stop_flag])
        t.start()
        threads.append(t)

    for i in range(int(noOfThreads)):
        threads[i].join()

    driver.quit()
