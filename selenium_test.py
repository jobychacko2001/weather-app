from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
import time

# Define the URL of the remote Chrome WebDriver
chrome_url = "http://localhost:4444/wd/hub"

# Define the desired capabilities for Chrome
desired_capabilities = DesiredCapabilities.CHROME.copy()
desired_capabilities['browserName'] = 'chrome'
driver = webdriver.Remote(command_executor=chrome_url, desired_capabilities=desired_capabilities)

# Navigate to your web application
driver.get('http://127.0.0.1:8000/')

# Find the input field by its ID and enter "Toronto"
input_field = driver.find_element(By.ID, 'id_city')
input_field.clear()  # Clear any existing text
input_field.send_keys('Toronto')

# Click the "Get Weather" button
button = driver.find_element(By.ID, 'submit')
button.click()

# Wait for the weather info to load
time.sleep(5)  # Wait for 5 seconds (you may adjust this time as needed)

# Find the weather info elements and assert their presence
weather_info = driver.find_element(By.CLASS_NAME, 'weather-info')
assert weather_info.is_displayed(), "Weather info is not displayed"

# Further assertions can be added to validate the weather information content if needed

# Close the browser window
driver.quit()
