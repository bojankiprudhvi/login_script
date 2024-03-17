from selenium import webdriver
from datetime import datetime, timedelta
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import smtplib
from email.message import EmailMessage
import re
import time 



#email notifaction in case of failure
def send_email(subject, body):
    sender_email = "ooorikehemanth@gmail.com"
    sender_password = "Hemanth@99"
    receiver_email = "phanindravemuganti1999@gmail.com"

    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(sender_email, sender_password)
    server.send_message(msg)
    server.quit()
try:
    # Replace these with your actual username and password
    username = "Phanindra.Vemuganti@synopsys.com"
    password = "Phani7@180020040"
    
    # Replace this with the URL of the website you want to login to
    website_url = "https://ifazility.com/Optdesk/Account/Login"
    
    # Path to your webdriver executable
    #webdriver_path = "C:\Users\Public\Desktop"
    
    # Initialize the webdriver
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()))
    driver.implicitly_wait(5)
    
    # Open the website
    driver.get(website_url)

    # Find the login form elements and fill them in
    username_field = driver.find_element(By.ID, "txtUserName")
    username_field.send_keys(username)
    
    password_field = driver.find_element(By.ID,"txtPassword")
    password_field.send_keys(password)
    
    # Submit the login form
    password_field.send_keys(Keys.RETURN)
    
    # Wait for a few seconds to let the page load
    time.sleep(2)

    booking_url = "https://ifazility.com/optdesk/Admin/WorkStationBook"
    driver.get(booking_url)

    # Wait for a few seconds to let the page load
    time.sleep(2)

    # Find the date field element by its ID
    state_date = driver.find_element(By.ID, 'searchfromdate')

    # Calculate tomorrow's date
    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow_date = tomorrow.strftime('%m/%d/%Y')  # Format as MM/DD/YYYY

    # Update the value of the date field with tomorrow's date
    driver.execute_script("arguments[0].setAttribute('value', arguments[1])", state_date, tomorrow_date)

    # Find the date field element by its ID
    end_date = driver.find_element(By.ID, 'searchtodate')

    # Update the value of the date field with tomorrow's date
    driver.execute_script("arguments[0].setAttribute('value', arguments[1])", end_date, tomorrow_date)

    # Find the dropdown element by its ID
    dropdown = driver.find_element(By.ID,"dtsearchfrom")

    # Create a Select object from the dropdown element
    select = Select(dropdown)
    #Select by value
    select.select_by_value("10:40:00")


    #clicking the select button
    submit_button = driver.find_element(By.ID, 'btnsearch')

    submit_button.click()

    #1041 1437 cubicl ws-151
    # Set the desired values for X1 and Y1
    new_x1_value = "1041"
    new_y1_value = "1437"
    x1_values = driver.find_element(By.ID, 'X1')
    y1_values = driver.find_element(By.ID, 'Y1')
    driver.execute_script("document.getElementById('X1').value = '{}'".format(new_x1_value))
    driver.execute_script("document.getElementById('Y1').value = '{}'".format(new_y1_value))

    # Identify the JavaScript function and its parameters
    function_name = "checkbookingstatus_greyred"

    # Find the elements and get their values
    starttime_element = driver.find_element(By.ID,"dtsearchfrom")
    starttime = starttime_element.get_attribute("value")

    endtime_element = driver.find_element(By.ID,"dtsearchto")
    endtime = endtime_element.get_attribute("value")

    date_element = driver.find_element(By.ID,"searchfromdate")
    date = date_element.get_attribute("value")

    enddate_element = driver.find_element(By.ID,"searchtodate")
    enddate = enddate_element.get_attribute("value")

    # Identify the JavaScript function and its parameters
    #function_name = "myFunction"

    # Execute the JavaScript function using Selenium
    #driver.execute_script(f"{function_name}('{starttime}', '{endtime}', '{date}', '{enddate}')")

    new_x2_value =0
    new_y2_value =0
    # Execute the JavaScript function using Selenium
    driver.execute_script(f"{function_name}({new_x1_value},{new_x2_value}, {new_y1_value},{new_y2_value}, '{date}', '{enddate}', '{starttime}', '{endtime}')")
    save_button = driver.find_element(By.XPATH, "//button[contains(@onclick, 'saveworkstation')]")

    # Click the "Save" button
    save_button.click()

    time.sleep(5)
    confirm_button = driver.find_element(By.XPATH, "//button[text()='Click to Confirm']")

    # Click the "Click to Confirm" button
    confirm_button.click()
    error_message = "successfully booked the 151 cubical to you please cross check once."
    send_email("Cubical booking success Notification", error_message)


    time.sleep(50)
    # Close the browser
    driver.quit()
    

except Exception as e:
    error_message = f"An error occurred in the script: {str(e)}"
    send_email("Cubical booking Notification", error_message)
