from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


#set the driver
PATH = "C:\Program Files (x86)\chromedriver.exe"
s = Service(PATH)
driver = webdriver.Chrome(service=s)
driver.get("https://pubmed.ncbi.nlm.nih.gov/advanced/")

#create the search method
def search(number_of_results, query):
    search = driver.find_element(By.ID, "query-box-input")
    search.clear()
    search.send_keys(query)
    search.send_keys(Keys.RETURN)
    number_of_pages = number_of_results // 10
    number_of_results_in_last_page = number_of_results % 10
    pmids = []
    for i in range(number_of_pages + 1):
        count = 0
        try:
            WebDriverWait(driver, 20).until(
                EC.text_to_be_present_in_element_attribute((By.ID, "bottom-page-number-input"),"value",str(i+1))
            )
            articles = driver.find_elements(By.CLASS_NAME, "full-docsum")
            for article in articles:
                count += 1
                if count > number_of_results_in_last_page and i == number_of_pages:
                    break
                pid = article.find_element(By.CLASS_NAME, "docsum-pmid")
                pmids.append(pid.text)
            next_button = driver.find_element(By.CSS_SELECTOR,".next-page-btn > .chevron-icon:nth-child(1)")
            next_button.click()
        except Exception as e:
            print(e)
            driver.quit()
            break
    driver.quit()
    return pmids

if __name__ == '__main__':
    query = "fever"
    pmids = search(number_of_results=12,query=query)
    print(pmids)