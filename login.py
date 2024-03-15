from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import re
import time 
# Replace these with your actual username and password
username = "bojanki.prudhviraj"
password = "LGsoft123@mar"
 
# Replace this with the URL of the website you want to login to
website_url = "http://mod.lge.com/hub/"
 
# Path to your webdriver executable
#webdriver_path = "C:\Users\Public\Desktop"
 
# Initialize the webdriver
driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()))
driver.implicitly_wait(5)
 
# Open the website
driver.get(website_url)
 
# Find the login form elements and fill them in
username_field = driver.find_element(By.ID, "username")
username_field.send_keys(username)
 
password_field = driver.find_element(By.ID,"password")
password_field.send_keys(password)
 
# Submit the login form
password_field.send_keys(Keys.RETURN)
 
# Wait for a few seconds to let the page load
time.sleep(5)
 
# Close the browser
driver.quit()