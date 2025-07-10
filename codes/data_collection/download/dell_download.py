# from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests
import os


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)


# # Setup Selenium WebDriver
# driver = webdriver.Chrome('/home/kaz81/Downloads/chromedriver-linux64/chromedriver')  # Replace with the path to your chromedriver
url = 'https://www.dell.com/en-us/dt/corporate/social-impact/advancing-sustainability/climate-action/product-carbon-footprints.htm#tab0=0'
driver.get(url)

# Wait for the page to load
# time.sleep(5)

# Click on the 'Desktops' tab
# desktops_tab = driver.find_element(By.ID, "tab-0")  # ID of the 'Desktops' tab
# desktops_tab.click()

# Wait for the content to load
time.sleep(5)

# Directory to save PDFs
save_directory = '../dell/desktops_workstations'
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

# Locate PDF links
pdf_links = driver.find_elements(By.XPATH, "//a[contains(@href, '.pdf')]")

# Download PDF files
for link in pdf_links:
    pdf_url = link.get_attribute('href')
    pdf_response = requests.get(pdf_url)
    if pdf_response.status_code == 200:
        pdf_filename = os.path.join(save_directory, os.path.basename(pdf_url))
        with open(pdf_filename, 'wb') as file:
            file.write(pdf_response.content)

driver.quit()
