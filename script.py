import os
import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import concurrent.futures
from webdriver_manager.chrome import ChromeDriverManager
import threading



def initialize_driver(chromedriver_path):
    current_directory = os.getcwd()
    chromedriver_path = os.path.join(current_directory, "chromedriver")
    os.environ["PATH"] += os.pathsep + os.path.dirname(chromedriver_path)
    service = Service(executable_path=chromedriver_path)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def navigate_to_problemset(driver):
    problemset_btn = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable( (By.CSS_SELECTOR, f'a[href="/problemset') )
    )
    problemset_btn.click()


def get_all_problems_from_page(driver, url, threadname):
    driver.get(url)
    time.sleep(3)
    
    problem_row = WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, 'tr'))
    )
    for i in range(1,50):
        cells = WebDriverWait(problem_row[i], 30).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, 'td'))
        )
        for i in range(2):
            if i == 0: ##problem id
                problem_id_link = cells[i].find_element(By.TAG_NAME, "a")
                problem_id_text = problem_id_link.text
                print(threadname, end=": ")
                print(problem_id_text, end=" ")
            else:
                elements_of_name_cell = WebDriverWait(cells[i],5).until(
                    EC.presence_of_all_elements_located((By.TAG_NAME, 'div'))
                )
                for i in range(len(elements_of_name_cell)):
                    if i == 0:
                        problem_name_link = elements_of_name_cell[i].find_element(By.TAG_NAME, 'a')
                        problem_name_text = problem_name_link.text
                        print(problem_name_text, end=" ")
                    else:
                        try:
                            tags_list = WebDriverWait(elements_of_name_cell[i],0.001).until(
                                EC.visibility_of_all_elements_located((By.TAG_NAME, 'a'))
                            )
                            for tag in tags_list:
                                tag_name = tag.text
                                print(tag_name, end=" ")
                        except:
                            pass

                        
        print()
def main():
    chromedriver_path = "chromedriver"
    driver = initialize_driver(chromedriver_path)
    driver.get('https://codeforces.com/')
    navigate_to_problemset(driver)

    mainlink = "https://codeforces.com/problemset/page/"
    
    noOfThreads = 10
    threads = []
    for i in range(noOfThreads):
        tname = f"Thread {i+1}"
        t = threading.Thread(target=get_all_problems_from_page,daemon=True ,args=[driver, "https://codeforces.com/problemset/page/{i}", tname])
        t.start()
        threads.append(t)

    for i in range(noOfThreads):
        threads[i].join()


    driver.quit()


if __name__ == "__main__":
    try:
        start = time.perf_counter()
        main()
        finish = time.perf_counter()
        print(f"Finished in {round(finish-start, 2)} second(s)")
    except selenium.common.exceptions.NoSuchWindowException:
        print("The browser window was closed by user.")
    except Exception as e:
        print(f"An error occurred: {e}")


