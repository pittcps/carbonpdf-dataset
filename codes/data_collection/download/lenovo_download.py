from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import os

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Set up the Chrome WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# URL of the Lenovo eco-declaration page
url = 'https://www.lenovo.com/us/en/compliance/eco-declaration/'

driver.get(url)
time.sleep(6)  # Wait for initial page load

# Navigate to 'Notebooks & Ultrabooks' section
notebooks_tab = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "tablets-tab"))
)

# Scroll to the element
driver.execute_script("arguments[0].scrollIntoView();", notebooks_tab)

time.sleep(2)

# Try clicking using JavaScript
driver.execute_script("arguments[0].click();", notebooks_tab)

# Find all links that contain 'PCF' or 'pcf' in their href and download them
links = driver.find_elements(By.XPATH, "//a[contains(translate(@href, 'PCF', 'pcf'), 'pcf') and contains(@href, '.pdf')]")
for link in links:
    pcf_url = link.get_attribute('href')
    if pcf_url.startswith('http'):
        response = requests.get(pcf_url)
        if response.status_code == 200:
            file_name = os.path.join('lenovo/tablets', pcf_url.split('/')[-1])
            with open(file_name, 'wb') as f:
                f.write(response.content)
    else:
        print(f"Invalid URL: {pcf_url}")

driver.quit()
