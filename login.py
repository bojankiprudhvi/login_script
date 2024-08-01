import time
import logging
import os
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration
USERNAME = "Phanindra.Vemuganti@synopsys.com"
PASSWORD = "Phani7@180020040"
LOGIN_URL = "https://ifazility.com/Optdesk/Account/Login"
BOOKING_URL = "https://ifazility.com/optdesk/Admin/WorkStationBook"
TIMEOUT = 10  # seconds

def initialize_driver():
    """Initialize the Chrome WebDriver."""
    driver = webdriver.Chrome()
    driver.implicitly_wait(TIMEOUT)
    return driver

def login(driver):
    """Log into the website."""
    logging.info("Opening login page.")
    driver.get(LOGIN_URL)
    
    try:
        username_field = WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable((By.ID, "txtUserName")))
        username_field.send_keys(USERNAME)

        password_field = WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable((By.ID, "txtPassword")))
        password_field.send_keys(PASSWORD)
        password_field.send_keys(Keys.RETURN)
        toast_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.toast-message"))
            )
        toast_text = toast_message.text
      #  print(toast_text)
        logging.info(toast_text)
    except Exception as e:
        logging.error(f"Error during login: {e}")
        driver.quit()

def book_workstation(driver):
    """Book a workstation."""
    logging.info("Navigating to booking page.")
    driver.get("https://ifazility.com/optdesk/Admin/workstationbook")
    try:                
        time.sleep(2)
        tomorrow = datetime.now() + timedelta(days=6)
        tomorrow_date = tomorrow.strftime('%m/%d/%Y')

        # Set date fields
        set_date_field(driver, 'searchfromdate', tomorrow_date)
        set_date_field(driver, 'searchtodate', tomorrow_date)
 
        # Select time from dropdown
        select_dropdown(driver, 'dtsearchfrom', "10:40:00")
 
        # Click search button
        driver.find_element(By.ID, 'btnsearch').click()
 
        # Set workstation coordinates
        set_workstation_coordinates(driver, "1041", "1437")
 
        # Execute JavaScript function to check booking status
        execute_booking_status_function(driver)
 
        # Select time for start time dropdown
        select_dropdown(driver, 'tmestart', "10:40:00")
 
        # Save the booking
        save_booking(driver)
       
        toast_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.toast-message"))
            )
        toast_text = toast_message.text
      #  print(toast_text)
        logging.info(toast_text)
        logging.info("Booking process completed successfully.")
    except Exception as e:
         # Take a screenshot
        screenshot_dir = '/tmp/screenshots/'
        driver.save_screenshot(os.path.join(screenshot_dir, 'screenshot.png')) # Save to the correct directory
       # toast_message = WebDriverWait(driver, 10).until(
       #     EC.presence_of_element_located((By.CSS_SELECTOR, "div.toast-message"))
        #    )
        #toast_text = toast_message.text
      #  print(toast_text)
        #logging.info(toast_text)
        logging.error(f"Error during booking: {e} failed to book the cubical since its is booked by someone ")
    finally:
       time.sleep(5)
       driver.quit()

def set_date_field(driver, field_id, date_value):
    """Set the date field using JavaScript."""
    date_field = driver.find_element(By.ID, field_id)
    driver.execute_script("arguments[0].setAttribute('value', arguments[1])", date_field, date_value)

def select_dropdown(driver, dropdown_id, value):
    """Select a value from a dropdown menu."""
    dropdown = driver.find_element(By.ID, dropdown_id)
    select = Select(dropdown)
    select.select_by_value(value)

def set_workstation_coordinates(driver, x1_value, y1_value):
    """Set the workstation coordinates."""
    driver.execute_script("document.getElementById('X1').value = '{}';".format(x1_value))
    driver.execute_script("document.getElementById('Y1').value = '{}';".format(y1_value))

def execute_booking_status_function(driver):
    logging.info("Entered into execute_booking_status_function")
    """Execute the JavaScript function to check booking status."""
    starttime = driver.find_element(By.ID, "dtsearchfrom").get_attribute("value")
    endtime = driver.find_element(By.ID, "dtsearchto").get_attribute("value")
    date = driver.find_element(By.ID, "searchfromdate").get_attribute("value")
    enddate = driver.find_element(By.ID, "searchtodate").get_attribute("value")
    
    function_name = "checkbookingstatus_greyred"
    driver.execute_script(f"{function_name}(1041, 0, 1437, 0, '{date}', '{enddate}', '{starttime}', '{endtime}')")

def save_booking(driver):
    """Save the booking and confirm."""
    save_button = driver.find_element(By.XPATH, "//button[contains(@onclick, 'saveworkstation')]")
    save_button.click()
    
    time.sleep(2)  # Wait for the save action to complete
    confirm_button = driver.find_element(By.XPATH, "//button[text()='Click to Confirm']")
    confirm_button.click()

if __name__ == "__main__":
    driver = initialize_driver()
    screenshot_dir = '/tmp/screenshots/'
    os.makedirs(screenshot_dir, exist_ok=True)
    login(driver)
    book_workstation(driver)
