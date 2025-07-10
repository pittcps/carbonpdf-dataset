from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import os
from urllib.parse import urlparse, parse_qs

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Set up the Chrome WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# URL of the website
url = 'https://h20195.www2.hp.com/v2/Library.aspx#&country-us&prodtype_oid-321957&sortorder-popular&teasers-off&isRetired-false&isRHParentNode-false&titleCheck-false'
driver.get(url)

# Wait for the page to load
time.sleep(15)

# Function to accept policy alert if present
def accept_policy_alert():
    try:
        policy_alert_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//button[text()='I ACCEPT']"))
        )
        if policy_alert_button.is_displayed():
            policy_alert_button.click()
            time.sleep(2)  # Wait for the policy alert to be dismissed
    except Exception as e:
        print("No policy alert found or error in dismissing it:", e)

accept_policy_alert()

# Function to click the 'Load More' button
def click_load_more():
    try:
        load_more_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "loadMore"))
        )
        # Check if the button is displayed and clickable
        if load_more_button.is_displayed():
            load_more_button.click()
            return True
        else:
            return False
    except:
        # If 'Load More' button is not found or not clickable
        return False

# Keep clicking 'Load More' until it's no longer visible
while click_load_more():
    time.sleep(15)  # Wait for the page to load more content


# Directory to save PDFs
save_directory = '../hp/laptops'
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

# Locate PDF links
pdf_links = driver.find_elements(By.XPATH, "//a[contains(@href, 'GetDocument.aspx')]")

# Download PDF files
for link in pdf_links:
    pdf_url = link.get_attribute('href')
    parsed_url = urlparse(pdf_url)
    docname = parse_qs(parsed_url.query)['docname'][0]
    pdf_filename = f"{docname}.pdf"
    # pdf_response = requests.get(pdf_url)
    pdf_response = requests.get(pdf_url, verify=False)
    if pdf_response.status_code == 200:
        full_path = os.path.join(save_directory, pdf_filename)
        with open(full_path, 'wb') as file:
            file.write(pdf_response.content)

driver.quit()

